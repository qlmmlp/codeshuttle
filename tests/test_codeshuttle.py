### FILE_PATH: tests/test_codeshuttle.py
import pytest
import os
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

@patch('os.path.exists', return_value=True)
@patch('os.access', return_value=True)
def test_codeshuttle_apply_changes(mock_access, mock_exists):
    mock_parser = MagicMock(spec=Parser)
    mock_file_handler = MagicMock(spec=FileHandler)
    mock_logger = MagicMock(spec=Logger)

    mock_parser.parse.return_value = [FileChange("test.txt", "content")]

    shuttle = CodeShuttle()
    shuttle.parser = mock_parser
    shuttle.file_handler = mock_file_handler
    shuttle.logger = mock_logger

    with patch.object(shuttle, '_read_input', return_value="mock input") as mock_read_input:
        shuttle.apply_changes("input.txt", "/root", verbose=True)

    mock_read_input.assert_called_once_with("input.txt")
    mock_parser.parse.assert_called_once_with("mock input")
    mock_file_handler.apply_changes.assert_called_once_with([FileChange("test.txt", "content")], "/root")
    mock_logger.log.assert_called_with("All changes applied successfully")

@patch('os.path.exists', return_value=True)
@patch('os.access', return_value=True)
def test_codeshuttle_apply_changes_dry_run(mock_access, mock_exists):
    mock_parser = MagicMock(spec=Parser)
    mock_file_handler = MagicMock(spec=FileHandler)
    mock_logger = MagicMock(spec=Logger)

    mock_parser.parse.return_value = [FileChange("test.txt", "content")]

    shuttle = CodeShuttle()
    shuttle.parser = mock_parser
    shuttle.file_handler = mock_file_handler
    shuttle.logger = mock_logger

    with patch.object(shuttle, '_read_input', return_value="mock input"), \
            patch.object(shuttle, '_preview_changes') as mock_preview:
        shuttle.apply_changes("input.txt", "/root", verbose=True, dry_run=True)

    mock_preview.assert_called_once_with([FileChange("test.txt", "content")])
    mock_file_handler.apply_changes.assert_not_called()

def test_codeshuttle_collect_files():
    mock_file_handler = MagicMock(spec=FileHandler)
    mock_logger = MagicMock(spec=Logger)

    mock_file_handler.get_files_to_collect.return_value = ["file1.txt", "file2.txt"]
    mock_file_handler.collect_file_contents.return_value = "collected content"

    shuttle = CodeShuttle()
    shuttle.file_handler = mock_file_handler
    shuttle.logger = mock_logger

    with patch('builtins.open', mock_open()) as mock_file:
        with patch('os.path.abspath', return_value="/absolute/root"):
            shuttle.collect_files("output.txt", "/root", verbose=True)

    mock_file_handler.get_files_to_collect.assert_called_once_with("/root", None)
    mock_file_handler.collect_file_contents.assert_called_once_with(["file1.txt", "file2.txt"], "/root")
    mock_file().write.assert_has_calls([
        call("# Root directory: /absolute/root\n\n"),
        call("collected content")
    ])
    mock_logger.log.assert_has_calls([
        call("Collected 2 files"),
        call("Written collected content to output.txt")
    ])

def test_codeshuttle_collect_files_dry_run():
    mock_file_handler = MagicMock(spec=FileHandler)
    mock_logger = MagicMock(spec=Logger)

    mock_file_handler.get_files_to_collect.return_value = ["file1.txt", "file2.txt"]

    shuttle = CodeShuttle()
    shuttle.file_handler = mock_file_handler
    shuttle.logger = mock_logger

    with patch.object(shuttle, '_preview_collection') as mock_preview:
        shuttle.collect_files("output.txt", "/root", dry_run=True)

    mock_preview.assert_called_once_with(["file1.txt", "file2.txt"])
    mock_file_handler.collect_file_contents.assert_not_called()

@patch('os.path.exists', return_value=True)
@patch('os.access', return_value=True)
def test_codeshuttle_apply_changes_with_output_file(mock_access, mock_exists):
    mock_parser = MagicMock(spec=Parser)
    mock_file_handler = MagicMock(spec=FileHandler)
    mock_logger = MagicMock(spec=Logger)

    mock_parser.parse.return_value = [
        FileChange("test1.txt", "content1"),
        FileChange("test2.txt", "content2")
    ]

    shuttle = CodeShuttle()
    shuttle.parser = mock_parser
    shuttle.file_handler = mock_file_handler
    shuttle.logger = mock_logger

    mock_output = mock_open()
    with patch('builtins.open', mock_output):
        with patch.object(shuttle, '_read_input', return_value="mock input"):
            shuttle.apply_changes("input.txt", "/root", verbose=False, output_file="output.txt")

    mock_output.assert_called_with("output.txt", "w", encoding='utf-8')
    handle = mock_output()
    handle.write.assert_has_calls([
        call("### FILE_PATH: test1.txt\n"),
        call("content1\n\n"),
        call("### FILE_PATH: test2.txt\n"),
        call("content2\n\n")
    ])

if __name__ == "__main__":
    pytest.main()