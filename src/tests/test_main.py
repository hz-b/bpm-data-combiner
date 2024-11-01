from datetime import timedelta, datetime
import itertools
import pytest
from time import sleep
from sys import stdout
import logging
import pydev

from bpm_data_combiner.app.main import update, facade
from known_devices import dev_names_bessyii as dev_names

facade.set_device_names(device_names=dev_names)
# activate all devices first

for name in facade.dev_name_index:
    facade.dev_status(name, "enabled", True)
    facade.dev_status(name, "active", True)
    facade.dev_status(name, "synchronised", 2)


logger = logging.getLogger("bpm-data-combiner")


def test10_main_dev_monitor():
    # Reset the states
    update(dev_name=None, reset=True)
    for dev_name in list(facade.dev_name_index):
        update(dev_name=dev_name, enabled=False, plane="x")
        update(dev_name=dev_name, enabled=False, plane="y")

    for dev_name in list(facade.dev_name_index):
        update(dev_name=dev_name, enabled=True, plane="x")
        update(dev_name=dev_name, enabled=True, plane="y")


def test20_main_behaved():
    """test that data stream is assembled to combined data"""

    update(dev_name=None, reset=True)

    N = 3
    for cnt in range(N):
        for dev_name in list(facade.dev_name_index):
            update(dev_name=dev_name, reading=[cnt, 2 * cnt, -cnt])

    for cnt in range(N):
        readings = facade.collector.get_collection(cnt)
        assert readings.is_ready()


def test30_main_interleaving():
    """Test that data are combined if the data of the devices are interleaved"""

    cnt = 4
    for dev_name in facade.dev_name_index:
        update(dev_name=dev_name, reading=[cnt, 2 * cnt, -cnt])

    readings = facade.collector.get_collection(cnt)
    assert readings.is_ready()


def test40_monitor_collector_interaction():
    """Test that collector will still show ready for one id even if devices are marked as inactive"""

    for dev_name in facade.dev_name_index:
        # Make sure that all are active
        update(dev_name=dev_name, active=True)

    # Send data properly
    def send_data(dev_name, cnt, val):
        update(dev_name=dev_name, reading=[cnt, val, -val])

    id_ = 42
    for val, dev_name in enumerate(facade.dev_name_index):
        send_data(dev_name, id_, val)
    # All data sent.. so this should be now 1, cb evaluated once
    assert facade.collector.get_collection(42).ready

    id_ = 23
    dev_names = list(facade.dev_name_index)
    update(dev_name=dev_names[0], active=False)
    for cnt, dev_name in enumerate(dev_names[1:]):
        send_data(dev_name, id_, cnt)

    # All data sent.. so the callback should have been
    # triggered a second time
    assert facade.collector.get_collection(id_).ready


def test50_reading_single_device_misbehaved():
    """the first device sending second data set before first is finished"""
    dev_names = list(facade.dev_name_index)
    # Todo: check that it also works for index 0!
    dev_name = dev_names[1]
    cnt = 5
    update(dev_name=dev_name, reading=[cnt, 10 * cnt, 100 * cnt])

    with pytest.raises(AssertionError) as ae:
        update(dev_name=dev_name, reading=[cnt, 10 * cnt, 100 * cnt])


def test001_check_stats():
    """test that data stream is assembled to combined data"""

    update(dev_name=None, reset=True)

    # ensure that all devices are active
    for dev_name in list(facade.dev_name_index):
        update(dev_name=dev_name, active=True)
        update(dev_name=dev_name, sync_stat=2)
        update(dev_name=dev_name, enabled=True, plane="x")
        update(dev_name=dev_name, enabled=True, plane="y")

    N = 3
    for cnt in range(N):
        for dev_name in list(facade.dev_name_index):
            update(dev_name=dev_name, reading=[cnt, cnt, -cnt])
            print(f"{dev_name=} {cnt=} ")

    for cnt in range(N):
        readings = facade.collector.get_collection(cnt)
        assert readings.is_ready()

    update(dev_name=None, periodic=True)


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
    L = len(facade.dev_name_index)
    # while True:
    for j in range(20000):
        for i in range(N):
            # delay = cmp_dly.get_delay().total_seconds()
            # stdout.write(
            #     f"\r{L} devices, delay before next call: {delay * 1000:6.1f} ms"
            # )
            # sleep(delay)

            cnt = next(counter)
            for dev_name in facade.dev_name_index:
                try:
                    update(dev_name=dev_name, reading=[cnt, 2*cnt, -cnt])
                except:
                    logger.error(f"{dev_name=}, {cnt=}")
                    raise

        # for cnt in range(N):
        #    readings = facade.collector.get_collection(cnt)
        #    assert readings.is_ready()


if __name__ == "__main__":
    run_performance()
