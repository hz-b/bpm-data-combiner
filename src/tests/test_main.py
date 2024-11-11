"""

Assuming that all update is a thin wrapper around
:meth:`Facade.update`
Assuming that test_facade tests all the different update calls
"""
import numpy as np
from bpm_data_combiner.app.main import update
from bpm_data_combiner.app.known_devices import dev_names_bessyii as dev_names


def test10_update_reset():
    update(dev_name=None, reset=True)


def test20_reading():
    update(dev_name=None, reset=True)
    data = [0] + [42, 2**13, 2**14] + [0] * 2 + [0] * 4
    update(dev_name=dev_names[0], reading=np.array(data).astype(np.int32))
