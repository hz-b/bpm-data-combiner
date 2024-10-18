from dataclasses import dataclass
from enum import Enum, IntEnum
from typing import Optional


class PlaneNames(Enum):
    x = "x"
    y = "y"


class SynchronisationStatus(IntEnum):
    no_sync = 0
    tracking = 1
    synchronised = 2


@dataclass
class MonitoredDevice:
    """Info on status of currently monitored device

    update methods return if the all changed the internal state
    """
    # identifier for the device
    name: str
    # planes can be enabled separately
    enabled_x: Optional[bool] = True
    enabled_y: Optional[bool] = True
    # is it active: i.e. data are received
    active: Optional[bool] = False
    # is the device in synch state: thus the counters are valid ones
    sync_stat : Optional[SynchronisationStatus] = SynchronisationStatus.no_sync

    @property
    def enabled(self):
        return self.enabled_x or self.enabled_y

    @property
    def synchronised(self) -> bool:
        return self.sync_stat == SynchronisationStatus.synchronised

    @property
    def usable(self) ->  bool:
        return self.synchronised and self.active

    def update_active(self, active: bool) -> bool:
        if self.active == active:
            return False
        else:
            self.active = active
            return True
        raise AssertionError("should not end up here")

    def update_synchronised(self, sync_stat: SynchronisationStatus) -> bool:
        if self.sync_stat == sync_stat:
            return False
        else:
            self.sync_stat = sync_stat
            return True
        raise AssertionError("should not end up here")

    def update_plane(self, plane: PlaneNames, status: bool) -> bool:
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
