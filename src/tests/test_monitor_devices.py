from itertools import zip_longest

from bpm_data_combiner.monitor_devices.bl.monitor_device_status_collection import MonitorDeviceStatusCollection
from bpm_data_combiner.monitor_devices.bl.monitor_device_status_collection import StatusField
from bpm_data_combiner.monitor_devices.bl.monitored_device_status import MonitoredDeviceStatus

_names = ["Test1", "Test2"]


def test_monitored_device_active():
    m = MonitoredDeviceStatus("md1")
    assert not m.usable
    assert not m.active
    assert not m.synchronised
    # both planes enabled by default
    assert m.enabled
    # should flag that change was done

    assert m.update_active(True)
    # should flag that change was done
    assert m.update_synchronised(1)
    # but still not usable
    assert not m.usable

    # now synchronised
    assert m.update_synchronised(2)
    # thus usable
    assert m.usable

def test_get_devices():
    mon_dev = MonitorDeviceStatusCollection(_names)

    for name in _names:
        # should flag that an update was required
        assert mon_dev.update(name, "active", True)
    names = mon_dev.get_device_names()
    assert len(names) == 0

    # only if synchronised and active they are considered
    for name in _names:
        # should flag that an update was required
        assert mon_dev.update(name, "synchronised",  2)

    names = mon_dev.get_device_names()
    assert len(names) == 2


def test_monitor_enable_disable():
    mon_dev = MonitorDeviceStatusCollection(_names)

    # should be enabled by default ... check method works, and flags no change
    assert not mon_dev.update("Test2", StatusField.enabled, True)
    md2 = mon_dev.devices_status["Test2"]
    assert md2.enabled
    assert md2.enabled_x
    assert md2.enabled_y
    md1 = mon_dev.devices_status["Test2"]
    assert md1.enabled
    assert md1.enabled_x
    assert md1.enabled_y

    assert mon_dev.update("Test2", StatusField.enabled, False)
    md4 = mon_dev.devices_status["Test2"]
    assert not md4.enabled
    assert not md4.enabled_x
    assert not md4.enabled_y
    md3 = mon_dev.devices_status["Test1"]
    assert md3.enabled
    assert md3.enabled_x
    assert md3.enabled_y

    assert mon_dev.update("Test2", StatusField.enabled_y, True)
    md6 = mon_dev.devices_status["Test2"]
    assert md6.enabled
    assert not md6.enabled_x
    assert md6.enabled_y



def test_monitor_active():
    mon_dev = MonitorDeviceStatusCollection(_names)
    assert not mon_dev.devices_status["Test1"].active

    # should signal update
    assert mon_dev.update("Test1", "active", True)
    assert mon_dev.devices_status["Test1"].active
    assert not mon_dev.devices_status["Test2"].active

    # should not signal update
    assert not mon_dev.update("Test1", StatusField.active, True)
    assert mon_dev.devices_status["Test1"].active
    assert not mon_dev.devices_status["Test2"].active

def test_monitor_synchronised():
    mon_dev = MonitorDeviceStatusCollection(_names)
    for _, md in mon_dev.devices_status.items():
        assert md.enabled
        assert not md.active
        assert md.synchronised == 0
        assert not md.usable
    del md

    assert mon_dev.update("Test1", "synchronised", 2)
    md1 = mon_dev.devices_status["Test1"]
    assert md1.enabled
    assert not md1.active
    assert not md1.usable
    assert md1.synchronised

    md2 = mon_dev.devices_status["Test2"]
    assert md2.enabled
    assert not md2.active
    assert not md2.usable
    assert not md2.synchronised

def test_monitor_usable():
    mon_dev = MonitorDeviceStatusCollection(_names)
    assert mon_dev.update("Test2", "active", True)
    assert not mon_dev.update("Test2", StatusField.active, True)
    assert mon_dev.update("Test2", "synchronised", 2)
    for val, chk in zip_longest(mon_dev.get_device_names(), ["Test2"]):
        assert val == chk
