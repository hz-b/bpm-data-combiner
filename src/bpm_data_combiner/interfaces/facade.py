from abc import ABCMeta, abstractmethod
from typing import Sequence, Union

from bpm_data_combiner.monitor_devices.interfaces.monitor_devices_status import StatusField


class FacadeInterface(metaclass=ABCMeta):
    @abstractmethod
    def new_value(self, dev_name: str, value: Sequence[float]):
        pass

    @abstractmethod
    def dev_status(self, dev_name: str, field: StatusField, value: Union[bool|int]) -> bool:
        """
        returns if the device status needed to be updated
        """
        pass
