from .clock_model import ClockModel

class ClockPresenter:
    def __init__(self, model: ClockModel):
        self._model = model

    def get_time_display(self) -> str:
        seconds = self._model.get_time()
        minutes = int(seconds / 60)
        seconds = int(seconds % 60)
        return f"{minutes:02d}:{seconds:02d}"
