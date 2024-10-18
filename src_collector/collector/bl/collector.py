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
from typing import Sequence, Hashable

from ..bl.collection_for_one_id import CollectionForOneId
from ..bl.event import Event
from ..data_model.collection_item import CollectionItem
from ..interfaces.collector import CollectorInterface



class Collector(CollectorInterface):
    """Provide access to active reading collections

    It works assuming that not more than `max_collections` are
    required to be cached. Uses lru_cache for caching the objects.

    Todo:
        keep track of finished / timeout :class:`ReadingsCollection`
        instances?
        to be able to discard :class:`BPMReading` instances that
        arrive far too late?
    """

    def __init__(
        self,
        *,
        devices_names: Sequence[str],
        threshold: float = None,
        max_collections: int = 50,
    ):
        self._device_names = devices_names
        self.on_new_collection = Event(name="on_new_collection")
        self.on_above_threshold = Event(name="reading_collection_on_threshold")
        self.on_ready = Event(name="reading_collection_on_ready")

        @functools.lru_cache(maxsize=max_collections)
        def _get_collection(cnt: Hashable):
            r = CollectionForOneId(
                device_names=self.device_names,
                threshold=threshold,
                id=cnt,
            )
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

    def new_collection(self, val: CollectionItem):
        rc = self._get_collection(val.id_)
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
