"""
This module provides functionality to fetch chess puzzles from the Lichess API.
"""

import requests

def fetch_daily_puzzle():
    """
    Fetches the daily chess puzzle from the Lichess API.

    Returns:
        dict: A dictionary containing puzzle information (e.g., FEN, moves)
              if successful, None otherwise.
    """
    url = "https://lichess.org/api/puzzle/daily"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching daily puzzle: {e}")
        return None

if __name__ == "__main__":
    # Example usage:
    puzzle = fetch_daily_puzzle()
    if puzzle:
        print("Daily Puzzle Fetched Successfully:")
        print(f"Puzzle ID: {puzzle.get('puzzle', {}).get('id')}")
        print(f"FEN: {puzzle.get('puzzle', {}).get('fen')}")
        print(f"Moves: {puzzle.get('puzzle', {}).get('solution')}")
    else:
        print("Failed to fetch daily puzzle.")
