from abc import ABCMeta, abstractmethod
from enum import Enum
from typing import Union, Sequence

from ..data_model.monitored_device import SynchronisationStatus


class StatusField(Enum):
    #: both planes
    enabled = "enabled"
    enabled_x = "enabled_x"
    enabled_y = "enabled_y"
    synchronised = "synchronised"
    active = "active"


class MonitorDevicesStatusInterface(metaclass=ABCMeta):
    """Expects to be informed on devices status, passes it on to event subscribes

    Gets informed if a device is
    * active
    * enabled

    If one of them changes the :class:``Event any:`on_status_change`
    is triggered. This will pass a sequence of valide device names
    to callers.

    These two differ by:
     * Enabled: typically a person will decide that this device
       is used. It is split up for its two planes x and y.
     * active: typically an automatic monitor will check if it the
       device is active or not.

    """
    @abstractmethod
    def update(self, dev_name : str, field: StatusField, info: Union[bool,SynchronisationStatus]) -> bool:
        """

        flags if internally an update was made
        """
        pass

    @abstractmethod
    def get_devicenames(self) -> Sequence[str]:
        """names of currently usable devices
        """
        pass
