"""
Todo:
    required? is it accessible from user space ?
"""
from abc import ABCMeta, abstractmethod

from typing import Dict

from .collection_item import CollectionItemInterface


class CollectionForOneIdInterface(metaclass=ABCMeta):
    @abstractmethod
    def add_item(self, item: CollectionItemInterface):
        pass

    @abstractmethod
    def data(self) -> Dict[str, CollectionItemInterface]:
        pass

    @property
    @abstractmethod
    def active(self)  -> bool:
        """is collection still waiting for data
        """

    @property
    @abstractmethod
    def ready(self)  -> bool:
        """does collection already have all data
        """

