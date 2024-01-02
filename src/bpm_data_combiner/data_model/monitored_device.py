from dataclasses import dataclass
from typing import Optional


@dataclass
class MonitoredDevice:
    # identifier for the device
    name: str
    # is it active: i.e. data are received
    active : Optional[bool] = True
    # are its data to be used
    enabled : Optional[bool] = True