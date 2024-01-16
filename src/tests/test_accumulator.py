import pytest
import numpy as np
from bpm_data_combiner.bl.accumulator import Accumulator
from bpm_data_combiner.data_model.bpm_data_reading import BPMReading


def test_accumulator_empty():
    """exception raised if no data available"""
    dev_names = ["a_test1", "a_test2", "a_test3"]
    acc = Accumulator(dev_names)

    with pytest.raises(AssertionError):
        acc.get()


def test_accumulator_add():
    """Simple data, all from same devices"""
    dev_names = [f"a_test_{cnt:d}" for cnt in range(10)]
    acc = Accumulator(dev_names)

    n = 3

    L = len(dev_names)
    test_data = np.array([np.arange(1, L + 1) * i for i in range (1, n+1)])
    for i, indices in enumerate(test_data):
        X = indices
        Y = -indices
        d = {
            name: BPMReading(dev_name=name, x=x, y=y, cnt=i)
            for name, x, y, in zip(dev_names, X, Y)
        }
        acc.add(d)

    rc = acc.get()
    assert (rc.names == dev_names).all()
    # (1/2 * n * (n + 1) ) / n
    ref_val = (n + 1) / 2
    assert (rc.x.values == test_data).all()
    assert (rc.y.values == -test_data).all()


def test_accumulator_entry_missing():
    """Simple data, all from same devices"""
    dev_names = np.array([f"a_test_{cnt:d}" for cnt in range(10)])
    acc = Accumulator(dev_names)

    L = len(dev_names)
    indices = np.arange(1, L + 1)
    for i, cnt in enumerate(indices):
        # Make one device looking missing
        idx = np.ones(L, bool)
        idx[i] = False
        names = dev_names[idx]
        X = np.arange(1, L) * cnt
        Y = -np.arange(1, L) * cnt

        d = {
            name: BPMReading(dev_name=name, x=x, y=y, cnt=cnt)
            for name, x, y, in zip(names, X, Y)
        }
        acc.add(d)

    indices = np.arange(1, L + 1)

    rc = acc.get()
    assert (rc.names == dev_names).all()
    # (1/2 * n * (n + 1) ) / n
    ref_val = (len(indices) + 1) / 2
    # as a value is missing, the scaled refernce value should not be reproduced
    assert not (rc.x.values == ref_val * indices).all()
    assert not (rc.y.values == -ref_val * indices).all()


def test_accumulator_devices_always_missing():
    """Simple data, all from same devices"""
    dev_names = np.array([f"a_test_{cnt:d}" for cnt in range(10)])
    acc = Accumulator(dev_names)

    L = len(dev_names)
    selection = np.ones(len(dev_names), dtype=bool)
    selection[5] = False
    selection[7] = False
    names = dev_names[selection]

    test_data = np.array([np.arange(1, L - 1) * (i + 1) for i in range(5)])
    for i, indices in enumerate(test_data):
        X = indices
        Y = -indices

        d = {
            name: BPMReading(dev_name=name, x=x, y=y, cnt=i)
            for name, x, y, in zip(names, X, Y)
        }
        acc.add(d)

    r = acc.get()

    for valid in [r.x.valid, r.y.valid]:
        assert valid.shape == (len(test_data), len(selection))
        assert (np.sum(valid, axis=1) == np.array(len(names))[np.newaxis]).all()
