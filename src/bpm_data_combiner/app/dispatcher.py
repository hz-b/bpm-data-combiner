from typing import Sequence

from ..interfaces.monitor_devices import MonitorDevicesStatusInterface, StatusField
from ..interfaces.dispatcher import DispatcherInterface


class Dispatcher(DispatcherInterface):
    def __init__(self, device_monitor: MonitorDevicesStatusInterface):
        self.device_moitor = device_monitor

    def new_value(self, dev_name: str, value: Sequence[float]):
        pass

    def dev_status(self, dev_name: str, field: StatusField, value: bool):
        self.device_moitor.update(dev_name, field, value)
