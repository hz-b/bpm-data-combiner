class CountDown:
    def __init__(self, max_steps: int):
        self.value = 0
        self.max_steps = max_steps

    def reset(self) -> None:
        self.value = 0

    def step(self) -> None:
        if self.value <  self.max_steps:
            self.value += 1

    def status(self) -> int:
        return self.max_steps - self.value

