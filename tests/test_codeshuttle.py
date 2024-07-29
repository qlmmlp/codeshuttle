import pytest
from io import StringIO
from unittest.mock import patch, mock_open, call, MagicMock
from codeshuttle.codeshuttle import CodeShuttle, Parser, FileHandler, Logger, FileChange

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

def test_codeshuttle_run():
    mock_parser = MagicMock(spec=Parser)
    mock_file_handler = MagicMock(spec=FileHandler)
    mock_logger = MagicMock(spec=Logger)

    mock_parser.parse.return_value = [FileChange("test.txt", "content")]

    shuttle = CodeShuttle()
    shuttle.parser = mock_parser
    shuttle.file_handler = mock_file_handler
    shuttle.logger = mock_logger

    with patch.object(shuttle, '_read_input', return_value="mock input") as mock_read_input:
        shuttle.run("input.txt", "/root", verbose=True)

    print(f"Mock parser calls: {mock_parser.mock_calls}")
    print(f"Mock file handler calls: {mock_file_handler.mock_calls}")
    print(f"Mock read input calls: {mock_read_input.mock_calls}")

    mock_read_input.assert_called_once_with("input.txt")
    mock_parser.parse.assert_called_once_with("mock input")
    mock_file_handler.apply_changes.assert_called_once_with([FileChange("test.txt", "content")], "/root")

def test_codeshuttle_run_from_file():
    mock_parser = MagicMock(spec=Parser)
    mock_file_handler = MagicMock(spec=FileHandler)
    mock_logger = MagicMock(spec=Logger)

    mock_parser.parse.return_value = [FileChange("test.txt", "content")]

    shuttle = CodeShuttle()
    shuttle.parser = mock_parser
    shuttle.file_handler = mock_file_handler
    shuttle.logger = mock_logger

    with patch('builtins.open', new_callable=mock_open, read_data="input data"):
        shuttle.run("input.txt", "/root", verbose=False)

    print(f"Mock parser calls: {mock_parser.mock_calls}")
    print(f"Mock file handler calls: {mock_file_handler.mock_calls}")

    mock_parser.parse.assert_called_once_with("input data")
    mock_file_handler.apply_changes.assert_called_once_with([FileChange("test.txt", "content")], "/root")

if __name__ == "__main__":
    pytest.main()