### FILE_PATH: codeshuttle/__init__.py
from .codeshuttle import CodeShuttle
from .file_change import FileChange
from .parser import Parser
from .file_handler import FileHandler
from .logger import Logger

__version__ = "0.2.0"  # Update this version number as needed

__all__ = ['CodeShuttle', 'FileChange', 'Parser', 'FileHandler', 'Logger', '__version__']