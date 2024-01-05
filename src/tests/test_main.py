import pytest
from bpm_data_combiner.app.main import update, dev_names, col

device_names = ["Test001", "Test002"]


def test_main_behaved():
    """test that data stream is assembled to combined data
    """

    N = 3
    for cnt in range(N):
        for dev_name in dev_names:
            update(dev_name=dev_name, cnt=cnt)
            update(dev_name=dev_name, x=cnt)
            update(dev_name=dev_name, y=-cnt)
            update(dev_name=dev_name, ctl=cnt)

    for cnt in range(N):
        readings = col.get_collection(cnt)
        assert readings.is_ready()


def test_main_interleaving():
    """Test that data are combined if the data of the devices are interleaved
    """

    cnt = 4
    for dev_name in dev_names: update(dev_name=dev_name, cnt=cnt)
    for dev_name in dev_names:
        update(dev_name=dev_name, x=cnt)
        update(dev_name=dev_name, y=-cnt)
    for dev_name in dev_names:
        update(dev_name=dev_name, ctl=cnt)

    readings = col.get_collection(cnt)
    assert readings.is_ready()


def test_reading_single_device_misbehaved():
    """the first device sending second data set before first is finished
    """
    dev_name = dev_names[0]
    cnt = 5
    update(dev_name=dev_name, cnt=cnt)
    update(dev_name=dev_name, x=-10 * cnt)
    update(dev_name=dev_name, y=-100 * cnt)

    with pytest.raises(AssertionError) as ae:
        update(dev_name=dev_name, cnt=cnt +1)
