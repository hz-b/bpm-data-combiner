from typing import Sequence, Hashable, Dict
import logging
from collector.interfaces.collection_item import CollectionItemInterface
from ..errors import UnknownDeviceNameError, DoubleSubmissionError
from ..interfaces.collection_for_one_id import CollectionForOneIdInterface

logger = logging.getLogger("combiner")


class CollectionForOneId(CollectionForOneIdInterface):
    """Collect data for one count

    use :meth:`ready` to see if sufficient data is here
    """

    def __init__(
        self,
        *,
        source_names: Sequence[str],
        threshold: int = None,
        id: Hashable,
    ):
        self.collection = dict()
        self.source_names = set(source_names)
        # for debug purposes
        self.id = id

        if threshold is None:
            threshold = max(1, len(source_names) // 2)
        self.threshold = threshold

        self._ready = False
        self._above_threshold = False
        self._is_active = True

    def add_item(self, item: CollectionItemInterface):
        """cmd.dev_name

        Todo: should disabled data be discarded?
        """
        name = item.source
        # data from known / expected device
        if name not in self.source_names:
            logger.info(
                "Collector: expecting following device names %s; unknown name %s",
                self.source_names,
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

    def data(self) -> Dict[str, CollectionItemInterface]:
        return self.collection

    def sources_missing(self):
        return self.source_names.difference(self.collection.keys())

    def is_ready(self) -> (bool, bool):
        """Compare to device list and see if all names are in"""
        L = len(self.sources_missing())
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

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
                f"id={self.id},"
                f" ready={self.ready},"
                f" sources_missing={self.sources_missing()}"
            ")"
        )
