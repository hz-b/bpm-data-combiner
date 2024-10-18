from abc import ABCMeta, abstractmethod

from collector.interfaces.collection_item import CollectionItemInterface


class CollectorInterface(metaclass=ABCMeta):
    @abstractmethod
    def new_collection(self, val: CollectionItemInterface) -> tuple[bool, bool]:
        """
        returns if
            already finished ?
        """
