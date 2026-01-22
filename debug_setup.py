import sys
import traceback

print("--- DIAGNOSTIC START ---")

print("\n1. Testing AnalysisTool (Base Class)...")
try:
    from tools.analysis_tool import AnalysisTool
    print("   Import Success.")
except Exception as e:
    print(f"   FAIL Import: {e}")
    traceback.print_exc()

print("\n2. Testing CppcheckTool...")
try:
    from tools.cppcheck_tool import CppcheckTool
    print("   Import Success.")
    t = CppcheckTool()
    print("   Instantiation Success.")
except Exception as e:
    print(f"   FAIL: {e}")
    traceback.print_exc()

print("\n3. Testing ValgrindTool...")
try:
    from tools.valgrind_tool import ValgrindTool
    print("   Import Success.")
    t = ValgrindTool()
    print("   Instantiation Success.")
except Exception as e:
    print(f"   FAIL: {e}")
    traceback.print_exc()

print("\n4. Testing BuildManager...")
try:
    from core.build_manager import BuildManager
    print("   Import Success.")
    # BuildManager requires a path argument
    b = BuildManager("/app/src") 
    print("   Instantiation Success.")
except Exception as e:
    print(f"   FAIL: {e}")
    traceback.print_exc()

print("\n--- DIAGNOSTIC END ---")
