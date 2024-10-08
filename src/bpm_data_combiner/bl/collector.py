"""
Combine the data to common sets

Idea:
    when 50 percent of devices have fired: take this moment for
    reference.
    * when all have responded: get data out
    * if more than half a delta t has passed push data out on the flaky channel

Question:
   what to do with very late arrivals?
   how long of a queue to preserve
"""
import functools
from typing import Sequence, Hashable, Dict
import numpy as np
import numpy.ma as ma

from ..data_model.collection_item import CollectionItem
from ..data_model.monitored_device import MonitoredDevice
from ..errors import DoubleSubmissionError, UnknownDeviceNameError
from .event import Event
from ..data_model.bpm_data_reading import BPMReading
from ..data_model.bpm_data_collection import BPMDataCollection, BPMDataCollectionPlane

from .logger import logger

from sys import stderr as stream

def _combine_collections_by_device_names(
    collections: Sequence[Dict[str, BPMReading]], dev_names_index: dict, *, default_value
) -> ma.masked_array:
    """use the name to stuff data into correct location

    Todo:
        Should it return a masked array? Is there a better
        representation?
    """
    res = np.empty([len(collections), len(dev_names_index), 2], dtype=np.int32)
    res.fill(default_value)
    res = ma.array(res, mask=True)

    # now fill data at appropriate place
    # todo: handle that x and y plane can be enabled separately
    for row, data_collection in enumerate(collections):
        for name, bpm_data in data_collection.items():
            col = dev_names_index[name]
            res.mask[row, col, :] = False
            for plane, val in enumerate([bpm_data.x, bpm_data.y]):
                if val is None:
                    res[row, col, plane].mask = True
                else:
                    res[row, col, plane] = val

    return res


def collection_to_bpm_data_collection(
    collection: Dict[str, BPMReading], dev_names_index: Dict, default_value=2**31-1
):
    ma = _combine_collections_by_device_names([collection], dev_names_index,
                                              default_value=default_value)
    # only one collection -> first dimension one entry
    (ma,) = ma
    # need one reading to get its count
    for _, reading in collection.items():
        break
    return BPMDataCollection(
        x=BPMDataCollectionPlane(values=ma[:, 0], valid=~ma.mask[:,0]),
        y=BPMDataCollectionPlane(values=ma[:, 1], valid=~ma.mask[:,1]),
        names=list(dev_names_index),
        # assuming to be the same for both planes
        cnt=reading.cnt,
    )


class ReadingsCollection:
    """Collect data for one count

    use :meth:`ready` to see if sufficient data is here
    """

    def __init__(self, *, name: str, device_names: Sequence[str], threshold: int = None, cnt : int):
        self.name = name
        self.collection = dict()
        self.device_names = set(device_names)
        # for debug purposes
        self.cnt = cnt

        if threshold is None:
            threshold = max(1, len(device_names) // 2)
        self.threshold = threshold

        self._ready = False
        self._above_threshold = False
        self._is_active = True

    def add_reading(self, val: BPMReading):
        """cmd.dev_name

        Todo: should disabled data be discarded?
        """
        dev_name = val.dev_name
        # data from known / expected device
        if dev_name not in self.device_names:
            logger.info("Collector %s: expecting following device names %s; unknown name %s",
                          self.name, self.device_names, dev_name)
            raise UnknownDeviceNameError(f"Unknown or unusable device {dev_name}")
        # not one device sending twice
        if dev_name in self.collection:
            raise DoubleSubmissionError(f"{dev_name=} already in collection")

        # data expected
        assert self.active
        self.collection[dev_name] = val
        self._ready, self._above_threshold = self.is_ready()

    def data(self) -> Dict[str, BPMReading]:
        return self.collection

    def is_ready(self) -> (bool, bool):
        """Compare to device list and see if all names are in"""
        L = len(self.device_names.difference(self.collection.keys()))
        return L == 0, L < self.threshold

    @property
    def ready(self) -> bool:
        return self._ready

    @property
    def above_threshold(self) -> bool:
        return self._above_threshold

    @property
    def active(self) -> bool:
        """just a convenience function

        return not self.ready

        Todo:
            check if it should be removed
        """
        return not self.ready


class Collector:
    """Provide access to active reading collections

    It works assuming that not more than `max_collections` are
    required to be cached. Uses lru_cache for caching the objects.

    Todo:
        keep track of finished / timeout :class:`ReadingsCollection`
        instances?
        to be able to discard :class:`BPMReading` instances that
        arrive far too late?
    """

    def __init__(self, *, name: str, devices_names: Sequence[str], threshold : float = None, max_collections: int = 50):
        self.name = name
        self._device_names = devices_names
        self.on_new_collection = Event(name="on_new_collection")
        self.on_above_threshold = Event(name="reading_collection_on_threshold")
        self.on_ready = Event(name="reading_collection_on_ready")

        @functools.lru_cache(maxsize=max_collections)
        def _get_collection(cnt: Hashable):
            r = ReadingsCollection(name=self.name, device_names=self.device_names, threshold=threshold, cnt=cnt)
            self.on_new_collection.trigger(r)
            return r

        self._get_collection = _get_collection

    def reset(self):
        self._get_collection.cache_clear()

    def get_collection(self, cnt: Hashable):
        col = self._get_collection(cnt)
        #: todo: I think this is always true
        assert col.active or col.ready
        return col

    def new_reading(self, val: CollectionItem):
        rc = self._get_collection(val.cnt)
        rc.add_reading(val)
        if rc.ready:
            self.on_ready.trigger(rc.data())
        if rc.above_threshold:
            self.on_above_threshold.trigger(rc.data())

    @property
    def device_names(self):
        return self._device_names

    @device_names.setter
    def device_names(self, device_names: Sequence[str]):
        self._device_names = device_names
