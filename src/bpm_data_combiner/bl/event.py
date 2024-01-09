"""A very simple and basic event implementation

Only allows subscription to the event
"""
from typing import Sequence, Callable


class Event:
    """A single event managing subscribers

    The subscribers will be called when :method:`trigger` is called.
    The object is then passed to the subscribers.
    """

    def __init__(self, *, name: str, subscribers: Sequence[Callable] = None):
        self.name = name
        if subscribers is None:
            subscribers = []
        self.subscribers = []
        for sub in subscribers:
            self.add_subscriber(sub)

    def add_subscriber(self, cb: Callable):
        """each callable shall expect a single argument"""
        assert callable(cb)
        self.subscribers.append(cb)

    def trigger(self, obj):
        """

        Todo:
            review name
        """
        for sub in self.subscribers:
            sub(obj)

    def __repr__(self):
        cls_name = self.__class__.__name__
        subs_text = ", ".join([repr(s) for s in self.subscribers])
        return f"{cls_name}(name={self.name}, subscribers={subs_text})"


__all__ = ["Event"]
