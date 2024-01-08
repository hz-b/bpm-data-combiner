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
    #: typically the std values of the measurements
    #: time the number of measurements
    #: Todo: check is that the variance?
    weights : Sequence[float]
    # invalid given that no data were available or
    # it was marked as invalid
    valid : Sequence[bool]


@dataclass
class BPMDataCollectionStats:
    x: BPMDataCollectionStatsPlane
    y: BPMDataCollectionStatsPlane
    active : Sequence[bool]
    names : Sequence[str]
