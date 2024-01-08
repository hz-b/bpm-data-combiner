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
from pandas import Index

from ..errors import DoubleSubmissionError
from .event import Event
from ..data_model.bpm_data_reading import BPMReading
from ..data_model.bpm_data_collection import BPMDataCollection, BPMDataCollectionPlane


def _combine_collections_by_device_names(
    collections: Sequence[Dict[str, BPMReading]], dev_names_index: Index
) -> ma.masked_array:
    """use the name to stuff data into correct location

    Todo:
        Should it return a masked array
    """
    res = np.zeros([len(collections), len(dev_names_index), 2], dtype=np.int64)
    res = ma.array(res, fill_value=0, mask=True)

    # now fill data at appropriate place
    for cnt, data_collection in enumerate(collections):
        for name, bpm_data in data_collection.items():
            idx = dev_names_index.get_loc(name)
            res.mask[cnt, idx, :] = False
            res[cnt, idx, 0] = bpm_data.x
            res[cnt, idx, 1] = bpm_data.y
    return res


def collection_to_bpm_data_collection(
    collection: Dict[str, BPMReading], dev_names_index: Index
):
    ma = _combine_collections_by_device_names([collection], dev_names_index)
    # only one collection -> first dimension one entry
    (ma,) = ma
    # need one reading to get its count
    for _, reading in collection.items():
        break
    return BPMDataCollection(
        x=BPMDataCollectionPlane(values=ma[:, 0]),
        y=BPMDataCollectionPlane(values=ma[:, 1]),
        names=dev_names_index.values,
        # assuming to be the same for both planes
        active=ma.mask[:, 0],
        cnt=reading.cnt,
    )


class ReadingsCollection:
    """Collect data for one count

    use :meth:`ready` to see if sufficient data is here
    """

    def __init__(self, *, device_names: Sequence, threshold: int = None):
        self.collection = dict()
        self.device_names = set(device_names)

        if threshold is None:
            self.threshold = max(1, len(device_names) // 2)

        self._ready = False
        self._above_threshold = False
        self._is_active = True

    def add_reading(self, val: BPMReading):
        dev_name = val.dev_name
        # data from known / expected device
        assert dev_name in self.device_names
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
        """just a convenience

        Or more expressive
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

    def __init__(self, *, devices_names: Sequence[str], max_collections: int = 50):
        self.device_names = devices_names
        self.on_new_collection = Event(name="on_new_collection")
        self.on_above_threshold = Event(name="reading_collection_on_threshold")
        self.on_ready = Event(name="reading_collection_on_ready")

        @functools.lru_cache(maxsize=max_collections)
        def _get_collection(cnt: Hashable):
            r = ReadingsCollection(device_names=self.device_names)
            self.on_new_collection.trigger(r)
            return r

        self._get_collection = _get_collection

    def get_collection(self, cnt: Hashable):
        col = self._get_collection(cnt)
        #: todo: I think this is always true
        assert col.active or col.ready
        return col

    def new_reading(self, val: BPMReading):
        rc = self._get_collection(val.cnt)
        rc.add_reading(val)
        if rc.ready:
            self.on_ready.trigger(rc.data())
        if rc.above_threshold:
            self.on_above_threshold.trigger(rc.data())
