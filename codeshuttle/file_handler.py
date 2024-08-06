### FILE_PATH: codeshuttle/file_handler.py
import os
import fnmatch
from typing import List
from .file_change import FileChange

class FileHandler:
    @staticmethod
    def apply_changes(changes: List[FileChange], root_dir: str):
        for change in changes:
            full_path = os.path.join(root_dir, change.file_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(change.content)

    @staticmethod
    def get_files_to_collect(root_dir: str, scope_file: str = None) -> List[str]:
        if scope_file is None:
            # Default behavior: collect only files from the root directory
            return [f for f in os.listdir(root_dir) if os.path.isfile(os.path.join(root_dir, f))]

        patterns = ['*']  # Default to collecting all files if scope file is empty

        if os.path.exists(scope_file):
            with open(scope_file, 'r', encoding='utf-8') as f:
                patterns = [line.strip() for line in f if line.strip() and not line.startswith('#')]

        files_to_collect = []
        for root, _, files in os.walk(root_dir):
            for file in files:
                file_path = os.path.relpath(os.path.join(root, file), root_dir)
                if any(fnmatch.fnmatch(file_path, pattern) for pattern in patterns):
                    files_to_collect.append(file_path)

        return files_to_collect

    @staticmethod
    def collect_file_contents(files: List[str], root_dir: str) -> str:
        collected_content = ""
        for file in files:
            try:
                full_path = os.path.join(root_dir, file)
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    collected_content += f"### FILE_PATH: {file}\n{content}\n\n"
            except IOError as e:
                print(f"Warning: Could not read file {file}: {str(e)}")
        return collected_content