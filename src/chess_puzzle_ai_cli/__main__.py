import argparse
from prompt_toolkit.application import Application
from prompt_toolkit.layout import Layout
from chess_puzzle_ai_cli.modules.board.board_model import BoardModel
from chess_puzzle_ai_cli.modules.board.board_presenter import BoardPresenter
from chess_puzzle_ai_cli.modules.board.board_view import BoardView
from chess_puzzle_ai_cli.modules.clock.clock_model import ClockModel
from chess_puzzle_ai_cli.modules.clock.clock_presenter import ClockPresenter
from chess_puzzle_ai_cli.modules.clock.clock_view import ClockView
from prompt_toolkit.layout.containers import HSplit, VSplit, WindowAlign
from chess_puzzle_ai_cli.utils.styles import default
from prompt_toolkit.styles import Style, merge_styles
from chess_puzzle_ai_cli.utils.config import game_config, terminal_config, player_info_config, lichess_config
from chess_puzzle_ai_cli.utils.logging import configure_logger, log

def _parse_arguments():
    parser = argparse.ArgumentParser(description="Chess Puzzle AI CLI Wrapper")
    parser.add_argument(
        "--clock-file",
        type=str,
        help="Path to the file containing the current clock time from the AI agent."
    )
    parser.add_argument(
        "--status-file",
        type=str,
        help="Path to the file containing the status of the AI agent's task."
    )
    return parser.parse_args()

def main() -> None:
    # Initialize logging
    configure_logger("chess-puzzle-ai-cli")

    # Initialize configs (this will create default config files if they don't exist)
    game_config
    terminal_config
    player_info_config
    lichess_config

    args = _parse_arguments()
    log.info(f"Received clock_file: {args.clock_file}")
    log.info(f"Received status_file: {args.status_file}")

    # Create a default board model
    board_model = BoardModel()

    # Create a board presenter
    board_presenter = BoardPresenter(board_model)

    # Create a board view
    board_view = BoardView(board_presenter, board_presenter.get_board_display())

    # Create a clock model
    clock_model = ClockModel(args.clock_file)

    # Create a clock presenter
    clock_presenter = ClockPresenter(clock_model)

    # Create a clock view
    clock_view = ClockView(clock_presenter)

    # Create the application layout
    layout = Layout(
        HSplit([
            board_view,
            VSplit([clock_view], align=WindowAlign.CENTER)
        ])
    )

    # Create the application
    application = Application(
        layout=layout,
        full_screen=True,
        mouse_support=True,
        style=merge_styles([Style.from_dict(default)]),
    )

    # Set up a timer to refresh the clock view periodically
    def on_render(app):
        clock_view.update()

    application.before_render += on_render

    # Run the application
    application.run()

if __name__ == "__main__":
    main()
