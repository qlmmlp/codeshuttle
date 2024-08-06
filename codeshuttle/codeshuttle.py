### FILE_PATH: codeshuttle/codeshuttle.py
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

    def apply_changes(self, input_source: str, root_dir: str, verbose: bool, output_file: str = None, dry_run: bool = False):
        try:
            if not os.path.exists(root_dir):
                raise OSError(f"Root directory '{root_dir}' does not exist.")
            if not os.access(root_dir, os.W_OK):
                raise OSError(f"Root directory '{root_dir}' is not writable.")

            input_data = self._read_input(input_source)
            changes = self.parser.parse(input_data)

            # Convert file paths to be relative to root_dir
            for change in changes:
                change.file_path = os.path.relpath(change.file_path, root_dir)

            if dry_run:
                self._preview_changes(changes)
            else:
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

    def collect_files(self, output_file: str, root_dir: str, pattern_file: str = None, dry_run: bool = False, verbose: bool = False):
        try:
            files_to_collect = self.file_handler.get_files_to_collect(root_dir, pattern_file)

            if dry_run:
                self._preview_collection(files_to_collect)
            else:
                collected_content = self.file_handler.collect_file_contents(files_to_collect, root_dir)
                self._write_collected_content(collected_content, output_file, root_dir)

                if verbose:
                    self.logger.log(f"Collected {len(files_to_collect)} files")
                    self.logger.log(f"Written collected content to {output_file}")

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
                with open(input_source, 'r', encoding='utf-8') as f:
                    return f.read()
            except IOError as e:
                raise IOError(f"Error reading input file '{input_source}': {str(e)}")

    @staticmethod
    def _write_applied_changes(changes, output_file: str):
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                for change in changes:
                    f.write(f"### FILE_PATH: {change.file_path}\n")
                    f.write(f"{change.content}\n\n")
        except IOError as e:
            raise IOError(f"Error writing to output file '{output_file}': {str(e)}")

    @staticmethod
    def _preview_changes(changes):
        for change in changes:
            print(f"Would apply changes to: {change.file_path}")
            print(f"Content:\n{change.content}\n")

    @staticmethod
    def _preview_collection(files):
        print("Files that would be collected:")
        for file in files:
            print(f"  {file}")

    def _write_collected_content(self, content, output_file: str, root_dir: str):
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"# Root directory: {os.path.abspath(root_dir)}\n\n")
                f.write(content)
        except IOError as e:
            raise IOError(f"Error writing to output file '{output_file}': {str(e)}")