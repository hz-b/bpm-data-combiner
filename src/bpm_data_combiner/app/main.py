"""

Todo:
   add a reset command
"""


from typing import Optional, Sequence, Mapping

from .command_context_manager import UpdateContext
from ..bl.accumulator import Accumulator
from ..bl.collector import Collector, ReadingsCollection, collection_to_bpm_data_collection
from ..bl.command_round_buffer import CommandRoundBuffer
from ..bl.dispatcher import DispatcherCollection
from ..bl.event import Event
from ..bl.logger import logger
from ..bl.monitor_devices import MonitorDevicesStatus
from bpm_data_combiner.monitor_devices.bl.monitor_synchronisation import MonitorDeviceSynchronisation, offset_from_median
from ..bl.preprocessor import PreProcessor
from ..bl.statistics import compute_mean_weights_for_planes
from ..data_model.bpm_data_reading import BPMReading
from ..data_model.monitored_device import MonitoredDevice
from ..data_model.command import Command
from .config import Config
from .view import Views
from .known_devices import dev_names as _dev_names
from datetime import datetime
import sys

stream = sys.stdout

config = Config()
def cb(flag):
    views.configuration.update(flag)
config.on_median_computation_request.add_subscriber(cb)

dev_name_index = {name: idx for idx, name in enumerate(_dev_names)}
print(f"Known devices {list(dev_name_index)}")
# Now connect all the different objects together
# ToDo: would a proper message bus simplify the code
#       I think  I would do it for the part of describing
#       interaction of collection further down
dispatcher_collection = DispatcherCollection()
monitor_devices = MonitorDevicesStatus([MonitoredDevice(name) for name in dev_name_index])
monitor_device_synchronisation = MonitorDeviceSynchronisation(monitored_devices=monitor_devices)
def process_mon_sync(data):
    if config.do_median_computation:
        # needs roughly half of the CPU ... only switch it on by request
        views.monitor_device_sync.update(*offset_from_median(data))
monitor_device_synchronisation.on_new_index.add_subscriber(process_mon_sync)
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
col = Collector(
    name="data_collector", devices_names=list(dev_name_index), max_collections=10
)
# fmt:off
def update_collection_number(r: ReadingsCollection):
    logger.info("collector new readings collection with number %d", r.id_)
    # sys.stdout.write(f"collector new readings collection with number  {r.cnt}")
    # sys.stdout.flush()
    views.collector.update(r.id_)
col.on_new_collection.add_subscriber(update_collection_number)
# fmt:on
# preprocessor: set x or y to None if disabled
dispatcher_collection.subscribe(
    lambda reading: col.new_collection(preprocessor.preprocess(reading))
)

#: accumulate data above threshold
# acc_abv_th = Accumulator(dev_name_index)
# col.on_above_threshold.add_subscriber(acc_abv_th.add)
#: accumulate data only using items that a ready
acc_ready = Accumulator(dev_name_index)


# fmt:off
views = Views(prefix="OrbCol")
def cb(collection):
    # Here we need to use dev_names and not the active ones
    # I guss there should be an exporter
    for _, item in collection.items():
        logger.debug("new ready collection %s", item.id_)
        break
    data = collection_to_bpm_data_collection(collection, dev_name_index, default_value=0)
    logger.debug("adding data %s", data)
    acc_ready.add(data)
    views.ready_data.update(data)
col.on_ready.add_subscriber(cb)
# col.on_ready.add_subscriber(acc_ready.add)
# fmt:on


# fmt:off
def cb(names):
    logger.debug("Monitoring devices, active ones: %s", names)
    views.monitor_bpms.update(
        names=[ds.name for _, ds in monitor_devices.devices_status.items()],
        active=[ds.active for _, ds in monitor_devices.devices_status.items()],
        synchronised=[ds.synchronised for _, ds in monitor_devices.devices_status.items()],
        usable=[ds.usable for _, ds in monitor_devices.devices_status.items()],
    )
monitor_devices.on_status_change.add_subscriber(cb)
# fmt:on


# fmt:off
def cb_periodic_update_accumulated_ready(cnt : Optional[int]):
    """
    """
    stat_data = compute_mean_weights_for_planes(acc_ready.get())
    views.periodic_data.update(stat_data)
    logger.debug("pushing stat data to bdata_view")
    views.bdata.update(stat_data)
    logger.debug("pushing stat data to bdata_view done")

# could do that directly too ... but appetite comes with eating
# so let's have a common point to see what all shall be processed
# at this point
periodic_event = Event(name="periodic_update_2sec")
periodic_event.add_subscriber(cb_periodic_update_accumulated_ready)
# fmt:on


def process_reading(*, dev_name, reading):
    cnt, x, y = reading
    logger.debug(f"new reading for dev %s cnt %s", dev_name, cnt)
    monitor_device_synchronisation.add_new_count(dev_name, cnt)
    return col.new_collection(
        preprocessor.preprocess(BPMReading(dev_name=dev_name, x=x, y=y, cnt=cnt))
    )


def process_active(*, dev_name, active):
    r = monitor_devices.set_active(dev_name, active)
    return r

def process_sync_stat(*, dev_name, sync_stat, tpro=False):
    r = monitor_devices.set_synchronisation_status(dev_name, sync_stat)
    r = r or sync_stat
    if tpro:
        stat = monitor_devices.devices_status[dev_name]
        stream.write(f"{dev_name=} {sync_stat=} {r=} {stat=}\n")
        stream.flush()
    return r


def process_enabled(*, dev_name, enabled, plane):
    return monitor_devices.set_enabled(dev_name, enabled, plane)


def process_periodic_trigger(*, dev_name, periodic: Mapping):
    periodic_event.trigger(periodic)


def process_reset(*, dev_name, reset):
    dispatcher_collection.reset()
    col.reset()

def process_compute_median(*, dev_name, cfg_comp_median):
    config.request_median_computation(cfg_comp_median)

cmds = dict(
    # handling a single reading
    cnt=process_cnt,
    x=process_x_val,
    y=process_y_val,
    ctl=process_chk_cnt,
    # handling device status monitoring
    enabled=process_enabled,
    active=process_active,
    sync_stat=process_sync_stat,
    # metronom: used to derive appropriate delay
    # to wait for all data
    periodic=process_periodic_trigger,
    # reset all internal states
    reset=process_reset,
    reading=process_reading,
    cfg_comp_median=process_compute_median,
)

rbuffer = CommandRoundBuffer(maxsize=50)


def update(*, dev_name, tpro=False, **kwargs):
    """Inform the dispatcher associated to the device that new data is available"""
    # just to get the cmd: first kwarg
    # for cmd in kwargs: break;
    # that code says it

    # if tpro:
    #    sys.stdout.write(f" update(dev_name {dev_name}, kwargs {kwargs})\n")
    #    sys.stdout.flush()

    cmd = next(iter(kwargs))
    method = cmds[cmd]
    try:
        dc = Command(
            cmd=cmd, dev_name=dev_name, kwargs=kwargs, timestamp=datetime.now()
        )
        rbuffer.append(dc)
    except:
        logger.error("Failed to prepare wrapper info")
        raise
    r = None
    with UpdateContext(
        method=method,
        rbuffer=rbuffer,
        view=views.monitor_update_cmd_errors,
        only_buffer=not bool(tpro),
    ):
        r = method(dev_name=dev_name, **kwargs)

    # todo: does pydevice expects a return on the function ?
    # logger.info(f" update(dev_name {dev_name}, kwargs {kwargs}) succeded\n")
    if r is None:
        r = kwargs.get("val", True)
    return r


__all__ = ["update"]
