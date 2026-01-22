import json
import os
import re 
from typing import List, Dict, Any
from tools.cppcheck_tool import CppcheckTool
from core.build_manager import BuildManager
# --- תוספת 1: ייבוא הכלי החדש ---
from tools.valgrind_tool import ValgrindTool

class BenchmarkManager:
    def __init__(self, input_dir_name: str = "src", config_file: str = "expected_results.json"):
        """
        Initialize the manager.
        """
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.project_root = os.path.dirname(current_dir)
        self.src_path = os.path.join(self.project_root, input_dir_name)
        self.config_path = os.path.join(self.src_path, config_file)
        self.reports_path = os.path.join(self.project_root, "reports")

        self._validate_input()
        os.makedirs(self.reports_path, exist_ok=True)
        self.ground_truth = self._load_ground_truth()
        
        # אתחול מנהל הבנייה
        self.builder = BuildManager(self.src_path)
        
        # --- תוספת 2: רשימת הכלים ---
        self.static_tools = [CppcheckTool()]
        self.dynamic_tools = [ValgrindTool()]

    def _validate_input(self):
        if not os.path.isdir(self.src_path):
            raise FileNotFoundError(f"Input directory not found: {self.src_path}")
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Missing configuration file: {self.config_path}")
        try:
            with open(self.config_path, 'r') as f:
                json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format in: {self.config_path}: {e}")

    def _load_ground_truth(self) -> Dict:
        with open(self.config_path, 'r') as f:
            return json.load(f)

    def _parse_cmake_files(self) -> List[str]:
        cmake_path = os.path.join(self.src_path, "CMakeLists.txt")
        if not os.path.exists(cmake_path):
            print("Note: No CMakeLists.txt found in src.")
            return []

        print(f"Found CMakeLists.txt, parsing sources...")
        with open(cmake_path, 'r') as f:
            content = f.read()

        source_files = re.findall(r'([\w\-\./\\]+\.(?:cpp|c|cc|cxx))', content, re.IGNORECASE)
        return list(set(source_files))

    def get_files_to_test(self) -> List[Dict]:
        json_files_map = {item["filename"]: item.get("bugs", []) for item in self.ground_truth.get("files", [])}
        cmake_files = self._parse_cmake_files()
        
        final_file_list = []
        all_filenames = set(json_files_map.keys()) | set(cmake_files)
        
        for filename in all_filenames:
            clean_filename = os.path.basename(filename)
            full_path = os.path.join(self.src_path, clean_filename)
            
            if os.path.exists(full_path):
                expected_bugs = json_files_map.get(clean_filename, [])
                final_file_list.append({
                    "path": full_path,
                    "filename": clean_filename,
                    "expected_bugs": expected_bugs
                })
        return final_file_list

    def build_project(self):
        """Compiles the project using the BuildManager."""
        self.builder.clean_build()
        success = self.builder.run_build()
        if not success:
            raise RuntimeError("Project compilation failed. Aborting benchmark.")
        return self.builder.get_executables()

    def run_all_tests(self):
        # static analysis
        files_data = self.get_files_to_test()
        if files_data:
            print(f"\n=== Phase 1: Static Analysis ({len(files_data)} files) ===")
            for file_info in files_data:
                file_path = file_info["path"]
                filename = file_info["filename"]
                expected_bugs = file_info["expected_bugs"]

                print(f"\n[File]: {filename}")
                for tool in self.static_tools:
                    self._run_tool(tool, file_path, filename, expected_bugs)
        
        # build user's project
        print(f"\n=== Phase 2: Building Project ===")
        try:
            executables = self.build_project()
        except RuntimeError as e:
            print(e)
            return

        # dynamic analysis
        if executables:
            print(f"\n=== Phase 3: Dynamic Analysis ({len(executables)} executables) ===")
            for exe_path in executables:
                exe_name = os.path.basename(exe_path)
                print(f"\n[Executable]: {exe_name}")
                
                for tool in self.dynamic_tools:
                    self._run_tool(tool, exe_path, exe_name, [])
        else:
            print("No executables found to test.")
        
        print("\n--- Benchmark Completed ---")

    def _run_tool(self, tool, path, name, expected_bugs):
        """Helper to run a single tool and verify results."""
        tool_name = tool.__class__.__name__
        print(f"Running {tool_name} ...", end=" ", flush=True)

        try:
            result = tool.run(path)
            print("DONE.")
            
            found_bugs = result["bugs"] if isinstance(result, dict) and "bugs" in result else []
            self._verify_result(name, tool_name, found_bugs, expected_bugs)
                    
        except Exception as e:
            print(f"FAILED.")
            print(f"Error: {e}")

    # compare expected results with the ones found
    def _verify_result(self, filename: str, tool_name: str, found_bugs: List[Dict], expected_bugs: List[Dict]):
        print(f"[Verification - {tool_name}]")
        
        if not expected_bugs and found_bugs:
            print(f"Found {len(found_bugs)} bugs (No verification data).")
            print("[Findings]:")
            for bug in found_bugs:
                print(f" - {bug.get('message')}")
            return

        expected_count = len(expected_bugs)
        found_count = len(found_bugs) if found_bugs else 0

        if found_count >= expected_count and expected_count > 0:
             print(f"SUCCESS: Found {found_count} bugs (Expected: {expected_count})")
        elif expected_count == 0 and found_count == 0:
             print(f"SUCCESS: Clean file (as expected).")
        else:
            print(f"MISMATCH: Found {found_count} bugs but expected {expected_count}.")
            if found_count > 0:
                 print("[Actual Findings]:")
                 for bug in found_bugs:
                     line = bug.get('line', '?')
                     message = bug.get('message', 'No message')
                     severity = bug.get('severity', '?')
                     print(f" - Line {line} [{severity}]: {message}")