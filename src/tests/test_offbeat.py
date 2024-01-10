import datetime

from bpm_data_combiner.bl.offbeat import OffBeatDelay


def test_offbeat_not_initalised():
    dev_names = ["test0", "test1"]
    off_beat = OffBeatDelay(name="test", device_names=dev_names)

    cnt = 0
    def cb(obj):
        nonlocal cnt
        cnt += 1
    off_beat.col.on_new_collection.add_subscriber(cb)

    for name in dev_names:
        off_beat.data_arrived(name=name)

    assert cnt == 0


def test_offbeat_behaved():
    dev_names = ["test0", "test1"]
    off_beat = OffBeatDelay(name="test", device_names=dev_names)

    n_new_cols = 0
    def cb_col_chk(obj):
        nonlocal n_new_cols
        n_new_cols += 1
    off_beat.col.on_new_collection.add_subscriber(cb_col_chk)

    delay_arrived = 0
    def cb_delay(delay):
        nonlocal  delay_arrived
        delay_arrived += 1
        
        assert isinstance(delay, datetime.timedelta)
        assert delay.total_seconds() > 0


    off_beat.on_new_delay.add_subscriber(cb_delay)

    off_beat.set_counter(1)
    for name in dev_names:
        off_beat.data_arrived(name=name)

    assert n_new_cols == 1
    assert delay_arrived == 1



