import numpy as np
from numpy import ma
# from numpy.typing import ArrayLike

from ..data_model.bpm_data_accumulation import BPMDataAccumulationForPlane, BPMDataAccumulation
from ..data_model.bpm_data_collection import BPMDataCollectionStatsPlane, BPMDataCollectionStats

def compute_weights_scaled(values, *, n_readings: int): # -> ArrayLike:
    """Compute weights taking number of readings into account

    Currently unused
    """
    n, _ = values.shape
    return np.where(n_readings, n_readings / n * values.std(axis=0), np.inf)


def compute_mean_weight(accumulated_data: BPMDataAccumulationForPlane) -> BPMDataCollectionStatsPlane:
    """compute mean and weighted std of first axis,

    Weights are the standard deviation times the number of readings found
    """
    val = accumulated_data.values
    n_readings = accumulated_data.valid.sum(axis=0)
    return BPMDataCollectionStatsPlane(values=val.mean(axis=0), std=val.std(axis=0), n_readings=n_readings)


def compute_mean_weights_for_planes(data : BPMDataAccumulation) -> BPMDataCollectionStats:
    """
    """
    return BPMDataCollectionStats(
        x=compute_mean_weight(data.x), y=compute_mean_weight(data.y), names=data.names
    )
