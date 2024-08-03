import sys
import os
import pyperclip
from .parser import Parser
from .file_handler import FileHandler
from .logger import Logger

class CodeShuttle:
    def __init__(self):
        self.parser = Parser()
        self.file_handler = FileHandler()
        self.logger = Logger()

    def run(self, input_source: str, root_dir: str, verbose: bool, output_file: str = None):
        try:
            # Check if root directory exists and is writable
            if not os.path.exists(root_dir):
                raise OSError(f"Root directory '{root_dir}' does not exist.")
            if not os.access(root_dir, os.W_OK):
                raise OSError(f"Root directory '{root_dir}' is not writable.")

            input_data = self._read_input(input_source)
            changes = self.parser.parse(input_data)
            self.file_handler.apply_changes(changes, root_dir)

            if verbose:
                for change in changes:
                    self.logger.log(f"Applied changes to {change.file_path}")

            if output_file:
                self._write_applied_changes(changes, output_file)
                self.logger.log(f"Written applied changes to {output_file}")

            self.logger.log("All changes applied successfully")
        except OSError as e:
            raise OSError(f"File system error: {str(e)}")
        except Exception as e:
            raise Exception(f"An unexpected error occurred: {str(e)}")

    @staticmethod
    def _read_input(input_source: str) -> str:
        if input_source == '-':
            return sys.stdin.read()
        elif input_source == 'pb':
            return pyperclip.paste()
        else:
            try:
                with open(input_source, 'r') as f:
                    return f.read()
            except IOError as e:
                raise IOError(f"Error reading input file '{input_source}': {str(e)}")

    @staticmethod
    def _write_applied_changes(changes, output_file: str):
        try:
            with open(output_file, 'w') as f:
                for change in changes:
                    f.write(f"### FILE_PATH: {change.file_path}\n")
                    f.write(f"{change.content}\n\n")
        except IOError as e:
            raise IOError(f"Error writing to output file '{output_file}': {str(e)}")