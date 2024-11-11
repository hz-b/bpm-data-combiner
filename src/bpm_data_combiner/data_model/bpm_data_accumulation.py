"""output of accumulation

Todo:
   Review how to represent arrays / matrix like structures
   in a dataclass?
"""
from dataclasses import dataclass
import numpy as np
from typing import Sequence


@dataclass(frozen=True)
class BPMDataAccumulationForSignal:
    # values i.e. the data
    values: np.ndarray
    # which data are valid
    valid: np.ndarray


@dataclass(frozen=True)
class BPMDataAccumlationPos:
    x: BPMDataAccumulationForSignal
    y: BPMDataAccumulationForSignal



@dataclass(frozen=True)
class BPMDataAccumlationQuality:
    q: BPMDataAccumulationForSignal
    sum: BPMDataAccumulationForSignal


@dataclass(frozen=True)
class BPMDataAccumlationButtons:
    a: BPMDataAccumulationForSignal
    b: BPMDataAccumulationForSignal
    c: BPMDataAccumulationForSignal
    d: BPMDataAccumulationForSignal


@dataclass(frozen=True)
class BPMDataAccumulation:
    # used masked array
    pos : BPMDataAccumlationPos
    quality : BPMDataAccumlationQuality
    buttons : BPMDataAccumlationButtons
    names: Sequence[str]
    counts: Sequence[int]
