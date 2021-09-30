from time import time


class Timer:

    def __init__(self):
        self.started_at = time()

    def stop(self) -> str:
        hours, rest = divmod(time() - self.started_at, 3600)
        minutes, seconds = divmod(rest, 60)
        self.started_at = None
        return f'{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}'
