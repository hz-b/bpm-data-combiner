from ..bl.accumulator import Accumulator
from ..bl.dispatcher import DispatcherCollection
from ..bl.collector import Collector
from ..bl.monitor_devices import MonitorDevices
from ..data_model.monitored_device import MonitoredDevice

import logging
logger = logging.getLogger("bpm-data-combiner")

dev_names = ["BPM1Z1D1R", "BPM1Z2D1R"]

# Now connect all the different objects together
# ToDo: would a proper message bus simplify the code
#       I think  I would do it for the part of describing
#       interaction of collection further down
dispatcher_collection = DispatcherCollection()
monitor_devices = MonitorDevices([MonitoredDevice(name) for name in dev_names])
# ToDo: Collector should get / retrieve an updated set of valid
#       device names every time a new reading collections is created
col = Collector(devices_names=dev_names)
def cb(val):
    col.new_reading(val)
dispatcher_collection.subscribe(cb)


#: accumulate data above threshold
acc_abv_th = Accumulator(dev_names)
col.on_above_threshold.add_subscriber(acc_abv_th.add)
#: accumulate data only using items that a ready
acc_ready = Accumulator(dev_names)
col.on_ready.add_subscriber(acc_ready.add)

def process_cnt(*, dev_name, cnt):
    return dispatcher_collection.get_dispatcher(dev_name).new_reading(cnt)


def process_x_val(*, dev_name, x):
    return dispatcher_collection.get_dispatcher(dev_name).update_x_val(x)

def process_y_val(*, dev_name, y):
    return dispatcher_collection.get_dispatcher(dev_name).update_y_val(y)

def process_chk_cnt(*, dev_name, ctl):
    return dispatcher_collection.get_dispatcher(dev_name).update_check(ctl)

def process_active(*, dev_name, active):
    return monitor_devices.set_active(dev_name, active)

def process_enabled(*, dev_name, enabled):
    return monitor_devices.set_enabled(dev_name, enabled)

cmds = dict(
# handling a single reading
    cnt=process_cnt,
    x=process_x_val,
    y=process_y_val,
    ctl=process_chk_cnt,
# handling device status monitoring
    enabled=process_enabled,
    active=process_active,
)

def update(*, dev_name, **kwargs):
    """Inform the dispatcher associated to the device that new data is available

    """
    # just to get the cmd: first kwarg
    # for cmd in kwargs: break;
    # that code says it
    cmd = next(iter(kwargs))
    method = cmds[cmd]
    try:
        method(dev_name=dev_name, **kwargs)
    except Exception as exc:
        logger.error(f"Could not process command {cmd=} {method=} {dev_name=} {kwargs=}: {exc}")
        raise exc

