from datetime import timedelta, datetime
import itertools
import pytest
from time import sleep
from sys import stdout
import logging
import pydev
from copy import copy

from bpm_data_combiner.app.main import controller as _controller
from known_devices import dev_names_bessyii as dev_names

logger = logging.getLogger("bpm-data-combiner")


def get_controller():
    controller = copy(_controller)
    controller.set_device_names(device_names=dev_names)
    # activate all devices first

    for name in controller.dev_name_index:
        controller.dev_status(name, "enabled", True)
        controller.dev_status(name, "active", True)
        controller.dev_status(name, "synchronised", 2)

    return controller



def test01_facade_set_device_names():
    ctrlr = get_controller()
    ctrlr.set_device_names([])
    assert len(ctrlr.dev_name_index) == 0
    ctrlr.set_device_names(device_names=dev_names)

    assert len(ctrlr.dev_name_index)


def test02_register_devices():
    # clear them first
    controller = get_controller()
    controller.set_device_names([])
    assert len(controller.dev_name_index) == 0
    controller.update(dev_name=None, reset=True)
    controller.update(dev_name=None, known_device_names=dev_names)
    assert len(controller.dev_name_index) == len(dev_names)
    for name, check in zip(controller.dev_name_index, dev_names):
        assert name == check


def test05_check_stats():
    """test that data stream is assembled to combined data"""
    controller = get_controller()
    assert len(controller.dev_name_index)

    controller.update(dev_name=None, reset=True)
    assert len(controller.dev_name_index)

    # ensure that all devices are active
    for dev_name in list(controller.dev_name_index):
        controller.update(dev_name=dev_name, active=True)
        controller.update(dev_name=dev_name, sync_stat=2)
        controller.update(dev_name=dev_name, enabled=True, plane="x")
        controller.update(dev_name=dev_name, enabled=True, plane="y")

    N = 3
    for cnt in range(N):
        for dev_name in list(controller.dev_name_index):
            controller.update(dev_name=dev_name, reading=[cnt, cnt, -cnt])
            print(f"{dev_name=} {cnt=} ")

    for cnt in range(N):
        readings = controller.collector.get_collection(cnt)
        assert readings.is_ready()

    controller.update(dev_name=None, periodic=True)


def test10_main_dev_monitor():
    controller = get_controller()
    controller.update(dev_name=None, reset=True)
    for dev_name in list(controller.dev_name_index):
        controller.update(dev_name=dev_name, enabled=False, plane="x")
        controller.update(dev_name=dev_name, enabled=False, plane="y")

    for dev_name in list(controller.dev_name_index):
        controller.update(dev_name=dev_name, enabled=True, plane="x")
        controller.update(dev_name=dev_name, enabled=True, plane="y")


def test20_main_behaved():
    """test that data stream is assembled to combined data"""
    controller = get_controller()

    controller.update(dev_name=None, reset=True)

    N = 3
    for cnt in range(N):
        for dev_name in list(controller.dev_name_index):
            controller.update(dev_name=dev_name, reading=[cnt, 2 * cnt, -cnt])

    for cnt in range(N):
        readings = controller.collector.get_collection(cnt)
        assert readings.is_ready()


def test30_main_interleaving():
    """Test that data are combined if the data of the devices are interleaved"""

    controller = get_controller()

    cnt = 4
    for dev_name in controller.dev_name_index:
        controller.update(dev_name=dev_name, reading=[cnt, 2 * cnt, -cnt])

    readings = controller.collector.get_collection(cnt)
    assert readings.is_ready()


def test40_monitor_collector_interaction():
    """Test that collector will still show ready for one id even if devices are marked as inactive"""
    controller = get_controller()

    for dev_name in controller.dev_name_index:
        # Make sure that all are active
        controller.update(dev_name=dev_name, active=True)

    # Send data properly
    def send_data(dev_name, cnt, val):
        controller.update(dev_name=dev_name, reading=[cnt, val, -val])

    id_ = 42
    for val, dev_name in enumerate(controller.dev_name_index):
        send_data(dev_name, id_, val)
    # All data sent.. so this should be now 1, cb evaluated once
    assert controller.collector.get_collection(42).ready

    id_ = 23
    dev_names = list(controller.dev_name_index)
    controller.update(dev_name=dev_names[0], active=False)
    for cnt, dev_name in enumerate(dev_names[1:]):
        send_data(dev_name, id_, cnt)

    # All data sent.. so the callback should have been
    # triggered a second time
    assert controller.collector.get_collection(id_).ready


def test50_reading_single_device_misbehaved():
    """the first device sending second data set before first is finished"""
    controller = get_controller()

    dev_names = list(controller.dev_name_index)
    # Todo: check that it also works for index 0!
    dev_name = dev_names[1]
    cnt = 5
    controller.update(dev_name=dev_name, reading=[cnt, 10 * cnt, 100 * cnt])

    with pytest.raises(AssertionError) as ae:
        controller.update(dev_name=dev_name, reading=[cnt, 10 * cnt, 100 * cnt])



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
    controller = get_controller()

    cmp_dly = ComputeDelay(dt=timedelta(milliseconds=100))
    N = 10
    counter = itertools.count()
    L = len(controller.dev_name_index)
    # while True:
    for j in range(20000):
        for i in range(N):
            # delay = cmp_dly.get_delay().total_seconds()
            # stdout.write(
            #     f"\r{L} devices, delay before next call: {delay * 1000:6.1f} ms"
            # )
            # sleep(delay)

            cnt = next(counter)
            for dev_name in controller.dev_name_index:
                try:
                    controller.update(dev_name=dev_name, reading=[cnt, 2*cnt, -cnt])
                except:
                    logger.error(f"{dev_name=}, {cnt=}")
                    raise

        # for cnt in range(N):
        #    readings = controller.collector.get_collection(cnt)
        #    assert readings.is_ready()


if __name__ == "__main__":
    run_performance()
