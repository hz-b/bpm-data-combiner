from typing import Sequence, Hashable, Dict
import logging
from ..data_model.collection_item import CollectionItem
from ..errors import UnknownDeviceNameError, DoubleSubmissionError
from ..interfaces.colletion_for_one_id import CollectionForOneIdInterface

logger = logging.getLogger("combiner")


class CollectionForOneId(CollectionForOneIdInterface):
    """Collect data for one count

    use :meth:`ready` to see if sufficient data is here
    """

    def __init__(
        self,
        *,
        device_names: Sequence[str],
        threshold: int = None,
        id: Hashable,
    ):
        self.collection = dict()
        self.device_names = set(device_names)
        # for debug purposes
        self.id = id

        if threshold is None:
            threshold = max(1, len(device_names) // 2)
        self.threshold = threshold

        self._ready = False
        self._above_threshold = False
        self._is_active = True

    def add_reading(self, item: CollectionItem):
        """cmd.dev_name

        Todo: should disabled data be discarded?
        """
        name = item.name
        # data from known / expected device
        if name not in self.device_names:
            logger.info(
                "Collector: expecting following device names %s; unknown name %s",
                self.device_names,
                name,
            )
            raise UnknownDeviceNameError(f"Unknown or unusable device {name}")
        # not one device sending twice
        if name in self.collection:
            raise DoubleSubmissionError(f"{name=} already in collection")

        # data expected
        assert self.active
        self.collection[name] = item
        self._ready, self._above_threshold = self.is_ready()

    def data(self) -> Dict[str, CollectionItem]:
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
