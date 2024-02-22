"""

Todo:
   add a reset command
"""
import io
import itertools
import logging
import traceback
from typing import Optional

from ..bl.statistics import compute_mean_weights_for_planes
from ..data_model.bpm_data_accumulation import BPMDataAccumulation
from ..data_model.monitored_device import MonitoredDevice
from ..data_model.command import Command
from ..bl.accumulator import Accumulator
from ..bl.collector import Collector, collection_to_bpm_data_collection
from ..bl.dispatcher import DispatcherCollection
from ..bl.monitor_devices import MonitorDevices
from ..bl.offbeat import OffBeatDelay
from ..bl.command_round_buffer import CommandRoundBuffer
from .view import Views

import numpy as np
from pandas import Index
from datetime import datetime

from ..data_model.timestamp import DataArrived

logger = logging.getLogger("bpm-data-combiner")

#: Todo where to get the device names from
_dev_names = [
    "BPMZ5D8R",
    "BPMZ6D8R",
    "BPMZ7D8R",

    "BPMZ1T8R",
    "BPMZ2T8R",
    "BPMZ3T8R",
    "BPMZ4T8R",

]

# _dev_names = list(itertools.chain(*itertools.chain(*itertools.chain(*dev_names))))
dev_names = Index(_dev_names)
print(f"Known devices {dev_names=}")
# Now connect all the different objects together
# ToDo: would a proper message bus simplify the code
#       I think  I would do it for the part of describing
#       interaction of collection further down
dispatcher_collection = DispatcherCollection()
monitor_devices = MonitorDevices([MonitoredDevice(name) for name in dev_names])
# ToDo: Collector should get / retrieve an updated set of valid
#       device names every time a new reading collections is created
col = Collector(name="data_collector", devices_names=dev_names, max_collections=10)
dispatcher_collection.subscribe(col.new_reading)


# fmt:off
def update_device_names(device_names):
    """
    Todo:
        Do I need to mangle the names for a real device
    """
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
# col.on_above_threshold.add_subscriber(acc_abv_th.add)
#: accumulate data only using items that a ready
acc_ready = Accumulator(dev_names)
col.on_ready.add_subscriber(acc_ready.add)


# fmt:off
viewer = Views(prefix="Pierre:COM")
def cb(collection):
    # Here we need to use dev_names and not the active ones
    # I guss there should be an exporter
    data = collection_to_bpm_data_collection(collection, dev_names)
    viewer.ready_data.update(data)
col.on_ready.add_subscriber(cb)
# fmt:on
def cb(names):
    logger.debug("Monitoring devics, active ones: %s", names)
    viewer.monitor_bpms.update(names, np.ones(len(names), bool))

monitor_devices.on_status_change.add_subscriber(cb)


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

def process_guard(*, dev_name, guard):
    """Does it help to remove double calls to ctl
    """
    pass


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
    guard=process_guard,
    # handling device status monitoring
    enabled=process_enabled,
    active=process_active,
    # metronom: used to derive appropriate delay
    # to wait for all data
    metronom=process_offbeat,
    periodic=process_periodic_trigger
)


def dict_to_string(d: dict):
    tmp = ", ".join([f"{k}:{v}" for k,v in d.items()])
    return "{" + tmp + "}"


def round_buffer_to_string(rb: CommandRoundBuffer):
    def stringify_command(cmd):
        tmp = dict_to_string(cmd.kwargs)
        tmp = f"{cmd.dev_name:8s} {tmp}"
        return  f"{tmp:39s}"
    return [stringify_command(cmd) for cmd in list(rb.roundbuffer)[::-1]]



class UpdateContext:
    def __init__(self, *, method, rbuffer):
        self.method = method
        self.roundbuffer = rbuffer

    def __enter__(self):
        return

        last = self.roundbuffer.last()

        cmd = " %8s: cmd %4s, kw%s" %( last.dev_name,  last.cmd, dict_to_string(last.kwargs))
        logger.warning(
            "Processing dev_name %8s, command %4s, kwargs = %s", last.dev_name,  last.cmd, last.kwargs
        )

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            return

        viewer.monitor_update_cmd_errors.update(
            [f"ERR: {exc_type}", f"ERR {exc_val})"] + round_buffer_to_string(self.roundbuffer)
        )
        return

        last = self.roundbuffer.last()
        txt = f" {last.cmd:6s} {dict_to_string(last.kwargs)}: {exc_type}({exc_val})"
        # logger.error(self.roundbuffer)
        logger.error("Could not process command:" + txt)

        logger.error(
            f"Could not process command {self.cmd=}:"
            f"{self.method=} {self.dev_name=} {self.kwargs=}: {exc_type}({exc_val})"
        )

        marker = "-" * 78
        tb_buf = io.StringIO()
        traceback.print_tb(exc_tb, file=tb_buf)
        tb_buf.seek(0)
        logger.error("%s\nTraceback:\n%s\n%s\n", marker, tb_buf.read(), marker)


rbuffer = CommandRoundBuffer(maxsize=50)


def update(*, dev_name, **kwargs):
    """Inform the dispatcher associated to the device that new data is available"""
    # just to get the cmd: first kwarg
    # for cmd in kwargs: break;
    # that code says it

    cmd = next(iter(kwargs))
    method = cmds[cmd]
    dc = Command(cmd=cmd, dev_name=dev_name, kwargs=kwargs, timestamp=datetime.now())
    rbuffer.append(dc)
    with UpdateContext(method=method, rbuffer=rbuffer):
        method(dev_name=dev_name, **kwargs)
