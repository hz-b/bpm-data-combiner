from bpm_data_combiner.monitor_devices import MonitorDevicesStatus, MonitorDeviceSynchronisation

names = ["Test1", "Test2"]

def test_synchronisation():
    mon_dev = MonitorDevicesStatus(names)
    ms = MonitorDeviceSynchronisation(mon_dev)
    ref_val = 42
    [ms.add_new_count(dev_name=name, reading_index=ref_val) for name in names]
    median, offset = ms.offset_from_median()
    assert median == ref_val
    assert (offset == 0).all()
