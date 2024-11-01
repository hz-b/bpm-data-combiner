from dataclasses import dataclass
from typing import Hashable

import pytest

from collector import CollectionItemInterface, Collector, DoubleSubmissionError
from collector.bl.collection_for_one_id import CollectionForOneId

@dataclass
class ColItem(CollectionItemInterface):
    x: int
    y: int
    cnt: int
    name : str

    @property
    def identifier(self) -> Hashable:
        return self.cnt

    @property
    def source(self) -> Hashable:
        return self.name

def test_collector_behaving():
    dev_names = ["BPMZ1D1R", "BPMZ2D1R", "BPMZ4D1R", "BPMZ1T2R"]

    col = Collector(devices_names=dev_names)
    # check that it works
    repr(col)

    cnt = 7
    rc = col.new_item(ColItem(cnt=cnt, x=3, y=4, name=dev_names[0]))
    # assert that the new reading issued a callback
    rc_check = col.get_collection(cnt)
    # check that it works
    repr(rc)
    assert rc == rc_check

    assert isinstance(rc, CollectionForOneId)
    assert rc.ready == False
    assert rc.above_threshold == False

    col.new_item(ColItem(cnt=cnt, x=11, y=13, name=dev_names[1]))
    col.new_item(ColItem(cnt=cnt, x=17, y=19, name=dev_names[2]))
    assert rc.ready == False
    assert rc.above_threshold == True

    col.new_item(ColItem(cnt=cnt, x=17, y=19, name=dev_names[-1]))
    assert rc.ready == True
    assert rc.above_threshold == True

    data = rc.data()

    # and check again
    assert len(repr(rc)) > 0
    assert len(repr(col)) > 0


def test_collector_double_submission():
    dev_names = ["BPMZ1D1R", "BPMZ2D1R", "BPMZ4D1R", "BPMZ1T2R"]
    col = Collector(devices_names=dev_names)
    cnt = -19
    col.new_item(ColItem(cnt=cnt, x=3, y=4, name=dev_names[0]))

    with pytest.raises(DoubleSubmissionError):
        col.new_item(ColItem(cnt=cnt, x=3, y=4, name=dev_names[0]))
    pass


def test_collector_invalid_submission():
    dev_names = ["BPMZ1D1R", "BPMZ2D1R", "BPMZ4D1R", "BPMZ1T2R"]
    col = Collector(devices_names=dev_names)
    cnt = 23

    with pytest.raises(AssertionError):
        col.new_item(ColItem(cnt=cnt, x=3, y=4, name="Q1M1"))
