import pytest
from unittest.mock import patch
from chess_puzzle_ai_cli.__main__ import main


def test_main_parses_arguments(tmp_path):
    clock_file = tmp_path / "clock.txt"
    status_file = tmp_path / "status.txt"
    clock_file.write_text("0.0")
    status_file.touch()

    with patch('argparse.ArgumentParser.parse_args') as mock_parse_args:
        # Configure the mock to return specific arguments
        mock_parse_args.return_value.clock_file = str(clock_file)
        mock_parse_args.return_value.status_file = str(status_file)

        with patch('chess_puzzle_ai_cli.utils.logging.log.info') as mock_log_info:
            # Call the main function
            with patch('prompt_toolkit.application.Application.run'):
                main()

            # Assert that the log.info was called with the correct arguments
            mock_log_info.assert_any_call(f"Received clock_file: {str(clock_file)}")
            mock_log_info.assert_any_call(f"Received status_file: {str(status_file)}")
