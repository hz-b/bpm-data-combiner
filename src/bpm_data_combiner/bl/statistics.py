import numpy as np
from numpy import ma

from ..data_model.bpm_data_accumulation import BPMDataAccumulationForPlane, BPMDataAccumulation
from ..data_model.bpm_data_collection import BPMDataCollectionStatsPlane, BPMDataCollectionStats


def compute_mean_weight(accumulated_data: BPMDataAccumulationForPlane) -> BPMDataCollectionStatsPlane:
    """compute mean and weighted std of first axis,

    Weights are the standard deviation times the number of readings found
    """
    n, _ = accumulated_data.values.shape
    values = ma.masked_array(data=accumulated_data.values, mask=~accumulated_data.valid)
    mean = values.mean(axis=0)
    n_readings = np.sum(~values.mask, axis=0)
    weights = np.where(n_readings, n_readings / n * values.std(axis=0), np.inf)
    return BPMDataCollectionStatsPlane(values=mean, weights=weights, valid=~weights.mask)


def compute_mean_weights_for_planes(data : BPMDataAccumulation) -> BPMDataCollectionStats:
    """
    """
    return BPMDataCollectionStats(
        x=compute_mean_weight(data.x), y=compute_mean_weight(data.y), names=data.names
    )