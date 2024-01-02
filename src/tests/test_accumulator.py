import pytest

from bpm_data_combiner.bl.accumulator import Accumulator


def test_accumulator_empty():
    """exception raised if no data available
    """
    dev_names = ["a_test1", "a_test2", "a_test3"]
    acc = Accumulator(dev_names)

    with pytest.raises(AssertionError):
        acc.get()


def test_accumulator_add():
    """Simple data, all from same devices
    """
    dev_names = [f"a_test_{cnt:d}" for cnt in range(10)]
    acc = Accumulator(dev_names)
