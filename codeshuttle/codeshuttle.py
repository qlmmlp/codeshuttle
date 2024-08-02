import sys
import pyperclip
from .parser import Parser
from .file_handler import FileHandler
from .logger import Logger

class CodeShuttle:
    def __init__(self):
        self.parser = Parser()
        self.file_handler = FileHandler()
        self.logger = Logger()

    def run(self, input_source: str, root_dir: str, verbose: bool):
        try:
            input_data = self._read_input(input_source)
            changes = self.parser.parse(input_data)
            self.file_handler.apply_changes(changes, root_dir)

            if verbose:
                for change in changes:
                    self.logger.log(f"Applied changes to {change.file_path}")

            self.logger.log("All changes applied successfully")
        except Exception as e:
            self.logger.log(f"Error: {str(e)}", "ERROR")
            sys.exit(1)

    @staticmethod
    def _read_input(input_source: str) -> str:
        if input_source == '-':
            return sys.stdin.read()
        elif input_source == 'pb':
            return pyperclip.paste()
        else:
            with open(input_source, 'r') as f:
                return f.read()