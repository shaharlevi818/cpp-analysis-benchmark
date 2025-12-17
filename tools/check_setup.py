# tools/check_setup.py

import os
import subprocess

def check_environment():
    print("--- Starting Environment Check ---")

    # 1. Check if the target C++ file exists
    file_path = "src/vulnerable.cpp"
    if os.path.exists(file_path):
        print(f"[V] Found target file: {file_path}")
    else:
        print(f"[X] ERROR: Could not find {file_path}. Check folder structure!")

    # 2. Check if CppCheck is installed and accessible
    try:
        # Run a simple version check command
        result = subprocess.run(['cppcheck', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"[V] CppCheck is installed: {result.stdout.strip()}")
        else:
            print(f"[X] CppCheck returned error: {result.stderr}")
    except FileNotFoundError:
        print("[X] ERROR: CppCheck not found via Python (is it installed in Docker?)")

    print("--- Check Finished ---")

if __name__ == "__main__":
    check_environment()