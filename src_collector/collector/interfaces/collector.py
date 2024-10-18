from abc import ABCMeta, abstractmethod

from ..data_model.collection_item import CollectionItem


class CollectorInterface(metaclass=ABCMeta):
    @abstractmethod
    def new_collection(self, val: CollectionItem) -> tuple[bool, bool]:
        """
        returns if
            already finished ?
        """
