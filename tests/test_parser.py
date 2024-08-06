import pytest
from io import StringIO
from unittest.mock import patch, mock_open, call, MagicMock
from codeshuttle.codeshuttle import CodeShuttle, Parser, FileHandler, Logger, FileChange

def test_parse_valid_input():
    parser = Parser()
    input_data = """### FILE_PATH: file1.py
print("Hello, World!")

### FILE_PATH: file2.py
def greet(name):
    return f"Hello, {name}!"
"""
    changes = parser.parse(input_data)

    assert len(changes) == 2
    assert isinstance(changes[0], FileChange)
    assert isinstance(changes[1], FileChange)

    assert changes[0].file_path == "file1.py"
    assert changes[0].content == 'print("Hello, World!")'

    assert changes[1].file_path == "file2.py"
    assert changes[1].content == 'def greet(name):\n    return f"Hello, {name}!"'