"""

Todo:
   add a reset command
"""
import io
import itertools
import logging
import traceback
from typing import Optional, Sequence, Mapping

from .command_context_manager import UpdateContext
from ..bl.accumulator import Accumulator
from ..bl.collector import Collector, collection_to_bpm_data_collection
from ..bl.command_round_buffer import CommandRoundBuffer
from ..bl.dispatcher import DispatcherCollection
from ..bl.event import Event
from ..bl.monitor_devices import MonitorDevices
from ..bl.preprocessor import PreProcessor
from ..bl.statistics import compute_mean_weights_for_planes
from ..data_model.bpm_data_accumulation import BPMDataAccumulation
from ..data_model.bpm_data_reading import BPMReading
from ..data_model.monitored_device import MonitoredDevice
from ..data_model.command import Command
from .view import Views

import numpy as np
from datetime import datetime


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

dev_name_index = {name: idx for idx, name in enumerate(_dev_names)}
print(f"Known devices {list(dev_name_index)}")
# Now connect all the different objects together
# ToDo: would a proper message bus simplify the code
#       I think  I would do it for the part of describing
#       interaction of collection further down
dispatcher_collection = DispatcherCollection()
monitor_devices = MonitorDevices([MonitoredDevice(name) for name in dev_name_index])
# fmt:off
preprocessor = PreProcessor(devices_status=monitor_devices.devices_status)
def update_device_names(device_names: Sequence[str]):
    """
    Todo: check that device n
    """
    col.device_names = device_names
    preprocessor.device_names = device_names
monitor_devices.on_status_change.add_subscriber(update_device_names)
# fmt:on

# ToDo: Collector should get / retrieve an updated set of valid
#       device names every time a new reading collections is created
col = Collector(name="data_collector", devices_names=list(dev_name_index), max_collections=10)
# preprocessor: set x or y to None if disabled
dispatcher_collection.subscribe(lambda reading: col.new_reading(preprocessor.preprocess(reading)))

#: accumulate data above threshold
# acc_abv_th = Accumulator(dev_name_index)
# col.on_above_threshold.add_subscriber(acc_abv_th.add)
#: accumulate data only using items that a ready
acc_ready = Accumulator(dev_name_index)
col.on_ready.add_subscriber(acc_ready.add)


# fmt:off
views = Views(prefix="Pierre:COM")
def cb(collection):
    # Here we need to use dev_names and not the active ones
    # I guss there should be an exporter
    data = collection_to_bpm_data_collection(collection, dev_name_index)
    views.ready_data.update(data)
col.on_ready.add_subscriber(cb)
# fmt:on
def cb(names):
    logger.debug("Monitoring devics, active ones: %s", names)
    views.monitor_bpms.update(names, np.ones(len(names), bool))

monitor_devices.on_status_change.add_subscriber(cb)


def cb_periodic_update_accumulated_ready(cnt : Optional[int]):
    """
    """
    views.periodic_data.update(compute_mean_weights_for_planes(acc_ready.get()))


# could do that directly too ... but appetite comes with eating
# so let's have a common point to see what all shall be processed
# at this point
periodic_event = Event(name="periodic_update_2sec")
periodic_event.add_subscriber(cb_periodic_update_accumulated_ready)


def process_cnt(*, dev_name, cnt):
    return dispatcher_collection.get_dispatcher(dev_name).new_reading(cnt)


def process_x_val(*, dev_name, x):
    return dispatcher_collection.get_dispatcher(dev_name).update_x_val(x)


def process_y_val(*, dev_name, y):
    return dispatcher_collection.get_dispatcher(dev_name).update_y_val(y)


def process_chk_cnt(*, dev_name, ctl):
    return dispatcher_collection.get_dispatcher(dev_name).update_check(ctl)

def process_reading(*, dev_name, reading):
    cnt, x, y = reading
    return col.new_reading(
        preprocessor.preprocess(BPMReading(dev_name=dev_name, x=x, y=y, cnt=cnt))
    )


def process_active(*, dev_name, active):
    return monitor_devices.set_active(dev_name, active)


def process_enabled(*, dev_name, enabled, plane):
    return monitor_devices.set_enabled(dev_name, enabled, plane)


def process_periodic_trigger(*, dev_name, periodic: Mapping):
    periodic_event.trigger(periodic)

def process_reset(*, dev_name, reset):
    dispatcher_collection.reset()
    col.reset()

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
    periodic=process_periodic_trigger,
    # reset all internal states
    reset=process_reset,
    reading=process_reading
)

rbuffer = CommandRoundBuffer(maxsize=50)


def update(*, dev_name, tpro=False, **kwargs):
    """Inform the dispatcher associated to the device that new data is available"""
    # just to get the cmd: first kwarg
    # for cmd in kwargs: break;
    # that code says it

    cmd = next(iter(kwargs))
    method = cmds[cmd]
    dc = Command(cmd=cmd, dev_name=dev_name, kwargs=kwargs, timestamp=datetime.now())
    rbuffer.append(dc)
    with UpdateContext(method=method, rbuffer=rbuffer, view=views.monitor_update_cmd_errors):
        method(dev_name=dev_name, **kwargs)
