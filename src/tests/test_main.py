"""

Assuming that all update is a thin wrapper around
:meth:`Facade.update`
Assuming that test_facade tests all the different update calls
"""
from copy import copy
import numpy as np
from bpm_data_combiner.app.main import update, controller
from known_devices import dev_names_bessyii as dev_names


def test10_update_reset():
    update(dev_name=None, reset=True)


def test20_reading():
    update(dev_name=None, reset=True)
    update(dev_name=dev_names[0], reading=np.array([42, 2**13, 2**14]).astype(np.int32))
