from dataclasses import dataclass
from typing import Sequence, Hashable


@dataclass
class BPMDataCollectionPlane:
    values : Sequence[int]
    # invalid given that no data were available or
    # it was marked as invalid
    valid : Sequence[bool]


@dataclass
class BPMDataCollection:
    x: BPMDataCollectionPlane
    y: BPMDataCollectionPlane
    names : Sequence[str]
    cnt: int

    @property
    def identifer(self) -> Hashable:
        return self.cnt

@dataclass
class BPMDataCollectionStatsPlane:
    #: typically the mean value of the measurements
    values : Sequence[float]
    #: typically the inverse of the standard deviation of the
    #: values of the measurements times the number of measurements
    #: Todo: check is that the variance?
    std: Sequence[float]
    # invalid given that no data were available or
    # it was marked as invalid
    # Todo: is this information still needed given that n_readings exists?
    # valid : Sequence[bool]
    # how many data points arrived
    n_readings : Sequence[int]


@dataclass
class BPMDataCollectionStats:
    x: BPMDataCollectionStatsPlane
    y: BPMDataCollectionStatsPlane
    names : Sequence[str]


__all__ = ["BPMDataCollectionStats", "BPMDataCollection"]
