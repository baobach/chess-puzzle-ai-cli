import pytest
from unittest.mock import MagicMock
from chess_puzzle_ai_cli.modules.clock.clock_model import ClockModel
from chess_puzzle_ai_cli.modules.clock.clock_presenter import ClockPresenter
from chess_puzzle_ai_cli.modules.clock.clock_view import ClockView

@pytest.fixture
def clock_file(tmp_path):
    file_path = tmp_path / "clock.txt"
    file_path.write_text("123")
    return str(file_path)

def test_clock_integration(clock_file):
    # Create the components
    model = ClockModel(clock_file)
    presenter = ClockPresenter(model)
    view = ClockView(presenter)

    # Initial display
    assert view._text_area.text == "02:03"

    # Update the clock file
    with open(clock_file, "w") as f:
        f.write("60")

    # Update the view
    view.update()

    # Check if the display has been updated
    assert view._text_area.text == "01:00"
