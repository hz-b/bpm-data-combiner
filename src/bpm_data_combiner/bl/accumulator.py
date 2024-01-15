"""Accumulate collected readings: to provide mean data
"""
from typing import Sequence, Dict
import numpy as np
import numpy.ma as ma

# could be also based on a list, index does more internal checks
# that's why it is used here
from pandas import Index
from ..data_model.bpm_data_reading import BPMReading
from ..data_model.bpm_data_collection import (
    BPMDataCollectionStats,
    BPMDataCollectionStatsPlane,
)
from .collector import _combine_collections_by_device_names

#  collections, #,
#  dev_names_index# : Index


def compute_mean_weight(values: ma.masked_array) -> (ma.masked_array, ma.masked_array):
    """compute mean and weighted std of first axis,

    Weights are the standard deviation times the number of readings found
    """
    n, _ = values.shape
    mean = values.mean(axis=0)
    n_readings = np.sum(~values.mask, axis=0)
    weights = np.where(n_readings, n_readings / n * values.std(axis=0), np.inf)
    return mean, weights


class Accumulator:
    def __init__(self, dev_names: Sequence[str]):
        # Need to know all dev_names
        # I am using pandas Index for looking up position and handling
        # filling data at correct place
        self.dev_names_index = Index(dev_names)
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

    def get(self, swap=True) -> BPMDataCollectionStats:
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

        tmp = _combine_collections_by_device_names(collections, self.dev_names_index)

        xm, xw = compute_mean_weight(tmp[..., 0])
        ym, yw = compute_mean_weight(tmp[..., 1])
        return BPMDataCollectionStats(
            x=BPMDataCollectionStatsPlane(values=xm, weights=xw, valid=~xm.mask),
            y=BPMDataCollectionStatsPlane(values=ym, weights=yw, valid=~ym.mask),
            names=self.dev_names_index.values,
        )
