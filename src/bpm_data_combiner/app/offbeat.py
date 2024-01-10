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

from typing import Sequence

from pandas import Index

from ..bl.collector import Collector
from ..data_model.timestamp import DataArrived

_now = datetime.now

reference_stamp_name = "reference_stamp"

class OffBeatDelay:
    """Find out how much delay to create an offbeat

    uses mean of all timestamps to define delay

    Todo:
        Finalise implementation
    """
    def __init__(self, device_names: Sequence[str]):
        assert reference_stamp_name not in device_names
        self.col = Collector(devices_names=Index([reference_stamp_name] + device_names))
        self.counter = None

    def data_arrived(self, *, dev_name, plane):
        if self.counter is None:
            return

        self.col.new_reading(
            DataArrived(cnt=self.counter, timestamp=_now(), name=dev_name, plane="x")
        )

    def set_counter(self, cnt):
        """
        Todo: need to fix "new_reading"
        """
        self.counter = cnt
        nd = DataArrived(cnt=self.counter, timestamp=_now(), name=reference_stamp_name, plane="x")
        return
        self.col.new_reading(nd)

    def set_delay(self, delay):
        """
        Todo:
             implement using delay
        """
