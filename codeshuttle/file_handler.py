import os
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