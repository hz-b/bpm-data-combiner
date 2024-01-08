from typing import Sequence

from ..data_model.monitored_device import MonitoredDevice


class MonitorDevices:
    def __init__(self, devices_status: Sequence[MonitoredDevice]):
        self.devices_status = {dev.name: dev for dev in devices_status}

    def set_enabled(self, dev_name: str, status: bool):
        self.devices_status[dev_name].enabled = status
        pass

    def set_active(self, dev_name: str, status: bool):
        self.devices_status[dev_name].active = status
        pass

    def get_devicenames(self):
        devs = [
            ds.name for _, ds in self.devices_status.items() if ds.active and ds.enabled
        ]
        return devs
