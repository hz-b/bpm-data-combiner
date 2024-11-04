from abc import ABCMeta, abstractmethod
from typing import Hashable


class CollectionItemInterface(metaclass=ABCMeta):
    """From one source, from one identifier
    """
    @property
    @abstractmethod
    def identifier(self) -> Hashable:
        pass

    @property
    @abstractmethod
    def source(self) -> Hashable:
        pass
