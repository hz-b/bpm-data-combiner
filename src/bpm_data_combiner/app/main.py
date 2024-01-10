import itertools
import logging

from ..data_model.monitored_device import MonitoredDevice
from ..bl.accumulator import Accumulator
from ..bl.dispatcher import DispatcherCollection
from ..bl.collector import Collector, collection_to_bpm_data_collection
from ..bl.monitor_devices import MonitorDevices
from .offbeat import OffBeatDelay
from .viewer import Viewer
from pandas import Index

from ..data_model.timestamp import DataArrived

logger = logging.getLogger("bpm-data-combiner")

#: Todo where to get the device names from
dev_names = [
    [
        [
            [f"BPM{cnt}Z{child}{sec_type}{sec}R" for cnt in range(1, 4 + 1)]
            for child in range(1, 4 + 1)
        ]
        for sec_type in ("D", "T")
    ]
    for sec in range(1, 8 + 1)
]

_dev_names = list(itertools.chain(*itertools.chain(*itertools.chain(*dev_names))))
dev_names = Index(_dev_names)
# Now connect all the different objects together
# ToDo: would a proper message bus simplify the code
#       I think  I would do it for the part of describing
#       interaction of collection further down
dispatcher_collection = DispatcherCollection()
monitor_devices = MonitorDevices([MonitoredDevice(name) for name in dev_names])
# ToDo: Collector should get / retrieve an updated set of valid
#       device names every time a new reading collections is created
col = Collector(devices_names=dev_names)
offbeat_delay = OffBeatDelay(device_names=_dev_names)


def cb(val):
    col.new_reading(val)

dispatcher_collection.subscribe(cb)


#: accumulate data above threshold
acc_abv_th = Accumulator(dev_names)
col.on_above_threshold.add_subscriber(acc_abv_th.add)
#: accumulate data only using items that a ready
acc_ready = Accumulator(dev_names)
# col.on_ready.add_subscriber(acc_ready.add)

viewer = Viewer(prefix="Pierre:COM")


def cb(collection):
    data = collection_to_bpm_data_collection(collection, dev_names)
    viewer.ready_data.update(data)


col.on_ready.add_subscriber(cb)


def process_cnt(*, dev_name, cnt):
    return dispatcher_collection.get_dispatcher(dev_name).new_reading(cnt)


def process_x_val(*, dev_name, x):
    offbeat_delay.data_arrived(dev_name=dev_name, plane="x")
    return dispatcher_collection.get_dispatcher(dev_name).update_x_val(x)


def process_y_val(*, dev_name, y):
    offbeat_delay.data_arrived(dev_name=dev_name, plane="x")
    return dispatcher_collection.get_dispatcher(dev_name).update_y_val(y)


def process_chk_cnt(*, dev_name, ctl):
    return dispatcher_collection.get_dispatcher(dev_name).update_check(ctl)


def process_active(*, dev_name, active):
    return monitor_devices.set_active(dev_name, active)


def process_enabled(*, dev_name, enabled):
    return monitor_devices.set_enabled(dev_name, enabled)


def process_offbeat(*, dev_name, metronom, type):
    """

    Todo:
        fix offbead_delay
    """
    assert dev_name is None
    key, val = type, metronom
    # return
    # print(f"          metronom {key=} with {val=}")

    if key == "tick":
        offbeat_delay.set_counter(val)
    elif key == "delay":
        offbeat_delay.set_delay(val)
    else:
        raise ValueError(f"Unknown {key=} with {val=}")
    # print(f"processed metronom {key=} with {val=}")


cmds = dict(
    # handling a single reading
    cnt=process_cnt,
    x=process_x_val,
    y=process_y_val,
    ctl=process_chk_cnt,
    # handling device status monitoring
    enabled=process_enabled,
    active=process_active,
    # metronom: used to derive appropriate delay
    # to wait for all data
    metronom=process_offbeat,
)

class UpdateContex:
    def __init__(self, *, cmd, method, dev_name, kwargs):
        self.cmd = cmd
        self.method = method
        self.dev_name = dev_name
        self.kwargs = kwargs
    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            return
        logger.error(
            f"Could not process command {self.cmd=}:"
            f"{self.method=} {self.dev_name=} {self.kwargs=}: {exc_type}({exc_val})"
        )
        marker = "-" * 78
        logger.error("%s\nTraceback:\n%s\n%s\n", marker, exc_tb, marker)





def update(*, dev_name, **kwargs):
    """Inform the dispatcher associated to the device that new data is available"""
    # just to get the cmd: first kwarg
    # for cmd in kwargs: break;
    # that code says it
    cmd = next(iter(kwargs))
    method = cmds[cmd]
    with UpdateContex(cmd=cmd, method=method, dev_name=dev_name, kwargs=kwargs):
        method(dev_name=dev_name, **kwargs)
