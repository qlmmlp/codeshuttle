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
            with open(full_path, 'w') as f:
                f.write(change.content)

    @staticmethod
    def get_files_to_collect(root_dir: str, pattern_file: str = None) -> List[str]:
        include_patterns = ['*']
        exclude_patterns = []

        if pattern_file:
            with open(pattern_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('!'):
                        exclude_patterns.append(line[1:])
                    else:
                        include_patterns.append(line)

        files_to_collect = []
        for root, _, files in os.walk(root_dir):
            for file in files:
                file_path = os.path.relpath(os.path.join(root, file), root_dir)
                if any(fnmatch.fnmatch(file_path, pattern) for pattern in include_patterns) and \
                        not any(fnmatch.fnmatch(file_path, pattern) for pattern in exclude_patterns):
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