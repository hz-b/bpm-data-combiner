from abc import ABCMeta, abstractmethod
from typing import Callable


class EventInterface(metaclass=ABCMeta):
    @abstractmethod
    def add_subscriber(self, cb: Callable):
        """add a subscriber to this event"""

    @abstractmethod
    def trigger(self, obj: object):
        """call callbacks with the object"""
