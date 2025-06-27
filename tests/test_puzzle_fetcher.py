import unittest
from unittest.mock import patch
import requests
from chess_puzzle_ai_cli.puzzle_fetcher import fetch_daily_puzzle

class TestPuzzleFetcher(unittest.TestCase):

    @patch('requests.get')
    def test_fetch_daily_puzzle_success(self, mock_get):
        """
        Test that fetch_daily_puzzle successfully fetches and returns puzzle data.
        """
        # Mock the response from requests.get
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "puzzle": {
                "id": "test_id",
                "fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
                "solution": ["e2e4", "e7e5"]
            }
        }
        mock_get.return_value = mock_response

        puzzle = fetch_daily_puzzle()

        # Assertions
        self.assertIsNotNone(puzzle)
        self.assertEqual(puzzle['puzzle']['id'], 'test_id')
        self.assertEqual(puzzle['puzzle']['fen'], 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
        self.assertEqual(puzzle['puzzle']['solution'], ['e2e4', 'e7e5'])
        mock_get.assert_called_once_with("https://lichess.org/api/puzzle/daily")

    @patch('requests.get')
    def test_fetch_daily_puzzle_http_error(self, mock_get):
        """
        Test that fetch_daily_puzzle handles HTTP errors gracefully.
        """
        mock_get.side_effect = requests.exceptions.HTTPError("404 Not Found")

        puzzle = fetch_daily_puzzle()

        self.assertIsNone(puzzle)
        mock_get.assert_called_once_with("https://lichess.org/api/puzzle/daily")

    @patch('requests.get')
    def test_fetch_daily_puzzle_connection_error(self, mock_get):
        """
        Test that fetch_daily_puzzle handles connection errors gracefully.
        """
        mock_get.side_effect = requests.exceptions.ConnectionError("Network unreachable")

        puzzle = fetch_daily_puzzle()

        self.assertIsNone(puzzle)
        mock_get.assert_called_once_with("https://lichess.org/api/puzzle/daily")

if __name__ == '__main__':
    unittest.main()
