import pytest
from unittest.mock import MagicMock, patch
from chess_puzzle_ai_cli.chess_puzzle_ai_cli import main
import io

@pytest.fixture
def mock_puzzle_data():
    return {
        'game': {'pgn': '1. d4 Nf6 2. c4 e6 3. Nc3 Bb4'},
        'puzzle': {'initialPly': 2, 'solution': ['c7c5', 'd7d5']}
    }

@pytest.fixture
def mock_fetch_daily_puzzle(mock_puzzle_data):
    with patch('chess_puzzle_ai_cli.puzzle_fetcher.fetch_daily_puzzle', return_value=mock_puzzle_data) as mock:
        yield mock

@pytest.fixture
def mock_subprocess_popen():
    with patch('subprocess.Popen') as mock:
        yield mock

@pytest.fixture
def mock_application_run():
    with patch('prompt_toolkit.Application.run') as mock:
        yield mock

import sys
import pytest
from unittest.mock import MagicMock, patch
from chess_puzzle_ai_cli.chess_puzzle_ai_cli import main
import io

@pytest.fixture
def mock_puzzle_data():
    return {
        'game': {'pgn': '1. d4 Nf6 2. c4 e6 3. Nc3 Bb4'},
        'puzzle': {'initialPly': 2, 'solution': ['c7c5', 'd7d5']}
    }

@pytest.fixture
def mock_fetch_daily_puzzle(mock_puzzle_data):
    with patch('chess_puzzle_ai_cli.puzzle_fetcher.fetch_daily_puzzle', return_value=mock_puzzle_data) as mock:
        yield mock

@pytest.fixture
def mock_subprocess_popen():
    with patch('subprocess.Popen') as mock:
        yield mock

@pytest.fixture
def mock_application_run():
    with patch('prompt_toolkit.Application.run') as mock:
        yield mock

def test_user_input_does_not_crash_program(mock_fetch_daily_puzzle, mock_subprocess_popen, mock_application_run):
    # Simulate user input that might cause a crash (e.g., an invalid move format)
    user_inputs = ["invalid_move", "e2e4", "exit"]
    input_iter = iter(user_inputs)

    def mock_handle_input(buffer):
        try:
            buffer.text = next(input_iter)
        except StopIteration:
            buffer.text = "exit" # Ensure exit if inputs run out
        buffer.validate_and_handle()

    with patch('prompt_toolkit.widgets.TextArea.accept_handler', new=mock_handle_input):
        with patch('sys.argv', ['chess-puzzle-ai-cli']): # Mock sys.argv to prevent argparse errors
            try:
                main()
            except Exception as e:
                pytest.fail(f"Program crashed with exception: {e}")

    # Assert that the application was run (and ideally exited gracefully)
    mock_application_run.assert_called_once()
