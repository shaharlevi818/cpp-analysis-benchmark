from abc import ABC, abstractmethod
from typing import Dict, Any

class AnalysisTool(ABC):
    
    def run(self, file_path: str) -> Dict[str, Any]:
        """
        Template method that executes the full analysis flow.
        """
        # 1. Run the specific tool command -> returns string.
        raw_output = self.run_analysis(file_path)
        
        # 2. Parse the output using the internal method
        return self._parse_output(raw_output)

    @abstractmethod
    def run_analysis(self, file_path: str) -> str:
        """
        Abstract method: Must run the tool and return raw output (string).
        """
        pass

    @abstractmethod
    def _parse_output(self, output: str) -> Dict[str, Any]:
        """
        Abstract method: Must parse the raw output into a standard JSON format.
        """
        pass