# tools/cppcheck_tool.py

from tools.base_tool import AnalysisTool

class CppCheckTool(AnalysisTool):
    """
    Implementation of the AnalysisTool for CppCheck.
    Static analysis
    """

    def __init__(self):
        super().__init__("CppCheck");

    def run_analysis(self, file_path: str) -> str:
        command = ['cppcheck',                                              
                   '--enable=all',                                          # Enable all checks
                   '--inconclusive',                                        # Report even if the analysis is not 100% sure
                   '--template={file}:{line}:{severity}:{message}',         # Format for the report for easy parsing
                    file_path
        ]

        return self.execute_command(command)
    
    def parse_output(self, raw_output: str) -> dict:
        bugs = []
        lines = raw_output.split('\n')                                      # line = {file}:{line}:{severity}:{message}
        for line in lines:
            parts = line.split(':')

            # validation to ensure processing a valid error line
            if len(parts) >= 4:
                file_name = parts[0]
                line_number = parts[1]
                severity = parts[2]
                message = ":".join(parts[3:])                                   # incase message has colons
            
                if severity in ['error', 'warning']:                                # error and warning are also failures, append them to bugs.
                    bug_details = { 
                        "line": int(line_number),
                        "severity": severity,
                        "message": message.strip()
                    }
                    bugs.append(bug_details)

        return {
            "passed" : len(bugs) == 0,                                        # pass only if o bugs found
            "bugs" : bugs
        }    



        
        

    