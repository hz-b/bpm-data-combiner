from abc import ABCMeta, abstractmethod
from enum import Enum
from typing import Sequence, Union

from ..monitor_devices.interfaces.monitor_device_status_collection import StatusField


class ValidCommands(Enum):
    # Device data
    reading = "reading"
    # Device status
    active = "active"
    enabled = "enabled"
    reset = "reset"
    sync_stat = "sync_stat"
    # requesting data
    periodic = "periodic"
    cfg_comp_median = "cfg_comp_median"
    known_device_names = "known_device_names"


class ControllerInterface(metaclass=ABCMeta):
    @abstractmethod
    def new_value(self, dev_name: str, value: Sequence[float]):
        pass

    @abstractmethod
    def dev_status(self, dev_name: str, field: StatusField, value: Union[bool,int]) -> bool:
        """
        returns if the device status needed to be updated
        """
        pass

    @abstractmethod
    def update(self, *, dev_name, tpro=False, **kwargs):
        pass