from dataclasses import dataclass
from enum import Enum
from typing import Optional


class PlaneNames(Enum):
    x = "x"
    y = "y"


@dataclass
class MonitoredDevice:
    # identifier for the device
    name: str
    # planes can be enabled separately
    enabled_x: Optional[bool] = True
    enabled_y: Optional[bool] = True
    # is it active: i.e. data are received
    active: Optional[bool] = True

    @property
    def enabled(self):
        return self.enabled_x or self.enabled_y

    def update_status(self, plane, status) -> bool:
        """update status as required, return if update was needed"""

        plane = PlaneNames(plane)
        if plane == PlaneNames.x:
            if self.enabled_x == status:
                return False
            else:
                self.enabled_x = status
                return True

        elif plane == PlaneNames.y:
            if self.enabled_y == status:
                return False
            else:
                self.enabled_y = status
                return True

        raise AssertionError("should not end up here")
