from typing import Sequence, Hashable, Mapping

from ..data_model.bpm_data_reading import BPMReading, BPMReadingBeingProcessed
from ..data_model.monitored_device import MonitoredDevice


class PreProcessor:
    """process received data before passed further down the line

    Warning:
        Assumes that the enable changes for planes x and y are
        changed in the object that this object references to
    """
    def __init__(self, devices_status: Mapping[str, MonitoredDevice]):
        self.devices_status =  devices_status

    def preprocess(self, data : BPMReadingBeingProcessed) -> BPMReading:
        dev_stat = self.devices_status[data.dev_name]
        x, y = data.x, data.y
        if not dev_stat.enabled_x:
            x = None
        if not dev_stat.enabled_y:
            y = None
        return BPMReading(dev_name=data.dev_name, x=x, y=y, cnt=data.cnt)