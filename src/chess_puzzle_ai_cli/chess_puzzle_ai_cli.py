"""
This module contains the main CLI logic for the chess-puzzle-ai-cli application.
"""

import chess
import chess.pgn
import io
import argparse
import subprocess
import threading
import time

from rich.console import Console

from chess_puzzle_ai_cli.puzzle_fetcher import fetch_daily_puzzle
from chess_puzzle_ai_cli.puzzle.puzzle_manager import PuzzleManager

from prompt_toolkit import Application
from prompt_toolkit.layout import Layout, Window, HSplit, D, FormattedTextControl
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.widgets import TextArea
from prompt_toolkit.buffer import Buffer


# Import cli-chess UI components
from chess_puzzle_ai_cli.cli_chess_ui.modules.board.board_model import BoardModel
from chess_puzzle_ai_cli.cli_chess_ui.modules.board.board_presenter import BoardPresenter
from chess_puzzle_ai_cli.cli_chess_ui.utils.styles import default as default_styles
from prompt_toolkit.styles import Style

# Global console for rich output outside of prompt_toolkit application
console = Console()

# Global variable to hold the AI process
ai_process = None
ai_process_status = "AI Agent: Not running"

def main():
    """
    The main game loop for the chess puzzle.
    """
    global ai_process, ai_process_status

    parser = argparse.ArgumentParser(description="Chess Puzzle AI CLI Wrapper")
    parser.add_argument("--command", type=str, help="The AI agent command to run in the background.")
    args = parser.parse_args()

    if args.command:
        try:
            ai_process = subprocess.Popen(args.command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            ai_process_status = f"AI Agent: Running (PID: {ai_process.pid})"
            console.print(f"Started AI agent: {args.command}")
        except Exception as e:
            ai_process_status = f"AI Agent: Failed to start ({e})"
            console.print(f"Error starting AI agent: {e}")

    puzzle_data = fetch_daily_puzzle()
    if not puzzle_data:
        console.print("Failed to fetch daily puzzle.")
        if ai_process: ai_process.terminate()
        return

    game_data = puzzle_data.get('game')
    puzzle_info = puzzle_data.get('puzzle')

    if not game_data or not puzzle_info:
        console.print("Invalid puzzle data format.")
        if ai_process: ai_process.terminate()
        return

    pgn_string = game_data.get('pgn')
    initial_ply = puzzle_info.get('initialPly')
    solution_uci = puzzle_info.get('solution')

    if not pgn_string or initial_ply is None or not solution_uci:
        console.print("Puzzle data is incomplete.")
        if ai_process: ai_process.terminate()
        return

    # Create a game from the PGN
    pgn_io = io.StringIO(pgn_string)
    game = chess.pgn.read_game(pgn_io)

    # Fast-forward to the puzzle's starting position
    node = game
    for _ in range(initial_ply):
        node = node.next()
    
    board_obj = node.board() # Renamed to avoid conflict with BoardModel
    
    # Initialize PuzzleManager
    puzzle_manager = PuzzleManager()
    puzzle_manager.load_puzzle({'fen': board_obj.fen(), 'moves': solution_uci})
    
    # Initialize BoardModel and BoardPresenter from cli-chess UI
    board_model = BoardModel(fen=puzzle_manager.get_current_board_fen())
    board_presenter = BoardPresenter(board_model)

    # Temporarily disable clock for testing
    # from cli_chess.modules.clock.clock_presenter import ClockPresenter
    # clock_presenter = ClockPresenter(board_model)

    # Key bindings for prompt_toolkit application
    kb = KeyBindings()

    @kb.add('c-q')
    @kb.add('c-c')
    def _(event):
        """Press Ctrl-Q or Ctrl-C to exit."""
        if ai_process: ai_process.terminate()
        event.app.exit()

    # Initial board display from BoardPresenter
    board_window = board_presenter.view.__pt_container__()
    status_control = FormattedTextControl(ai_process_status)
    
    # Input field
    input_field = TextArea(
        height=1,
        prompt="Enter your move (e.g., e2e4), or 'exit' to quit: ",
        multiline=False,
        wrap_lines=False,
    )

    def handle_input(buffer: Buffer):
        global ai_process_status
        user_move_uci = buffer.text.strip()
        buffer.text = '' # Clear input field

        # Check AI process status
        if ai_process and ai_process.poll() is not None:
            ai_process_status = f"AI Agent: Finished (Exit Code: {ai_process.returncode})"
            status_control.text = ai_process_status
            console.print(ai_process_status)
            application.exit()
            return

        if user_move_uci.lower() == 'exit':
            console.print("You quit the puzzle.")
            if ai_process: ai_process.terminate()
            application.exit()
            return
        
        if puzzle_manager.make_move(user_move_uci):
            board_model.fen = puzzle_manager.get_current_board_fen()
            console.print("Correct!")
            if puzzle_manager.is_puzzle_solved():
                console.print("Congratulations, you solved the puzzle!")
                if ai_process: ai_process.terminate()
                application.exit()
            else:
                # Make Lichess's move
                console.print("Lichess's turn...")
                lichess_move = puzzle_manager.get_expected_move()
                puzzle_manager.make_move(lichess_move) # Make the move in the puzzle manager
                board_model.fen = puzzle_manager.get_current_board_fen() # Update the board model
                if puzzle_manager.is_puzzle_solved():
                    console.print("Congratulations, you solved the puzzle!")
                    if ai_process: ai_process.terminate()
                    application.exit()
        else:
            console.print(f"Incorrect move. Expected {puzzle_manager.get_expected_move()}. Try again.")

    input_field.accept_handler = handle_input

    root_container = HSplit([
        board_window,
        Window(content=status_control, height=1, style="bg:#333333 fg:white"), # AI status display
        input_field,
    ])
    layout = Layout(root_container, focused_element=input_field)
    application = Application(layout=layout, key_bindings=kb, full_screen=True, style=Style.from_dict(default_styles))

    application.run()