"""

Todo:
    reimplement it for 
"""
from typing import Sequence, Tuple
import sys
import numpy as np


def write_rearranged_data(stream, data, name):
    stream.write(f"start {name:10s} ----------------------------\n")
    for col in data:
        stream.write(" ".join([f"{x:5d}" for x in col]) + "\n")
    stream.write(f"end   {name:10s} ----------------------------\n")
    stream.flush()

    
def insert(*, data: Sequence, x: Tuple[int, int], y: Tuple[int, int], scale: float, active: bool, index=int, verbose=False) -> Sequence:
    """
    """
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
    rearranged[6, index] = x_std * scale
    rearranged[7, index] = y_std * scale

    rearranged[4, index] = active * 2
    # ndata[2, index] = y_val
    # ndata[3, index] = y_std

    ndata = rearranged.ravel()
    if verbose:
        write_rearranged_data(sys.stdout, rearranged, "output")
    return ndata

