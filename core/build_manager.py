import os
import subprocess
import shutil
from typing import List

class BuildManager:
    """
    Responsible for compiling the C++ project using CMake.
    """
    def __init__(self, src_path: str, build_dir_name: str = "build"):
        self.src_path = src_path
        # Build folder will be inside the main project folder.
        self.project_root = os.path.dirname(src_path) 
        self.build_path = os.path.join(self.project_root, build_dir_name)

    def clean_build(self):
        """
        Removes the build directory to ensure a fresh start.
        """
        if os.path.exists(self.build_path):
            print(f"Cleaning old build directory: {self.build_path}")
            shutil.rmtree(self.build_path)

    def run_build(self) -> bool:
        """
        Runs the CMake build process.
        """
        print("\n--- Starting Build Process ---")
        
        # create new folder
        os.makedirs(self.build_path, exist_ok=True)

        try:
            # run CMake configuration
            print("Configuring project with CMake...")
            subprocess.run(
                ["cmake", "-S", self.src_path, "-B", self.build_path], 
                check=True, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE
            )

            # compile
            print("Compiling project...")
            subprocess.run(
                ["cmake", "--build", self.build_path], 
                check=True, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE
            )
            
            print("Build completed successfully!")
            return True

        except subprocess.CalledProcessError as e:
            print(f"Build Failed!")
            if e.stderr:
                print(f"Error details:\n{e.stderr.decode()}")
            return False

    def get_executables(self) -> List[str]:
        """
        Scans the build directory and prints everything it finds (Debug Mode).
        """
        executables = []

        if not os.path.exists(self.build_path):
            return []

        for root, dirs, files in os.walk(self.build_path):
            # skip inner folders of CMake 
            if "CMakeFiles" in root:
                continue
            
            for file in files:
                full_path = os.path.join(root, file)
                
                # check if file is exe file
                is_exe = os.access(full_path, os.X_OK)
                is_cmake = file.endswith(".cmake") or file.endswith(".txt")
                is_makefile = (file == "Makefile")

                if is_exe and not is_cmake and not is_makefile:
                    executables.append(full_path)
        
        return executables
