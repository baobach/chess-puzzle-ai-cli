import chess
import chess.engine

class PuzzleManager:
    """
    Manages chess puzzles, including loading, move validation, and solution checking.
    """
    def __init__(self):
        self.current_puzzle = None
        self.board = None
        self.solution_moves = []
        self.current_move_index = 0

    def load_puzzle(self, puzzle_data: dict):
        """
        Loads a new puzzle from the provided data.

        Args:
            puzzle_data (dict): A dictionary containing puzzle information,
                                 e.g., {'fen': '...', 'moves': ['e2e4', 'e7e5']}.
        """
        self.current_puzzle = puzzle_data
        self.board = chess.Board(puzzle_data['fen'])
        self.solution_moves = [chess.Move.from_uci(move) for move in puzzle_data['moves']]
        self.current_move_index = 0
        print(f"Puzzle loaded. FEN: {self.board.fen()}")

    def make_move(self, move_uci: str) -> bool:
        """
        Attempts to make a move on the puzzle board and validates it against the solution.

        Args:
            move_uci (str): The move in UCI format (e.g., 'e2e4').

        Returns:
            bool: True if the move is correct and part of the solution, False otherwise.
        """
        try:
            move = chess.Move.from_uci(move_uci)
            if move == self.solution_moves[self.current_move_index]:
                self.board.push(move)
                self.current_move_index += 1
                print(f"Correct move! Board FEN: {self.board.fen()}")
                return True
            else:
                print(f"Incorrect move. Expected {self.solution_moves[self.current_move_index].uci()}")
                return False
        except ValueError:
            print("Invalid move format.")
            return False
        except IndexError:
            print("Puzzle already completed or no more moves expected.")
            return False

    def is_puzzle_solved(self) -> bool:
        """
        Checks if the current puzzle has been solved.

        Returns:
            bool: True if all solution moves have been played, False otherwise.
        """
        return self.current_move_index == len(self.solution_moves)

    def get_current_board_fen(self) -> str:
        """
        Returns the FEN string of the current board state.
        """
        return self.board.fen() if self.board else ""

    def get_expected_move(self) -> str:
        """
        Returns the expected move in UCI format for the current puzzle state.
        """
        if self.current_move_index < len(self.solution_moves):
            return self.solution_moves[self.current_move_index].uci()
        return ""
