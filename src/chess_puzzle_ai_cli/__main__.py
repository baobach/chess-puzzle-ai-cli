from prompt_toolkit.application import Application
from prompt_toolkit.layout import Layout
from chess_puzzle_ai_cli.modules.board.board_model import BoardModel
from chess_puzzle_ai_cli.modules.board.board_presenter import BoardPresenter
from chess_puzzle_ai_cli.modules.board.board_view import BoardView
from chess_puzzle_ai_cli.utils.styles import default
from prompt_toolkit.styles import Style, merge_styles
from chess_puzzle_ai_cli.utils.config import game_config, terminal_config, player_info_config, lichess_config
from chess_puzzle_ai_cli.utils.logging import configure_logger

def main() -> None:
    # Initialize logging
    configure_logger("chess-puzzle-ai-cli")

    # Initialize configs (this will create default config files if they don't exist)
    game_config
    terminal_config
    player_info_config
    lichess_config

    # Create a default board model
    board_model = BoardModel()

    # Create a board presenter
    board_presenter = BoardPresenter(board_model)

    # Create a board view
    board_view = BoardView(board_presenter, board_presenter.get_board_display())

    # Create the application
    application = Application(
        layout=Layout(board_view),
        full_screen=True,
        mouse_support=True,
        style=merge_styles([Style.from_dict(default)]),
    )

    # Run the application
    application.run()

if __name__ == "__main__":
    main()
