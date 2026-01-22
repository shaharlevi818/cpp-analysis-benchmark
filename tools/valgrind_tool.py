import subprocess
import re
from typing import Dict, Any
from tools.analysis_tool import AnalysisTool

class ValgrindTool(AnalysisTool):
    
    def run_analysis(self, executable_path: str) ->str:
        """
        Runs Valgrind on the given executable file and detects memory leaks
        """

        print(f"[Valgrind] Analyzing: {executable_path}")

        # build commnd = --leak-check=full --track-origins=yes ./my_program
        command = [
            "valgrind",
            "--leak-check=full",
            "--track-origins=yes",
            executable_path
        ]

        try:
            result = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                errors='ignore',
                text=True,
                timeout=20          # limits time
            )

            
            return result.stderr
        
        except subprocess.TimeoutExpired:
            return "TIMEOUT_ERROR"
        except FileNotFoundError:
            return "VALGRING_NOT_INSTALLED"
        except Exception as e:
            return f"GENERAL_ERROR: {str(e)}"
    

    def _parse_output(self, raw_output: str) -> Dict[str, Any]:
        """
        Parses Valgrind raw text output into JSON format.
        """

        bugs = []

        # edge cases:
        if raw_output == "TIMEOUT_ERROR":
            return {"bugs": [{"message": "Execution timed out", "severity": "error", "line": 0}]}
        if raw_output == "VALGRIND_NOT_INSTALLED":
             return {"bugs": [{"message": "Valgrind not installed", "severity": "critical", "line": 0}]}
        if raw_output.startswith("GENERAL_ERROR"):
             return {"bugs": [{"message": raw_output, "severity": "error", "line": 0}]}
        
        # patterns to search in valgrind's raw_output
        patterns = [
            (r"definitely lost: ([0-9,]+) bytes", "Memory Leak (Definitely Lost)"),
            (r"indirectly lost: ([0-9,]+) bytes", "Memory Leak (Indirectly Lost)"),
            (r"Invalid read of size", "Invalid Memory Read"),
            (r"Invalid write of size", "Invalid Memory Write"),
            (r"Mismatched free", "Mismatched Free/Delete")
        ]

        for line in raw_output.splitlines():
            for pattern, error_type in patterns:
                match = re.search(pattern, line)
                if match:
                    # error found:

                    # regex catch bytes 0 as an error -> if 0 bytes lost -> skip
                    if "lost" in error_type.lower():        
                        bytes_lost_str = match.group(1).replace(',','')
                        if int(bytes_lost_str) == 0:
                            continue # skip if leak is 0
                    bugs.append({
                        "message": f"{error_type}: {line.strip()}",
                        "severity": "error",
                        "line": 0,          # for now, line = 0
                        "type": "memory_leak"
                    })
                    break

        return {"bugs": bugs}
    



