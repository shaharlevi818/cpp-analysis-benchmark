import pytest
from tools.cppcheck_tool import CppcheckTool

"""
Assuming that CppCheck is working properly, this test will check that the logic works. 
this test file will check whether parse_output from the cppcheck_tool.py file works as required. 
Whether the code in the test tool that checks CppCheck works correctly.
"""

def test_parse_cppcheck_error():
    """
    Test scenario: CppCheck finds a real error.
    Input: fake string that looks exactly like CppCheck output
    Expected Result: passed=False, bugs count=1
    """

    tool = CppcheckTool()
    fake_output = "src/vulnerable.cpp:9:error:Array 'buffer[10]' accessed at index 12."
    
    # The fake output is passed to the function under test.
    # tool.parse_output returns: result = {{"passed" : True/False}, {"bugs" : [[Line {line_number}] [{severity.upper()}]: {message}"]]}} where severity = 'erorr'/'warning'
    result = tool.parse_output(fake_output)

    assert result["passed"] is False, "Should fail when error is present"
    assert len(result["bugs"]) == 1, "Should identify exactly 1 bug"
    assert "[ERROR]" in result["bugs"][0], "Should identify as an ERROR"           # the bug is an ERROR and not a WARNING
    assert "Array 'buffer[10]'" in result["bugs"][0]

def test_parse_clean_output():
    """
    Test scenario: Code is clean.
    Input: Empty string.
    Expected Result: passed=True, bugs count=0
    """
    tool = CppcheckTool()
    fake_output = ""
    result = tool.parse_output(fake_output)

    assert result["passed"] is True, "Should pass when output is empty"
    assert len(result["bugs"]) == 0, "Should have 0 bugs"


def test_ignore_style_issues():
    """
    Test scenario: CppCheck finds a 'style' issue (not critical).
    The parser should IGNORE it because it's not 'error' or 'warning'.
    """
    tool = CppcheckTool()
    fake_output = "src/file.cpp:5:style:Variable 'x' is assigned a value that is never used."
    
    result = tool.parse_output(fake_output)
    
    assert result["passed"] is True
    assert len(result["bugs"]) == 0