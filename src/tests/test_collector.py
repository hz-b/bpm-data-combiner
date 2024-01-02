import pytest

from bpm_data_combiner.bl.collector import Collector, ReadingsCollection
from bpm_data_combiner.data_model.bpm_data_reading import BPMReading


def test_collector_behaving():
    dev_names = ["BPMZ1D1R", "BPMZ2D1R", "BPMZ4D1R", "BPMZ1T2R"]
    col = Collector(devices_names=dev_names)

    cnt = 7
    col.new_reading(BPMReading(cnt=cnt, x=3, y=4, dev_name=dev_names[0]))
    rc = col.get_collection(cnt)

    assert isinstance(rc, ReadingsCollection)
    assert rc.ready == False
    assert rc.above_threshold == False

    col.new_reading(BPMReading(cnt=cnt, x=11, y=13, dev_name=dev_names[1]))
    col.new_reading(BPMReading(cnt=cnt, x=17, y=19, dev_name=dev_names[-1]))
    assert rc.ready == False
    assert rc.above_threshold == True

    col.new_reading(BPMReading(cnt=cnt, x=17, y=19, dev_name=dev_names[-2]))
    assert rc.ready == True
    assert rc.above_threshold == True


def test_collector_double_submission():
    dev_names = ["BPMZ1D1R", "BPMZ2D1R", "BPMZ4D1R", "BPMZ1T2R"]
    col = Collector(devices_names=dev_names)
    cnt = -19
    col.new_reading(BPMReading(cnt=cnt, x=3, y=4, dev_name=dev_names[0]))

    with pytest.raises(AssertionError):
        col.new_reading(BPMReading(cnt=cnt, x=3, y=4, dev_name=dev_names[0]))


def test_collector_invalid_submission():
    dev_names = ["BPMZ1D1R", "BPMZ2D1R", "BPMZ4D1R", "BPMZ1T2R"]
    col = Collector(devices_names=dev_names)
    cnt = 23

    with pytest.raises(AssertionError):
        col.new_reading(BPMReading(cnt=cnt, x=3, y=4, dev_name="Q1M1"))
