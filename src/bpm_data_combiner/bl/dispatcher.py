"""Dispatch received data to subscribes as dataclasses

The last reassembly

Todo:
    does p4p solves that in this case
"""
import functools
from typing import List
from ..data_model.bpm_data_reading import BPMReadingBeingProcessed, BPMReading


class Dispatcher:
    def __init__(self, dev_name):
        self.dev_name = dev_name
        self.reading = None
        self.subscribers = []

    def subscribe(self, cb):
        self.subscribers.append(cb)

    def new_reading(self, cnt):
        assert self.reading is None
        self.reading = BPMReadingBeingProcessed(cnt=cnt)

    def update_x_val(self, x_val):
        assert self.reading is not None
        self.reading.x = x_val

    def update_y_val(self, y_val):
        assert self.reading is not None
        self.reading.y = y_val

    def update_check(self, chk):
        """
        Todo:
            find a better name?
        """
        assert self.reading.ready(chk)
        r = BPMReading(cnt=self.reading.cnt, x=self.reading.x, y=self.reading.y, dev_name=self.dev_name)
        self.reading = None
        for sub in self.subscribers: sub(r)

    def update(self, **kwargs):
        cmds = dict(
            cnt=self.new_reading,
            x=self.update_x_val,
            y=self.update_y_val,
            cnt_chk=self.update_check
        )
        for cmd, val in kwargs.items():
            method = cmds[cmd]
            method(val)


class DispatcherCollection:
    def __init__(self, subscribers: List = None):
        self.dispatchers = dict()
        if subscribers is None:
            subscribers = []
        assert callable(subscribers.append)
        for sub in subscribers: assert callable(sub)
        self.subscribers = subscribers

    def subscribe(self, cb):
        assert callable(cb)
        self.subscribers.append(cb)
        for _, dp in self.dispatchers.items():
            for cb in self.subscribers:
                dp.subscribe(cb)

    @functools.lru_cache(maxsize=None)
    def get_dispatcher(self, dev_name) -> Dispatcher:
        dp = Dispatcher(dev_name)
        for cb in self.subscribers:
            dp.subscribe(cb)
        self.dispatchers[dev_name] = dp
        return dp





