# tools/base_tool.py

import subprocess
import os
from typing import Any, Dict
from abc import ABC, abstractmethod


class AnalysisTool(ABC):
    """
    An Abstract Base Class for every code analysis tool.
    Every tool (like CppCheck, Valgrind) will inherit from this class and implement the functions.
    """

    def __init__(self, name):
        self.name = name

    def run(self, file_path: str) -> Dict[str, Any]:
        """
        The main public method.
        Orchestrates the process:
        1. Runs the analysis command.
        2. Parses the output.
        Returns the clean, structured result.
        """
        raw_output = self.run_analysis(file_path)
        return self.parse_output(raw_output)

    @abstractmethod
    def run_analysis(self, file_path: str):
        """
        Abstract function: Must be implemented by every tool.
        Gets a path to a file and runs the tool on it.
        """
        pass

    @abstractmethod
    def parse_output(self, raw_output: str):
        """
        Abstract function: Decodes the raw output of the tool
        and returns an ordered data structure (e.g. a dictionary or boolean).
        """
        pass

    def execute_command(self, command: list) -> str:
        """
        A helper function for running Linux commands (Shell Commands).
        Accepts a list of words (e.g. ['ls', '-l']) and returns the output as a string.
        """
        try:
            """
            subprocess.run: The modern Python command for running external processes
            capture_output=True: Captures what the tool printed (stdout/stderr) instead of throwing it to the screen
            text=True: Converts the result from bytes (binary) to string (human-readable text)
            """
            result = subprocess.run(command, capture_output=True, text=True, check=False)
            
            # Returns both the standard output and errors (if any)
            return result.stdout + result.stderr
        except Exception as e:
            return f"Error executing command: {str(e)}"