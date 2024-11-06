from .count_down import CountDown


class BPMInput:
    def __init__(self, bpm_name: str, heart_beat_steps=20):
        self.bpm_name = bpm_name
        self.status = CountDown(max_steps=heart_beat_steps)
