"""

Todo:
    reimplement it for
"""
from typing import Sequence, Tuple
import sys
import numpy as np


import pydev


def recalculate_value(*, value, nm2bits, scale=1, verbose=False):
    """scale value to bits
    """
    nval = np.round(np.asarray(value) * nm2bits * scale).astype(np.int16)
    # set it artificially to 1 ... otherwise SOFB rejects the data
    nval[np.absolute(nval)<1] = 1
    if verbose:
        printf(f"val {val} -> nval {nval}")
    return nval.tolist()


def write_rearranged_data(stream, data, name):
    stream.write(f"start {name:10s} ----------------------------\n")
    for col in data:
        stream.write(" ".join([f"{x:5d}" for x in col]) + "\n")
    stream.write(f"end   {name:10s} ----------------------------\n")
    stream.flush()


def insert(*, data: Sequence, x: Tuple[int, int], y: Tuple[int, int], active: bool, index=int, verbose=False) -> Sequence:
    """
    """
    if len(data) == 0:
        if verbose:
            print("Data was of length 0. I asssume start up is running")
        return

    data = np.array(data)
    rearranged = data.reshape(8, -1)
    if verbose:
        print(f"inserting at index {index}")
        write_rearranged_data(sys.stdout, rearranged, "input")

    x_val, x_std = x
    y_val, y_std = y
    del x, y

    # ensure that data is gone ...
    rearranged[:, index] = 0

    rearranged[0, index] = x_val
    rearranged[1, index] = y_val
    rearranged[6, index] = x_std
    rearranged[7, index] = y_std

    rearranged[4, index] = active * 3

    if verbose:
        write_rearranged_data(sys.stdout, rearranged, "output")

    ndata = rearranged.ravel().tolist()
    pydev.iointr('scaled-bpm-data', ndata)
    return ndata
