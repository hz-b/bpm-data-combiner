"""Combine data from different sources using identifiers

Identifiers are

* name of the sender
* package id

Shall still work if packages arrive out of order
"""
from .bl.collector import Collector
from .interfaces.collection_item import CollectionItemInterface
from .interfaces.collector import CollectorInterface
from .errors import DoubleSubmissionError, UnknownDeviceNameError

__all__ = [
    "CollectionItemInterface",
    "CollectorInterface",
    "Collector",
    "DoubleSubmissionError",
    "UnknownDeviceNameError",
]
