from chess_puzzle_ai_cli.utils.logging import log

class ClockModel:
    def __init__(self, clock_file_path):
        self._clock_file_path = clock_file_path
        self._time_left = 0.0

    def get_time(self):
        try:
            with open(self._clock_file_path, 'r') as f:
                self._time_left = float(f.read().strip())
        except (IOError, ValueError) as e:
            log.error(f"Error reading or parsing clock file: {e}")
            self._time_left = 0.0
        return self._time_left
