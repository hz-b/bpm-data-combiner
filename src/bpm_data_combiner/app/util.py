import numpy as np


def combine_counts(high: np.ndarray[np.int32], low: np.ndarray[np.int32]):
    return (high << 32) | np.array(low).astype(np.uint32)


