from dataclasses import dataclass

@dataclass
class FileChange:
    file_path: str
    content: str