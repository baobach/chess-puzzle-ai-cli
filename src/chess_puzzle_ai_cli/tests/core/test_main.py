import pytest
from unittest.mock import patch
from chess_puzzle_ai_cli.__main__ import main


def test_main_parses_arguments():
    with patch('argparse.ArgumentParser.parse_args') as mock_parse_args:
        # Configure the mock to return specific arguments
        mock_parse_args.return_value.clock_file = "/tmp/test_clock.txt"
        mock_parse_args.return_value.status_file = "/tmp/test_status.txt"

        with patch('chess_puzzle_ai_cli.utils.logging.log.info') as mock_log_info:
            # Call the main function
            with patch('prompt_toolkit.application.Application.run'):
                main()

            # Assert that the log.info was called with the correct arguments
            mock_log_info.assert_any_call("Received clock_file: /tmp/test_clock.txt")
            mock_log_info.assert_any_call("Received status_file: /tmp/test_status.txt")
