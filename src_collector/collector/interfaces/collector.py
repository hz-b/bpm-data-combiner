from abc import ABCMeta, abstractmethod

from .collection_for_one_id import CollectionForOneIdInterface
from .collection_item import CollectionItemInterface


class CollectorInterface(metaclass=ABCMeta):
    @abstractmethod
    def new_item(self, val: CollectionItemInterface) -> CollectionForOneIdInterface:
        """
        returns: collection

        returns the collection the items was stuffed in. The user can then
        inspect if this collection is already ready.
        """
