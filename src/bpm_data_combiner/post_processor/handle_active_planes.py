from typing import Mapping

from ..data_model.bpm_data_reading import BPMReading
from ..monitor_devices.interfaces.monitored_device_status import MonitoredDeviceWithPlanesStatusInterface


def pass_data_for_active_planes(cnt: int, x: int, y: int, device_status: MonitoredDeviceWithPlanesStatusInterface):
    if not device_status.enabled_x:
        x = None
    if not device_status.enabled_y:
        y = None
    return BPMReading(dev_name=device_status.name, x=x, y=y, cnt=cnt)
