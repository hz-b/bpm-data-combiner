import numpy as np

from ..data_model.bpm_data_accumulation import BPMDataAccumulationForSignal, BPMDataAccumulation
from ..data_model.bpm_data_collection import BPMDataCollectionStatsSignal, BPMDataCollectionStats, BPMDataCollection, \
    BPMDataCollectionStatsPos, BPMDataCollectionStatsQuality, BPMDataCollectionStatsButtons


def compute_weights_scaled(values#: ArrayLike,
                           ,*, n_readings: int): # -> ArrayLike:
    """Compute weights taking number of readings into account

    Currently unused
    """
    n, _ = values.shape
    return np.where(n_readings, n_readings / n * values.std(axis=0), np.inf)


def compute_mean_weight(accumulated_data: BPMDataAccumulationForSignal) -> BPMDataCollectionStatsSignal:
    """compute mean and weighted std of first axis,

    Weights are the standard deviation times the number of readings found
    """
    val = accumulated_data.values
    n_readings = accumulated_data.valid.sum(axis=0)
    return BPMDataCollectionStatsSignal(values=val.mean(axis=0), std=val.std(axis=0), n_readings=n_readings)


def compute_mean_weights_for_signals(data : BPMDataAccumulation) -> BPMDataCollectionStats:
    """
    """
    return BPMDataCollectionStats(
        pos=BPMDataCollectionStatsPos(
            x=compute_mean_weight(data.pos.x),
            y=compute_mean_weight(data.pos.y),
        ),
        quality=BPMDataCollectionStatsQuality(
            q=compute_mean_weight(data.quality.q),
            sum=compute_mean_weight(data.quality.sum),
        ),
        buttons=BPMDataCollectionStatsButtons(
            a=compute_mean_weight(data.buttons.a),
            b=compute_mean_weight(data.buttons.b),
            c=compute_mean_weight(data.buttons.c),
            d=compute_mean_weight(data.buttons.d),
        ),
        names=data.names
    )
