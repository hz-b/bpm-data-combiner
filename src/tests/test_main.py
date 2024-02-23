from datetime import timedelta, datetime
import itertools
import pytest
from time import sleep
from sys import stdout
import logging

from bpm_data_combiner.app.main import update, dev_name_index, col, monitor_devices

import pydev

logger = logging.getLogger("bpm-data-combiner")


def test10_main_dev_monitor():
    # Reset the states
    update(dev_name=None, reset=True)
    for dev_name in list(dev_name_index):
        update(dev_name=dev_name, enabled=False, plane="x")
        update(dev_name=dev_name, enabled=False, plane="y")

    for dev_name in list(dev_name_index):
        update(dev_name=dev_name, enabled=True, plane="x")
        update(dev_name=dev_name, enabled=True, plane="y")


def test20_main_behaved():
    """test that data stream is assembled to combined data"""

    update(dev_name=None, reset=True)

    N = 3
    for cnt in range(N):
        for dev_name in list(dev_name_index):
            update(dev_name=dev_name, cnt=cnt)
            update(dev_name=dev_name, x=cnt)
            update(dev_name=dev_name, y=-cnt)
            print(f"{dev_name=} {cnt=} ")
            update(dev_name=dev_name, ctl=cnt)

    for cnt in range(N):
        readings = col.get_collection(cnt)
        assert readings.is_ready()


def test30_main_interleaving():
    """Test that data are combined if the data of the devices are interleaved"""

    cnt = 4
    for dev_name in dev_name_index:
        update(dev_name=dev_name, cnt=cnt)
    for dev_name in dev_name_index:
        update(dev_name=dev_name, x=cnt)
        update(dev_name=dev_name, y=-cnt)
    for dev_name in dev_name_index:
        update(dev_name=dev_name, ctl=cnt)

    readings = col.get_collection(cnt)
    assert readings.is_ready()

def test40_monitor_collector_interaction():
    """Test that collector will give ready data if devices are makred a inacrtive
    """

    for dev_name in dev_name_index:
        # Make sure that all are active
        update(dev_name=dev_name, active=True)

    chk = 0
    def cnt_called(*args, **kwargs):
        nonlocal chk
        chk += 1

    col.on_ready.add_subscriber(cnt_called)
    # Send data properly
    def send_data(dev_name, cnt, val):
        update(dev_name=dev_name, cnt=cnt)
        update(dev_name=dev_name, x=val)
        update(dev_name=dev_name, y=-val)
        update(dev_name=dev_name, ctl=cnt)


    for val, dev_name in enumerate(dev_name_index):
        send_data(dev_name, 42, val)
    # All data sent.. so this should be now 1, cb evaluated once
    assert chk == 1

    dev_names = list(dev_name_index)
    update(dev_name=dev_names[0], active=False)
    for cnt, dev_name in enumerate(dev_names[1:]):
        send_data(dev_name, 23, cnt)

    # All data sent.. so the callback should have been
    # triggered a second time
    assert chk == 2


def test50_reading_single_device_misbehaved():
    """the first device sending second data set before first is finished
    """
    dev_names = list(dev_name_index)
    dev_name = dev_names[0]
    cnt = 5
    update(dev_name=dev_name, cnt=cnt)
    update(dev_name=dev_name, x=-10 * cnt)
    update(dev_name=dev_name, y=-100 * cnt)

    with pytest.raises(AssertionError) as ae:
        update(dev_name=dev_name, cnt=cnt + 1)



class ComputeDelay:
    """To get towards a periodic delay"""

    def __init__(self, *, dt: timedelta):
        self.dt = dt
        self.last = datetime.now()

    def get_delay(self) -> timedelta:
        now = datetime.now()
        next_point = self.last + self.dt
        delay = next_point - now
        assert delay.total_seconds() > 0
        self.last = next_point
        return delay


def run_performance():

    cmp_dly = ComputeDelay(dt=timedelta(milliseconds=100))
    N = 10
    counter = itertools.count()
    L = len(dev_name_index)
    while True:
        for i in range(N):
            delay = cmp_dly.get_delay().total_seconds()
            stdout.write(
                f"\r{L} devices, delay before next call: {delay * 1000:6.1f} ms"
            )
            sleep(delay)

            cnt = next(counter)
            for dev_name in dev_name_index:
                try:
                    update(dev_name=dev_name, cnt=cnt)
                    update(dev_name=dev_name, x=cnt)
                    update(dev_name=dev_name, y=-cnt)
                    update(dev_name=dev_name, ctl=cnt)
                except:
                    logger.error(f"{dev_name=}, {cnt=}")
                    raise

        for cnt in range(N):
            readings = col.get_collection(cnt)
            assert readings.is_ready()


if __name__ == "__main__":
    run_performance()
