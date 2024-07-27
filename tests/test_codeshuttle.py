### FILE_PATH: tests/test_codeshuttle.py

import pytest
from io import StringIO
from unittest.mock import patch, mock_open
from codeshuttle import CodeShuttle, Parser, FileHandler, Logger, FileChange

def test_parser():
    parser = Parser()
    input_data = """### FILE_PATH: test.txt
This is the content of test.txt
### FILE_PATH: dir/another.txt
This is the content of another.txt
"""
    expected = [
        FileChange("test.txt", "This is the content of test.txt"),
        FileChange("dir/another.txt", "This is the content of another.txt")
    ]
    assert parser.parse(input_data) == expected

def test_file_handler(tmp_path):
    file_handler = FileHandler()
    changes = [
        FileChange("test.txt", "This is a test file"),
        FileChange("dir/nested.txt", "This is a nested file")
    ]
    file_handler.apply_changes(changes, str(tmp_path))

    assert (tmp_path / "test.txt").read_text() == "This is a test file"
    assert (tmp_path / "dir" / "nested.txt").read_text() == "This is a nested file"

def test_logger():
    logger = Logger()
    with patch('sys.stdout', new=StringIO()) as fake_out:
        logger.log("Test message", "INFO")
        assert "INFO: Test message" in fake_out.getvalue()

@patch('codeshuttle.FileHandler')
@patch('codeshuttle.Parser')
def test_codeshuttle_run(mock_parser, mock_file_handler):
    mock_parser.return_value.parse.return_value = [FileChange("test.txt", "content")]

    shuttle = CodeShuttle()
    with patch.object(shuttle, '_read_input', return_value="mock input"):
        shuttle.run("input.txt", "/root", verbose=True)

    mock_parser.return_value.parse.assert_called_once()
    mock_file_handler.return_value.apply_changes.assert_called_once_with([FileChange("test.txt", "content")], "/root")

@patch('builtins.open', new_callable=mock_open, read_data="input data")
def test_codeshuttle_run_from_file(mock_file):
    with patch('codeshuttle.Parser') as mock_parser, \
            patch('codeshuttle.FileHandler') as mock_file_handler:
        mock_parser.return_value.parse.return_value = [FileChange("test.txt", "content")]

        shuttle = CodeShuttle()
        shuttle.run("input.txt", "/root", verbose=False)

        mock_file.assert_called_once_with("input.txt", "r")
        mock_parser.return_value.parse.assert_called_once_with("input data")
        mock_file_handler.return_value.apply_changes.assert_called_once_with([FileChange("test.txt", "content")], "/root")

if __name__ == "__main__":
    pytest.main()