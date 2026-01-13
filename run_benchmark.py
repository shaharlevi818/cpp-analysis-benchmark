import sys
import os

sys.path.append(os.getcwd())

from core.benchmark_manager import BenchmarkManager

if __name__ == "__main__":
    try:
        manager = BenchmarkManager()
        print(f"Project Root detected as: {manager.project_root}")

        # # for testing - start
        # files = manager.get_files_to_test()
        # print("\nFiles found for testing:")

        # for file in files:
        #     print(f" - {file}")

        # # for testing - end

        manager.run_all_tests()

    except Exception as e:
        print(f"Critical Error - {e}")

