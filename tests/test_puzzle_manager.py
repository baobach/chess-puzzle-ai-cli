import unittest
import chess
from chess_puzzle_ai_cli.puzzle.puzzle_manager import PuzzleManager

class TestPuzzleManager(unittest.TestCase):

    def setUp(self):
        """
        Set up a new PuzzleManager instance and a sample puzzle for each test.
        """
        self.puzzle_manager = PuzzleManager()
        self.sample_puzzle_data = {
            'fen': 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1',
            'moves': ['e2e4', 'e7e5', 'g1f3', 'b8c6']
        }

    def test_load_puzzle(self):
        """
        Test that a puzzle is loaded correctly.
        """
        self.puzzle_manager.load_puzzle(self.sample_puzzle_data)
        self.assertIsNotNone(self.puzzle_manager.board)
        self.assertEqual(self.puzzle_manager.board.fen(), self.sample_puzzle_data['fen'])
        self.assertEqual(len(self.puzzle_manager.solution_moves), len(self.sample_puzzle_data['moves']))
        self.assertEqual(self.puzzle_manager.current_move_index, 0)

    def test_make_correct_move(self):
        """
        Test making a correct move.
        """
        self.puzzle_manager.load_puzzle(self.sample_puzzle_data)
        initial_fen = self.puzzle_manager.board.fen()
        
        # Make the first correct move
        is_correct = self.puzzle_manager.make_move('e2e4')
        self.assertTrue(is_correct)
        self.assertEqual(self.puzzle_manager.current_move_index, 1)
        self.assertNotEqual(self.puzzle_manager.board.fen(), initial_fen)
        
        # Make the second correct move (Lichess's move)
        is_correct = self.puzzle_manager.make_move('e7e5')
        self.assertTrue(is_correct)
        self.assertEqual(self.puzzle_manager.current_move_index, 2)

    def test_make_incorrect_move(self):
        """
        Test making an incorrect move.
        """
        self.puzzle_manager.load_puzzle(self.sample_puzzle_data)
        initial_fen = self.puzzle_manager.board.fen()
        
        # Try to make an incorrect move
        is_correct = self.puzzle_manager.make_move('d2d4')
        self.assertFalse(is_correct)
        self.assertEqual(self.puzzle_manager.current_move_index, 0) # Should not advance
        self.assertEqual(self.puzzle_manager.board.fen(), initial_fen) # Board should not change

    def test_is_puzzle_solved(self):
        """
        Test checking if the puzzle is solved.
        """
        self.puzzle_manager.load_puzzle(self.sample_puzzle_data)
        self.assertFalse(self.puzzle_manager.is_puzzle_solved())

        # Make all correct moves
        for move_uci in self.sample_puzzle_data['moves']:
            self.puzzle_manager.make_move(move_uci)
        
        self.assertTrue(self.puzzle_manager.is_puzzle_solved())

    def test_get_expected_move(self):
        """
        Test getting the expected move.
        """
        self.puzzle_manager.load_puzzle(self.sample_puzzle_data)
        self.assertEqual(self.puzzle_manager.get_expected_move(), 'e2e4')
        self.puzzle_manager.make_move('e2e4')
        self.assertEqual(self.puzzle_manager.get_expected_move(), 'e7e5')
        self.puzzle_manager.make_move('e7e5')
        self.assertEqual(self.puzzle_manager.get_expected_move(), 'g1f3')
        self.puzzle_manager.make_move('g1f3')
        self.assertEqual(self.puzzle_manager.get_expected_move(), 'b8c6')
        self.puzzle_manager.make_move('b8c6')
        self.assertEqual(self.puzzle_manager.get_expected_move(), '') # Puzzle solved

if __name__ == '__main__':
    unittest.main()
