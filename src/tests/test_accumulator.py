"""
Todo:
    follow split up: accumulation and data processing as in code

"""
import pytest
import numpy as np
from bpm_data_combiner.bl.accumulator import Accumulator
from bpm_data_combiner.data_model.bpm_data_reading import BPMReading
from bpm_data_combiner.post_processor.combine import collection_to_bpm_data_collection, accumulated_collections_to_array
from bpm_data_combiner.post_processor.statistics import compute_mean_weights_for_planes

dev_names_index = {f"a_test_{cnt:d}": cnt for cnt in range(10)}


def test_accumulator_empty():
    """exception raised if no data available"""
    acc = Accumulator()

    with pytest.raises(AssertionError):
        acc.get()


def test_accumulator_add():
    """Simple data, all from same devices"""
    acc = Accumulator()

    n = 3

    L = len(dev_names_index)
    test_data = np.array([np.arange(1, L + 1) * i for i in range (1, n+1)])
    for i, indices in enumerate(test_data):
        X = indices
        Y = -indices
        d = {
            name: BPMReading(dev_name=name, x=x, y=y, cnt=i)
            for name, x, y, in zip(dev_names_index, X, Y)
        }
        acc.add(collection_to_bpm_data_collection(d, dev_names_index))

    rc = accumulated_collections_to_array(acc.get(), dev_names_index)
    assert (np.array(rc.names) == np.array(list(dev_names_index))).all()
    assert (rc.x.values.astype(int) == test_data).all()
    assert (rc.y.values.astype(int) == -test_data).all()

    # check stats too
    # (1/2 * n * (n + 1) ) / n
    ref_val = (n + 1) / 2
    data = compute_mean_weights_for_planes(rc)

def test_accumulator_entry_missing():
    """Simple data, all from same devices"""
    acc = Accumulator()

    L = len(dev_names_index)
    indices = np.arange(1, L + 1)
    for i, cnt in enumerate(indices):
        # Make one device looking missing
        selection = np.ones(L, bool)
        selection[i] = False
        names = [name for name, sel in zip(dev_names_index, selection) if sel]
        X = np.arange(1, L) * cnt
        Y = -np.arange(1, L) * cnt

        d = {
            name: BPMReading(dev_name=name, x=x, y=y, cnt=cnt)
            for name, x, y, in zip(names, X, Y)
        }
        acc.add(collection_to_bpm_data_collection(d, dev_names_index=dev_names_index))

    indices = np.arange(1, L + 1)


    rc = accumulated_collections_to_array(acc.get(), dev_names_index)
    assert (rc.names == np.array(list(dev_names_index))).all()
    # (1/2 * n * (n + 1) ) / n
    ref_val = (len(indices) + 1) / 2
    # as a value is missing, the scaled refernce value should not be reproduced
    assert not (rc.x.values == ref_val * indices).all()
    assert not (rc.y.values == -ref_val * indices).all()


def test_accumulator_devices_always_missing():
    """Simple data, all from same devices"""
    acc = Accumulator()

    L = len(dev_names_index)
    selection = np.ones(len(dev_names_index), dtype=bool)
    selection[5] = False
    selection[7] = False
    names = [name for name, sel in zip(dev_names_index, selection) if sel]

    test_data = np.array([np.arange(1, L - 1) * (i + 1) for i in range(5)])
    for i, indices in enumerate(test_data):
        X = indices
        Y = -indices

        d = {
            name: BPMReading(dev_name=name, x=x, y=y, cnt=i)
            for name, x, y, in zip(names, X, Y)
        }
        acc.add(collection_to_bpm_data_collection(d, dev_names_index))

    r = accumulated_collections_to_array(acc.get(), dev_names_index)

    for valid in [r.x.valid, r.y.valid]:
        assert valid.shape == (len(test_data), len(selection))
        assert (np.sum(valid, axis=1) == np.array(len(names))[np.newaxis]).all()
