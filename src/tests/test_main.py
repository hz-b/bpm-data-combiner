from datetime import timedelta, datetime
import itertools
import pytest
from time import sleep
from sys import stdout
import logging

from bpm_data_combiner.app.main import update, dev_names, col

import pydev

logger = logging.getLogger("bpm-data-combiner")


def test_main_behaved():
    """test that data stream is assembled to combined data"""

    N = 3
    for cnt in range(N):
        for dev_name in dev_names:
            update(dev_name=None, cnt=cnt)
            update(dev_name=dev_name, x=cnt)
            update(dev_name=dev_name, y=-cnt)

    for cnt in range(N):
        readings = col.get_collection(cnt)
        assert readings.is_ready()

@pytest.mark.skip
def test_main_interleaving():
    """Test that data are combined if the data of the devices are interleaved

    This test makes only sense if cnt is part of the data package
    """

    cnt = 4
    for dev_name in dev_names:
        update(dev_name=dev_name, cnt=cnt)
    for dev_name in dev_names:
        update(dev_name=dev_name, x=cnt)
        update(dev_name=dev_name, y=-cnt)
    for dev_name in dev_names:
        update(dev_name=dev_name, ctl=cnt)

    readings = col.get_collection(cnt)
    assert readings.is_ready()


@pytest.mark.skip
def test_reading_single_device_misbehaved():
    """the first device sending second data set before first is finished

    This test makes only sense if cnt is part of the transmitted data set
    """
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
    L = len(dev_names)
    while True:
        for i in range(N):
            delay = cmp_dly.get_delay().total_seconds()
            stdout.write(
                f"\r{L} devices, delay before next call: {delay * 1000:6.1f} ms"
            )
            sleep(delay)

            cnt = next(counter)
            for dev_name in dev_names:
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
