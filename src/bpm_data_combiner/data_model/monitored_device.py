from dataclasses import dataclass
from typing import Optional


@dataclass
class MonitoredDevicePlane:
    # are its data to be used
    enabled: Optional[bool] = True


@dataclass
class MonitoredDevice:
    # identifier for the device
    name: str
    # planes can be enabled separately
    enabled_x: Optional[MonitoredDevicePlane] = MonitoredDevicePlane()
    enabled_y: Optional[MonitoredDevicePlane] = MonitoredDevicePlane()
    # is it active: i.e. data are received
    active: Optional[bool] = True

    @property
    def enabled(self):
        return self.enabled_x or self.enabled_y
