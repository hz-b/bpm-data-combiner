from typing import Sequence, Union

from ..interfaces.monitor_devices_status import MonitorDevicesStatusInterface, StatusField
from ..interfaces.facade import FacadeInterface


class Facade(FacadeInterface):
    def __init__(self, device_monitor: MonitorDevicesStatusInterface):
        self.devices_monitor = device_monitor

    def new_value(self, dev_name: str, value: Sequence[float]):
        pass

    def dev_status(self, dev_name: str, field: StatusField, value: Union[bool,int]) -> bool:
        return self.devices_monitor.update(dev_name, field, value)
