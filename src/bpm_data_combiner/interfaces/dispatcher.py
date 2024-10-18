from abc import ABCMeta, abstractmethod
from typing import Sequence

from bpm_data_combiner.interfaces.monitor_devices_status import StatusField


class DispatcherInterface(metaclass=ABCMeta):
    @abstractmethod
    def new_value(self, dev_name: str, value: Sequence[float]):
        pass

    @abstractmethod
    def dev_status(self, dev_name: str, field: StatusField, value: bool):
        pass
