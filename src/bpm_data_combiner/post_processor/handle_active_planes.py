from typing import Mapping, Union

from ..data_model.bpm_data_reading import BPMReadingPos
from ..monitor_devices.interfaces.monitored_device_status import MonitoredDeviceWithPlanesStatusInterface


class BPMReadingpos:
    pass


def pass_data_for_active_planes(x: int, y: int, device_status: MonitoredDeviceWithPlanesStatusInterface):
    if not device_status.enabled_x:
        x = None
    if not device_status.enabled_y:
        y = None
    return BPMReadingPos(x=x, y=y)
