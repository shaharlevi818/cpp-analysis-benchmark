from core.benchmark_manager import BenchmarkManager

def main():
    manager = BenchmarkManager()
    try:
        executables = manager.build_project()
        print("\nFound executables:")
        for exe in executables:
            print(f" - {exe}")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()