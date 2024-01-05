"""Accumulate collected readings: to provide mean data
"""
from collections import deque
import numpy as np
from typing import Sequence

from ..data_model.bpm_data_collection import BPMDataCollection, BPMDataCollectionStats, BPMDataCollectionStatsPlane


class Accumulator:
    def __init__(self, dev_names: Sequence[str]):
        self.collections = deque()

    def add(self, col: BPMDataCollection):
        self.collections.append(col)

    def get(self) -> BPMDataCollectionStats:
        """Find out which data actually to use
        """
        assert len(self.collections) > 0

        #: Todo: should it be protected by a lock?
        cols, self.collections = self.collections, deque()

        #: How is it taken care of that data are missing?
        # Todo: should it be using a masked array
        tmp  = np.array(
            [[(r.x.values, r.y.values) for r in c] for c in cols]
        )

        x = tmp[:, 0, :]
        y = tmp[:, 1, :]

        return BPMDataCollectionStats(
            x=BPMDataCollectionStatsPlane(values=x.mean(axis=0), weights=x.std(axis=0)),
            y=BPMDataCollectionStatsPlane(values=y.mean(axis=0), weights=y.std(axis=0)),
            names=names
        )

