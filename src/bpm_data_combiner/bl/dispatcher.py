"""Dispatch received data to subscribes as dataclasses

All subscribers to :class:`DispatcherCollection` subscribe to all
:class:`Dispatcher`. Currently handled by:

:class:`DispatcherCollection` subscribes its
on_ready :meth:`Event.trigger` to each created dispatcher event
:any:`Dispatcher.on_ready`. Subscribers to
:class:`DispatcherCollection` are subscribing to its on_ready
event, and thus any dispatcher triggering on_ready will trigger
the subscribers to DispatcherCollection

Todo:
    does p4p solves that in this case
"""
import functools
from typing import List

from .event import Event
from ..data_model.bpm_data_reading import BPMReadingBeingProcessed, BPMReading


class Dispatcher:
    def __init__(self, dev_name):
        self.dev_name = dev_name
        self.reading = None
        self.on_ready = Event(name="dispatcher_data_ready")

    def new_reading(self, cnt):
        if self.reading is not None:
            raise AssertionError(
                f"{self.__class__.__name__}: start new reading: already processing?"
            )
        assert self.reading is None
        self.reading = BPMReadingBeingProcessed(cnt=cnt, dev_name=self.dev_name)

    def update_x_val(self, x_val):
        if self.reading is None:
            raise AssertionError(
                f"{self.__class__.__name__}: adding to x to reading: processing not started?"
            )
        assert self.reading is not None
        self.reading.x = x_val

    def update_y_val(self, y_val):
        if self.reading is None:
            raise AssertionError(
                f"{self.__class__.__name__}: adding to y to reading: processing not started?"
            )
        self.reading.y = y_val

    def update_check(self, chk):
        """
        Todo:
            find a better name?
        """
        if self.reading is None:
            raise AssertionError(
                f"{self.__class__.__name__}: expected reading finished but not yet started?"
            )

        if not self.reading.ready(chk):
            # dispose it and go further
            r, self.reading = self.reading, None
            raise AssertionError(f"Reading {r} not ready")

        r = BPMReading(
            cnt=self.reading.cnt,
            x=self.reading.x,
            y=self.reading.y,
            dev_name=self.dev_name,
        )
        self.reading = None
        self.on_ready.trigger(r)

    def update(self, **kwargs):
        cmds = dict(
            cnt=self.new_reading,
            x=self.update_x_val,
            y=self.update_y_val,
            cnt_chk=self.update_check,
        )
        for cmd, val in kwargs.items():
            method = cmds[cmd]
            method(val)


class DispatcherCollection:
    def __init__(self, subscribers: List = []):
        self.dispatchers = dict()
        for sub in subscribers:
            assert callable(sub)
        self.on_ready = Event(name="dispatcher_collection_data_ready")

    def subscribe(self, cb):
        self.on_ready.add_subscriber(cb)

    @functools.lru_cache(maxsize=None)
    def get_dispatcher(self, dev_name) -> Dispatcher:
        dp = Dispatcher(dev_name)
        dp.on_ready.add_subscriber(self.on_ready.trigger)
        self.dispatchers[dev_name] = dp
        return dp

    def reset(self):
        self.get_dispatcher.cache_clear()