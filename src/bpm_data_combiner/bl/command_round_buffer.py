from dataclasses import dataclass
from collections import deque


@dataclass(frozen=True)
class Command:
    cmd : str
    dev_name : str
    kwargs : dict

    
class CommandRoundBuffer:
    def __init__(self, maxsize=20):
        self.roundbuffer = deque()
        self.maxsize = maxsize

    def append(self, cmd: Command):
        if len(self.roundbuffer) > self.maxsize:
            self.roundbuffer.popleft()
        self.roundbuffer.append(cmd)

    def last(self):
        return self.roundbuffer[-1]
    
    def __repr__(self):
        header = "cnt device   ctl  kwargs"
        return "\n".join([header] + [f"{cnt:2d}  {c.dev_name:8s} {c.cmd:4s} {repr(c.kwargs):s} " for cnt, c in enumerate(self.roundbuffer)])

