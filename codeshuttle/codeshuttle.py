### FILE_PATH: codeshuttle/codeshuttle.py

import sys
import os
from typing import List

class FileChange:
    def __init__(self, file_path: str, content: str):
        self.file_path = file_path
        self.content = content

    def __eq__(self, other):
        if not isinstance(other, FileChange):
            return NotImplemented
        return self.file_path == other.file_path and self.content == other.content

    def __repr__(self):
        return f"FileChange(file_path='{self.file_path}', content='{self.content}')"

class Parser:
    def parse(self, input_data: str) -> List[FileChange]:
        changes = []
        lines = input_data.split('\n')
        current_file = None
        current_content = []

        for line in lines:
            if line.startswith("### FILE_PATH: "):
                if current_file:
                    changes.append(FileChange(current_file, '\n'.join(current_content).strip()))
                current_file = line.split(": ", 1)[1]
                current_content = []
            elif current_file is not None:
                current_content.append(line)

        if current_file:
            changes.append(FileChange(current_file, '\n'.join(current_content).strip()))

        return changes

class FileHandler:
    def apply_changes(self, changes: List[FileChange], root_dir: str):
        for change in changes:
            full_path = os.path.join(root_dir, change.file_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, 'w') as f:
                f.write(change.content)

class Logger:
    def log(self, message: str, level: str):
        print(f"{level}: {message}")

class CodeShuttle:
    def __init__(self):
        self.parser = Parser()
        self.file_handler = FileHandler()
        self.logger = Logger()

    def run(self, input_source: str, root_dir: str, verbose: bool):
        input_data = self._read_input(input_source)
        try:
            changes = self.parser.parse(input_data)
            self.file_handler.apply_changes(changes, root_dir)

            if verbose:
                for change in changes:
                    self.logger.log(f"Applied changes to {change.file_path}", "INFO")

            self.logger.log("All changes applied successfully", "INFO")
        except Exception as e:
            self.logger.log(f"Error: {str(e)}", "ERROR")
            sys.exit(1)

    def _read_input(self, input_source: str) -> str:
        if input_source == '-':
            return sys.stdin.read()
        else:
            with open(input_source, 'r') as f:
                return f.read()

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Apply code changes based on a specified format.")
    parser.add_argument("--input", help="Input file path (use '-' for stdin)", required=True)
    parser.add_argument("--root", help="Root directory for applying changes", default=".")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    shuttle = CodeShuttle()
    shuttle.run(args.input, args.root, args.verbose)

if __name__ == "__main__":
    main()