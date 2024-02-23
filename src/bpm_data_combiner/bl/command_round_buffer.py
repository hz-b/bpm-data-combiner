from collections import deque
from ..data_model.command import Command


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
        header = "timestamp cnt device   ctl  kwargs"
        return "\n".join([header] + [f"{c.timestamp.hour}:{c.timestamp.minute}:{c.timestamp.second} {cnt:2d}  {c.dev_name:8s} {c.cmd:4s} {repr(c.kwargs):s} " for cnt, c in enumerate(self.roundbuffer)])


def dict_to_string(d: dict):
    tmp = ", ".join([f"{k}:{v}" for k,v in d.items()])
    return "{" + tmp + "}"


def round_buffer_to_string(rb: CommandRoundBuffer):
    def stringify_command(cmd):
        tmp = dict_to_string(cmd.kwargs)
        dev_name = cmd.dev_name
        if dev_name is  None:
            dev_name = "None"
        tmp = f"{dev_name:8s} {tmp}"
        return  f"{tmp:39s}"
    return [stringify_command(cmd) for cmd in list(rb.roundbuffer)[::-1]]
