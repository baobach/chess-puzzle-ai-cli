from prompt_toolkit.widgets import TextArea
from .clock_presenter import ClockPresenter

class ClockView:
    def __init__(self, presenter: ClockPresenter):
        self._presenter = presenter
        self._text_area = TextArea(text=self._presenter.get_time_display(), height=1, width=5)

    def __pt_container__(self):
        return self._text_area

    def update(self):
        self._text_area.text = self._presenter.get_time_display()
