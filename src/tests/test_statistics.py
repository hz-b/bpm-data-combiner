import numpy as np

from bpm_data_combiner.data_model.bpm_data_accumulation import BPMDataAccumulationForSignal
from bpm_data_combiner.post_processor.statistics import compute_mean_weight


def test_compute_mean_weight_single_data():
    p = BPMDataAccumulationForSignal(
        values=np.array([[1, 2, 3, 4]]),
        valid=np.array([[True]*4])
    )
    print(p)
    r = compute_mean_weight(p)
    r.values == [1, 2, 3, 4]
    assert (r.n_readings == 1).all()
    assert (r.std == 0).all()