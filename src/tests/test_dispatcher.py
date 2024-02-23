from bpm_data_combiner.bl.dispatcher import Dispatcher, DispatcherCollection
from bpm_data_combiner.data_model.bpm_data_reading import BPMReading
import pytest


def _run_disp_standard(*, cnt, x, y, disp=None):
    if disp is None:
        disp = Dispatcher("test_dev")
    disp.update(cnt=cnt)
    disp.update(x=x)
    disp.update(y=y)
    disp.update(cnt_chk=cnt)


def test_dispatcher_expected_behaviour():
    _run_disp_standard(cnt=1, x=1, y=1)


def test_dispatcher_missing_values():
    disp = Dispatcher("test_dev")
    disp.update(cnt=1)
    disp.update(x=1)
    with pytest.raises(AssertionError) as rc:
        disp.update(cnt_chk=1)


def test_dispatcher_not_started():
    disp = Dispatcher("test_dev")
    with pytest.raises(AssertionError) as rc:
        disp.update(x=1)


def test_dispatcher_not_restarted():
    disp = Dispatcher("test_dev")
    for i in range(3):
        _run_disp_standard(cnt=i, x=3, y=5, disp=disp)
    with pytest.raises(AssertionError) as rc:
        disp.update(x=1)


def test_dispatcher_calls_subscribers():

    cnt = 0

    def cb(val):
        assert isinstance(val, BPMReading)
        nonlocal cnt
        cnt += 1

    disp = Dispatcher("test_dev")
    disp.on_ready.add_subscriber(cb)

    _run_disp_standard(cnt=-1, x=3, y=5, disp=disp)
    assert cnt == 1


def test_dispatcher_collection():
    dp_col = DispatcherCollection()
    dp_col.get_dispatcher("BPMZ1T2R")
    dp_col.get_dispatcher("BPMZ4T8R")
