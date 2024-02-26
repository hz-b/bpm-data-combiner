"""Accumulate collected readings: to provide mean data
"""
from ..data_model.bpm_data_accumulation import (
    BPMDataAccumulation,
    BPMDataAccumulationForPlane,
)
from ..data_model.bpm_data_reading import BPMReading
from .collector import _combine_collections_by_device_names
from typing import Dict
import numpy as np


class Accumulator:
    def __init__(self, dev_names_index: Dict[str, int], max_entries: int = 100):
        # Need to know all dev_names
        # I am using pandas Index for looking up position and handling
        # filling data at correct place
        self.dev_names_index = dev_names_index
        self.collections = None
        # so collections allocator are handled in a single place
        self.swap(check_collection_length=False)

    def add(self, col: Dict[str, BPMReading]):
        self.collections.append(col)

    def swap(self, check_collection_length: bool = True):
        """return collected collections, initialise internals to new"""
        if check_collection_length:
            assert len(self.collections) > 0
        # Data are processed: make object ready for further accumulation
        #: Todo: should it be protected by a lock?
        collections, self.collections = self.collections, list()
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

        tmp = _combine_collections_by_device_names(
            collections, self.dev_names_index, default_value=0
        )
        counts = np.zeros(len(collections), dtype=np.int64)
        for row, data_collection in enumerate(collections):
            for _, bpm_data in data_collection.items():
                counts[row] = bpm_data.cnt
                break

        x, y = tmp[..., 0], tmp[..., 1]

        return BPMDataAccumulation(
            x=BPMDataAccumulationForPlane(values=x.data, valid=~x.mask),
            y=BPMDataAccumulationForPlane(values=y.data, valid=~y.mask),
            names=list(self.dev_names_index),
            counts=counts,
        )
