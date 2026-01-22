import pytest
import os
from tools.cppcheck_tool import CppcheckTool

def test_cppcheck_detects_all_issues():
    """
    Integration Test:
    Verifies that CppCheck detects BOTH:
    1. Buffer Overflow (Line 9)
    2. Memory Leak (Line 15 approx)
    """

    tool = CppcheckTool()
    target_file = "src/vulnerable.cpp"

    assert os.path.exists(target_file), "File not found!"

    # run the target file:
    print(f"Running analysis on {target_file}...")
    raw_output = tool.run_analysis(target_file)
    result = tool.parse_output(raw_output)

    assert result["passed"] is False, "Analysis should fail on target file"

    # variables to monitor
    found_overflow = False
    found_leak = False

    # iterate the issues that found:
    for bug in result["bugs"]:
        
        # identify overflow
        if "buffer" in bug and "bounds" in bug:
            found_overflow = True

        if "leak" in bug or "not freed" in bug:
            found_leak = True

    # monitor results -> need to detect both issues
    assert found_overflow == True, "Missed buffer overflow!"
    assert found_leak == True, "Missed memory leak!"
        
