"""Accumulate collected readings: to provide mean data
"""
import logging

from bpm_data_combiner.data_model.bpm_data_accumulation import (
    BPMDataAccumulation,
    BPMDataAccumulationForPlane,
)

from collections import deque
import numpy as np
from typing import Dict

logger = logging.getLogger("bpm-data-combiner")


class Accumulator:
    def __init__(self, max_entries: int = 100):
        # Need to know all dev_names
        # I am using pandas Index for looking up position and handling
        # filling data at correct place
        self.collections = None
        # so collections allocator are handled in a single place
        self.swap(check_collection_length=False)
        self.max_entries = max_entries

    def add(self, col: Dict[str, object]):
        logger.debug("Accumulator: adding collection!")
        self.collections.append(col)
        if len(self.collections) > self.max_entries:
            self.collections.popleft()

    def swap(self, check_collection_length: bool = True):
        """return collected collections, initialise internals to new"""
        if check_collection_length:
            assert len(self.collections) > 0
        # Data are processed: make object ready for further accumulation
        #: Todo: should it be protected by a lock?
        collections, self.collections = self.collections, deque()
        return collections

    def get(self, swap=True) -> BPMDataAccumulation:
        """

        Warning:
            Side effect: internal collection is reset if swap is True
        """
        # only implemented and tested for this usage
        assert swap
        if swap:
            collections = self.swap()
        else:
            collections = self.collections
        return collections

