from dataclasses import dataclass
from typing import Sequence, Hashable


@dataclass(frozen=True)
class BPMDataCollectionSignal:
    values : Sequence[int]
    # invalid given that no data were available or
    # it was marked as invalid
    valid : Sequence[bool]


@dataclass(frozen=True)
class BPMDataCollectionPos:
    x: BPMDataCollectionSignal
    y: BPMDataCollectionSignal


@dataclass(frozen=True)
class BPMDataCollectionQuality:
    sum: BPMDataCollectionSignal
    q: BPMDataCollectionSignal


@dataclass(frozen=True)
class BPMDataCollectionButtons:
    a: BPMDataCollectionSignal
    b: BPMDataCollectionSignal
    c: BPMDataCollectionSignal
    d: BPMDataCollectionSignal


@dataclass(frozen=True)
class BPMDataCollection:
    pos : BPMDataCollectionPos
    quality : BPMDataCollectionQuality
    buttons : BPMDataCollectionButtons
    names : Sequence[str]
    cnt: int

    @property
    def identifer(self) -> Hashable:
        return self.cnt


@dataclass(frozen=True)
class BPMDataCollectionStatsSignal:
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

@dataclass(frozen=True)
class BPMDataCollectionStatsPos:
    x: BPMDataCollectionStatsSignal
    y: BPMDataCollectionStatsSignal


@dataclass(frozen=True)
class BPMDataCollectionStatsQuality:
    sum: BPMDataCollectionStatsSignal
    q: BPMDataCollectionStatsSignal

@dataclass(frozen=True)
class BPMDataCollectionStatsButtons:
    a: BPMDataCollectionStatsSignal
    b: BPMDataCollectionStatsSignal
    c: BPMDataCollectionStatsSignal
    d: BPMDataCollectionStatsSignal


@dataclass
class BPMDataCollectionStats:
    pos: BPMDataCollectionStatsPos
    quality: BPMDataCollectionStatsQuality
    buttons: BPMDataCollectionStatsButtons
    names : Sequence[str]


__all__ = ["BPMDataCollectionStats", "BPMDataCollection"]
