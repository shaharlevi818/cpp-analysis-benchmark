# tools/cppcheck_tool.py

import subprocess
import xml.etree.ElementTree as ET
from typing import Dict, Any
from tools.analysis_tool import AnalysisTool


class CppcheckTool(AnalysisTool):
    """
    Implementation of the AnalysisTool for CppCheck.
    Static analysis
    """

    def run_analysis(self, file_path: str) -> str:
        print(f"[Cppcheck] Analyzing: {file_path}")
        # --subprocess=missingIncludeSystem for exclude information notifications
        command = ["cppcheck", "--enable=all", "--xml", file_path]

        try:
            result = subprocess.run(
            command, 
            stderr=subprocess.PIPE, 
            stdout=subprocess.DEVNULL, 
            text=True
            )            
            return result.stderr
        except FileNotFoundError:
            return "CPPCHECK_NOT_INSTALLED"
        except Exception as e:
            return f"GENERAL_ERROR: {str(e)}"
    
    def _parse_output(self, raw_output: str) -> Dict[str, Any]:
        
        if raw_output == "CPPCHECK_NOT_INSTALLED":
            return {"bugs": [{"message": "Cppcheck not installed", "severity": "critical", "line": 0}]}
        if raw_output.startswith("GENERAL_ERROR"):
            return {"bugs": [{"message": raw_output, "severity": "error", "line": 0}]}
        
        bugs = []
        
        try:
            root = ET.fromstring(raw_output)
            for error in root.findall(".//error"):
                severity = error.get("severity", "unknown")
                if severity == "information":
                    continue        # information notification not consider as an error
                bugs.append({
                    "message": error.get("msg", "Unknown error"),
                    "severity": error.get("severity", "unknown"),
                    "line": int(error.find("location").get("line")) if error.find("location") is not None else 0,
                    "type": error.get("id", "unknown")
                })
        except ET.ParseError:
             return {"bugs": []}
             
        return {"bugs": bugs}



        
        

    