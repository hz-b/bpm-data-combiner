from dataclasses import dataclass
from typing import Sequence


@dataclass
class BPMDataCollectionPlane:
    values : Sequence[int]


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


class BPMDataCollectionStats:
    x: BPMDataCollectionStatsPlane
    y: BPMDataCollectionStatsPlane
    names : Sequence[str]
