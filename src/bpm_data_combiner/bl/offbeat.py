"""Offbeat beat

Support to determine which delay to use to get an offset beat.

Use case:
   * data from many devices are arriving periodically with some
     jitter. The jitter is considerably smaller than the update
     period
   * these data need to be combined
   * to combine the data a global counter is used

      * when data from the devices are arriving, they are
        tagged with the value of the global counter
      * the counter is updated in an off beat fashion:
        i.e. close to the middle of the update period

   * :class:`OffBeatDelay` derives the delay to be applied
     to some periodic loop so that the counter can be updated
     in an offbeat

Or short: a helper class for implementing a phased locked loop?

Todo:
    Terminology: is `offbeat` the correct name or should it be
    named `syncopation`
"""
from datetime import datetime

from typing import Sequence, Dict

import numpy as np
from pandas import Index

from .event import Event
from ..bl.collector import Collector
from ..data_model.timestamp import DataArrived

_now = datetime.now


def compute_median_delay_from_timestamps(data : Dict[str, DataArrived], *, reference_stamp_name : str, exclude_keys : Sequence[str]) -> float:
    """returns the median of the time difference between reference and all other data
    """
    ref = data[reference_stamp_name].timestamp
    stamps = np.array([d.timestamp for key, d in data.items() if key not in exclude_keys])
    dt = stamps - ref
    delay = np.median(dt)
    return delay


class OffBeatDelay:
    """Find out how much delay to create an offbeat

    uses mean of all timestamps to define delay

    Todo:
        Finalise implementation
    """
    def __init__(self, name: str, device_names: Sequence[str],
                 threshold : float = None,
                 reference_stamp_name="reference_stamp",
                 delay_name="delay_stamp"):

        assert reference_stamp_name != delay_name
        assert reference_stamp_name not in device_names
        assert delay_name not in device_names

        self.reference_stamp_name = reference_stamp_name
        self.delay_name = delay_name
        idx = Index([self.reference_stamp_name, self.delay_name] + device_names)

        self.col = Collector(name=name, devices_names=idx, threshold=threshold)
        self.counter = None
        self.delay = None
        self.on_new_delay = Event(name="offset_beat_delay_new_delay")

        def cb(data : Dict[str, DataArrived]):
            delay = compute_median_delay_from_timestamps(data, reference_stamp_name=self.reference_stamp_name,
                                                         exclude_keys=[self.reference_stamp_name, self.delay_name])
            # what a hack: should correct Data.Arrived.timestamp to payload?
            delay = delay.total_seconds() + data[self.delay_name].timestamp
            self.on_new_delay.trigger(delay)

        self.col.on_above_threshold.add_subscriber(cb)


    def data_arrived(self, *, name):
        if self.counter is None:
            return
        self.col.new_reading(
            DataArrived(cnt=self.counter, timestamp=_now(), dev_name=name)
        )

    def set_counter(self, cnt):
        """
        Todo: need to fix "new_reading"
        """
        self.counter = cnt
        assert(self.delay is not None)
        self.col.new_reading(
            DataArrived(cnt=self.counter, timestamp=_now(), dev_name=self.reference_stamp_name)
        )
        self.col.new_reading(
            DataArrived(cnt=self.counter, timestamp=self.delay, dev_name=self.delay_name)
        )

    def set_delay(self, delay):
        """
        Todo:
             implement using delay
        """
        self.delay = delay


__all__ = ["OffBeatDelay"]
