from ..bl.dispatcher import DispatcherCollection
from ..bl.collector import Collector
from ..bl.monitor_devices import MonitorDevices
from ..data_model.monitored_device import MonitoredDevice

import logging
logger = logging.getLogger("bpm-data-combiner")

dev_names = ["BPM1Z1D1R", "BPM1Z2D1R"]

dispatcher_collection = DispatcherCollection()
monitor_devices = MonitorDevices([MonitoredDevice(name) for name in dev_names])
col = Collector(devices_names=dev_names)
def cb(val):
    col.new_reading(val)
dispatcher_collection.subscribe(cb)


def process_cnt(*, dev_name, cnt):
    return dispatcher_collection.get_dispatcher(dev_name).new_reading(cnt)


def process_x_val(*, dev_name, x):
    return dispatcher_collection.get_dispatcher(dev_name).update_x_val(x)

def process_y_val(*, dev_name, y):
    return dispatcher_collection.get_dispatcher(dev_name).update_y_val(y)

def process_chk_cnt(*, dev_name, chk_cnt):
    return dispatcher_collection.get_dispatcher(dev_name).update_check(chk_cnt)

def process_active(*, dev_name, active):
    return monitor_devices.set_active(dev_name, active)

def process_enabled(*, dev_name, enabled):
    return monitor_devices.set_enabled(dev_name, enabled)

cmds = dict(
# handling a single reading
    cnt=process_cnt,
    x=process_x_val,
    y=process_y_val,
    cnt_chk=process_chk_cnt,
# handling device status monitoring
    enabled=process_enabled,
    active=process_active,
)

def update(*, dev_name, **kwargs):
    """Inform the dispatcher associated to the device that new data is available

    """

    cmd = list(kwargs.keys())[0]
    method = cmds[cmd]
    try:
        method(dev_name=dev_name, **kwargs)
    except Exception as exc:
        logger.error(f"Could not process command {cmd=} {method=} {dev_name=} {val=}: {exc}")
        raise exc

