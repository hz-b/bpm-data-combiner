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
from ..interfaces.collection_for_one_id import CollectionForOneIdInterface
from ..interfaces.collection_item import CollectionItemInterface
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

        @functools.lru_cache(maxsize=max_collections)
        def _get_collection(cnt: Hashable) -> CollectionForOneIdInterface:
            r = CollectionForOneId(
                source_names=self.device_names,
                threshold=threshold,
                id=cnt,
            )
            return r

        self._get_collection = _get_collection
        self.last_cnt = None

    def reset(self):
        self._get_collection.cache_clear()

    def get_collection(self, cnt: Hashable):
        col = self._get_collection(cnt)
        self.last_cnt = cnt
        #: todo: I think this is always true
        assert col.active or col.ready
        return col

    def new_item(self, val: CollectionItemInterface) -> CollectionForOneIdInterface:
        """

        Returns:
            collection for this identifer: user can check if it is ready or not
        """
        rc = self._get_collection(val.identifier)
        rc.add_item(val)
        return rc

    @property
    def device_names(self):
        return self._device_names

    @device_names.setter
    def device_names(self, device_names: Sequence[str]):
        self._device_names = device_names

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
                f"device_names={self.device_names},"
                f" last_cnt={self.last_cnt}"
            ")"
        )
