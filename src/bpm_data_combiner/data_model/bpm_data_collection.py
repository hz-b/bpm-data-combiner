from dataclasses import dataclass
from typing import Sequence


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
    valid : Sequence[bool]


@dataclass
class BPMDataCollectionStats:
    x: BPMDataCollectionStatsPlane
    y: BPMDataCollectionStatsPlane
    names : Sequence[str]
