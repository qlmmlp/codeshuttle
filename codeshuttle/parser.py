from typing import List
from .file_change import FileChange

class Parser:
    @staticmethod
    def parse(input_data: str) -> List[FileChange]:
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