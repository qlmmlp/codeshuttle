import pytest
from io import StringIO
from unittest.mock import patch
from codeshuttle.codeshuttle import Logger

@pytest.fixture
def logger():
    return Logger()

def test_log_info(logger):
    with patch('sys.stdout', new=StringIO()) as fake_out:
        logger.log("Test info message")
        assert fake_out.getvalue().strip() == "INFO: Test info message"

def test_log_error(logger):
    with patch('sys.stdout', new=StringIO()) as fake_out:
        logger.log("Test error message", "ERROR")
        assert fake_out.getvalue().strip() == "ERROR: Test error message"

def test_log_custom_level(logger):
    with patch('sys.stdout', new=StringIO()) as fake_out:
        logger.log("Test custom message", "CUSTOM")
        assert fake_out.getvalue().strip() == "CUSTOM: Test custom message"

def test_log_empty_message(logger):
    with patch('sys.stdout', new=StringIO()) as fake_out:
        logger.log("")
        assert fake_out.getvalue().strip() == "INFO:"