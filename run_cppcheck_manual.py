# run_cppcheck_manual.py

import os
from tools.cppcheck_tool import CppcheckTool


"""
    Saves the analysis results to files in the 'reports' directory.
"""
def save_report(tool_name, file_name, result):
    
    # Create filenames
    base_name = os.path.basename(file_name)
    status_file = f"reports/status_{tool_name}_{base_name}.txt"
    log_file = f"reports/log_{tool_name}_{base_name}.txt"
    
    # Save boolean status
    with open(status_file, "w") as sf:
        status = "PASSED" if result['passed'] else "BUG_DETECTED"
        # sf.write(f"--- Status Report for {tool_name} --- \n")
        # sf.write(f"File: {file_name}\n\n")
        sf.write(status)
    print(f"[+] Created status file: {status_file}")

    # Save log
    with open(log_file, "w") as lf:
        lf.write(f"--- Analysis Report for {tool_name} --- \n")
        lf.write(f"File: {file_name}\n\n")

        if result['passed']:
            lf.write("No bugs found.\n")
        else:
            lf.write(f"Found {len(result['bugs'])} issues:\n")
            for bug in result['bugs']:
                line = bug['line']
                severity = bug['severity'].upper()
                massage = bug['massage']
                lf.write(f"[Line {line}][{severity}]: {massage}\n")
        
        print(f"[+] Created log file: {log_file}")

def main():
    target_file = "src/vulnerable.cpp"
    tool = CppcheckTool()
    print(f"Running {tool.name} on {target_file}...")

    # Run analysis
    raw_output = tool.run_analysis(target_file)

    # Parse output
    parsed_result = tool.parse_output(raw_output)

    # Save reports
    save_report(tool.name, target_file, parsed_result)

    # Console output for verification
    print("\n--- Summary ---\n")
    print(f"Did code pass? {parsed_result['passed']}")
    print(f"Bugs founs: {parsed_result['bugs']}")

if __name__ == "__main__":
    main()


