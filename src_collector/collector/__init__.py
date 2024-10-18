"""Combine data from different sources using identifiers

Identifiers are

* name of the sender
* package id

Shall still work if packages arrive out of order
"""
from .bl.collector import Collector
from collector.interfaces.collection_item import CollectionItemInterface
from .errors import DoubleSubmissionError, UnknownDeviceNameError

__all__ = [
    "CollectionItemInterface",
    "Collector",
    "DoubleSubmissionError",
    "UnknownDeviceNameError",
]
