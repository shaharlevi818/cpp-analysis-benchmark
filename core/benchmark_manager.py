import json
import os
from typing import List, Dict, Any
from tools.cppcheck_tool import CppCheckTool

"""
High level manager -> finds the user's tests, runs the tools and copare the bugs that founded with the bugs known by user.

"""
class BenchmarkManager:
    def __init__(self, input_dir_name: str = "src", config_file: str = "expected_results.json"):
        """
        Initialize the manager - calaculates paths relative to the project root
        :param config_file: knowen bugs to be found. Added by the user.
        """
        # current directory - core
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # main folder -> one step back
        self.project_root = os.path.dirname(current_dir)

        # other paths
        self.config_path = os.path.join(self.project_root, "src", "expected_results.json")
        self.src_path = os.path.join(self.project_root, "src")
        self.reports_path = os.path.join(self.project_root, "reports")
        self.tools_path = os.path.join(self.project_root, "tools")
        self.tests_path = os.path.join(self.project_root, "tests")

        # input validation
        self.validate_input()

        # create reports folder if doesn't exist
        os.makedirs(self.reports_path, exist_ok=True)

        # settings file:
        self.ground_truth = self._load_ground_truth()

        # active tools:
        self.active_tools = [CppCheckTool()]

    def validate_input(self):
        """
        Validates input folder and JSON file
        """
        if not os.path.isdir(self.src_path):
            raise FileNotFoundError(f"Input directory not found: {self.src_path}")
        
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Missing configuraton file: {self.config_path}")

        try:
            with open(self.config_path, 'r') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            (f"Invalid JSON format in: {self.config_path}: {e}")

        if "files" not in data or not isinstance(data["files"], list) or len(data["files"]) == 0:
            raise ValueError(f"Invalid configuration: 'files' list is empty or missing.")

    def _load_ground_truth(self) -> Dict:
        """
        Loads the expected bugs configuration from the json file.
        """

        with open(self.config_path, 'r') as f:
            return json.load(f)


    def get_files_to_test(self) -> List[str]:
        """
        Returns a list of verified, full paths to the files that need to be tested in 'src'.
        Returns Objects and not string
        """

        files_config = self.ground_truth.get("files", [])
        verified_files = []

        for item in files_config:
            filename = item["filename"]
            full_path = os.path.join(self.src_path, filename)

            if os.path.exists(full_path):
                verified_files.append({
                    "path": full_path,
                    "filename": filename,
                    "expected_bugs": item.get("bugs", [])
                })
            else:
                print(f"Warning: File defined in JSON but not found: {filename}")
        
        return verified_files
        
        return verified_files
    
    def run_all_tests(self):
        """
        Runs tools and verifies results 
        """

        files_data = self.get_files_to_test()

        # empty folder to test
        if not files_data:
            print("No files found for testing")
            return
        
        print(f"\n--- Starting Benchmark on {len(files_data)} files ---")

        for file_info in files_data:
            file_path = file_info["path"]
            filename = file_info["filename"]
            expected_bugs = file_info["expected_bugs"]

            print(f"\n[File]: {filename}")

            for tool in self.active_tools:
                tool_name = tool.__class__.__name__
                print(f"Runnig {tool_name} ...", end=" ", flush=True)

                try:
                    result = tool.run(file_path)
                    print("DONE.")

                    if isinstance(result, dict) and "bugs" in result:
                        found_bugs = result["bugs"]
                    else: 
                        found_bugs = []
                    
                    self._verify_result(filename, tool_name, found_bugs, expected_bugs)
                          
                except Exception as e:
                    print(f"FAILED.")
                    print(f"Error: {e}")
        
        print("\n--- Benchmark Completed ___")


    def _verify_result(self, filename: str, tool_name: str, found_bugs: List[Dict], expected_bugs: List[Dict]):
        """
        Compares found bugs vs expected bugs and prints a mini-report.
        """

        print(f"[Verification - {tool_name}]")

        expected_count = len(expected_bugs)
        found_count = len(found_bugs) if found_bugs else 0

        if (expected_count == found_count):
            print(f" SUCCESS: Found {found_count} bugs as expected")
        else:
            print(f" MISMATCH: Found {found_count} bugs but expected to find {expected_count}.")
            if found_count > 0:
                 print("[Actual Findings]:")
                 for bug in found_bugs:
                     line = bug.get('line', '?')
                     massage = bug.get('message', 'No message')
                     severity = bug.get('severity', '?')
                     print(f"        - Line {line} [{severity}]: {massage}")