from typing import Mapping

from bpm_data_combiner.data_model.bpm_data_reading import BPMReading
from bpm_data_combiner.monitor_devices.data_model.monitored_device import MonitoredDevice


def pass_data_for_active_planes(cnt: int, x: int, y: int, device_status: MonitoredDevice):
    if not device_status.enabled_x:
        x = None
    if not device_status.enabled_y:
        y = None
    return BPMReading(dev_name=device_status.name, x=x, y=y, cnt=cnt)


class PreProcessor:
    """process received data before passed further down the line

    Todo:
        make it a function ... Facade helps to achieve that
    Warning:
        Assumes that the enable changes for planes x and y are
        changed in the object that this object references to
    """
    def __init__(self, devices_status: Mapping[str, MonitoredDevice]):
        self.devices_status =  devices_status

    def preprocess(self, data : BPMReading) -> BPMReading:
        return pass_data_for_active_planes(data.cnt, data.x, data.y, self.devices_status[data.dev_name])