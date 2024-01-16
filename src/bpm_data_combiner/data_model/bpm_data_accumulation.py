"""output of accumulation

Todo:
   Review how to represent arrays / matrix like structures
   in a dataclass?
"""
from dataclasses import dataclass
import numpy as np
from typing import Sequence


@dataclass
class BPMDataAccumulationForPlane:
    # values i.e. the data
    values: np.ndarray
    # which data are valid
    valid: np.ndarray


@dataclass
class BPMDataAccumulation:
    # used masked array
    x: BPMDataAccumulationForPlane
    y: BPMDataAccumulationForPlane
    names: Sequence[str]
    counts: Sequence[int]
