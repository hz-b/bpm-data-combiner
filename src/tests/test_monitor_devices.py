from itertools import zip_longest

from bpm_data_combiner.bl.monitor_devices import MonitorDevices
from bpm_data_combiner.data_model.monitored_device import MonitoredDevice


_devices = [MonitoredDevice("Test1"), MonitoredDevice("Test2")]


def test_monitor_enable_disable():
    mon_dev = MonitorDevices(_devices)
    # should be by default ... check method works
    mon_dev.set_enabled("Test2", True)
    for val, chk in zip(mon_dev.get_devicenames(), [dev.name for dev in _devices]):
        assert val == chk

    # disabled device removed from device names
    mon_dev.set_enabled("Test2", False)
    for val, chk in zip_longest(mon_dev.get_devicenames(), ["Test1"]):
        assert val == chk


def test_monitor_enable_disable():
    mon_dev = MonitorDevices(_devices)
    mon_dev.set_active("Test1", False)
    for val, chk in zip_longest(mon_dev.get_devicenames(), ["Test2"]):
        assert val == chk
