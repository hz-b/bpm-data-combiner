import io
import itertools
import logging
import traceback
from typing import Optional

from ..bl.statistics import compute_mean_weights_for_planes
from ..data_model.bpm_data_accumulation import BPMDataAccumulation
from ..data_model.monitored_device import MonitoredDevice
from ..bl.event import Event
from ..bl.accumulator import Accumulator
from ..bl.collector import Collector, collection_to_bpm_data_collection
from ..bl.dispatcher import DispatcherCollection
from ..bl.monitor_devices import MonitorDevices
from ..bl.offbeat import OffBeatDelay
from ..bl.preprocessor import PreProcessor
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
devices_status=[MonitoredDevice(name) for name in dev_names]
monitor_devices = MonitorDevices(devices_status=devices_status)
preprocessor = PreProcessor(devices_status=devices_status)
col = Collector(name="data_collector", devices_names=dev_names)
# fmt:off
def update_device_names(device_names):
    """update collector on valid device names"""
    col.device_names = device_names
monitor_devices.on_status_change.add_subscriber(update_device_names)
# fmt:on

# preprocessor: set x or y to None if disabled
dispatcher_collection.subscribe(lambda reading: col.new_reading(preprocessor.preprocess(reading)))

# Off beat treats each plane as separate device
offbeat_delay = OffBeatDelay(
    name="offbeat_delay_collector",
    device_names=list(
        itertools.chain(*[(name + ":x", name + ":y") for name in _dev_names])
    ),
)


#: accumulate data above threshold
acc_abv_th = Accumulator(dev_names)
col.on_above_threshold.add_subscriber(acc_abv_th.add)
#: accumulate data only using items that a ready
acc_ready = Accumulator(dev_names)
col.on_ready.add_subscriber(acc_ready.add)

# fmt:off
viewer = Viewer(prefix="Pierre:COM")
def cb(collection):
    # Here we need to use dev_names and not the active ones
    # I guss there should be an exporter
    data = collection_to_bpm_data_collection(collection, dev_names)
    viewer.ready_data.update(data)
col.on_ready.add_subscriber(cb)
# fmt:on


def cb_periodic_update_accumulated_above_threshold(cnt : Optional[int]):
    """
    """
    viewer.periodic_data.update(compute_mean_weights_for_planes(acc_abv_th.get()))


# could do that directly too ... but appetite comes with eating
# so let's have a common point to see what all shall be processed
# at this point
periodic_event = Event(name="periodic_update_2sec")
periodic_event.add_subscriber(cb_periodic_update_accumulated_above_threshold)


def process_cnt(*, dev_name, cnt):
    return dispatcher_collection.get_dispatcher(dev_name).new_reading(cnt)


def process_x_val(*, dev_name, x):
    offbeat_delay.data_arrived(name=f"{dev_name}:x")
    return dispatcher_collection.get_dispatcher(dev_name).update_x_val(x)


def process_y_val(*, dev_name, y):
    offbeat_delay.data_arrived(name=f"{dev_name}:y")
    return dispatcher_collection.get_dispatcher(dev_name).update_y_val(y)


def process_chk_cnt(*, dev_name, ctl):
    return dispatcher_collection.get_dispatcher(dev_name).update_check(ctl)


def process_active(*, dev_name, active):
    return monitor_devices.set_active(dev_name, active)


def process_enabled(*, dev_name, enabled, plane):
    return monitor_devices.set_enabled(dev_name, enabled, plane)


def process_offbeat(*, dev_name, metronom, type):
    """

    Todo:
        fix offbeat_delay
    """
    assert dev_name is None
    key, val = type, metronom

    if key == "tick":
        offbeat_delay.set_counter(val)
    elif key == "delay":
        offbeat_delay.set_delay(val)
    else:
        raise ValueError(f"Unknown {key=} with {val=}")

def process_periodic_trigger(*, dev_name, periodic):
    periodic_event.trigger(periodic)


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
    periodic=process_periodic_trigger
)


class UpdateContext:
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
        tb_buf = io.StringIO()
        traceback.print_tb(exc_tb, file=tb_buf)
        tb_buf.seek(0)
        logger.error("%s\nTraceback:\n%s\n%s\n", marker, tb_buf.read(), marker)


def update(*, dev_name, **kwargs):
    """Inform the dispatcher associated to the device that new data is available"""
    # just to get the cmd: first kwarg
    # for cmd in kwargs: break;
    # that code says it
    cmd = next(iter(kwargs))
    method = cmds[cmd]
    with UpdateContext(cmd=cmd, method=method, dev_name=dev_name, kwargs=kwargs):
        method(dev_name=dev_name, **kwargs)
