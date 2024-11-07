from .count_down import CountDown
from ..data_model.monitored_device import SynchronisationStatus, PlaneNames
from ..interfaces.monitored_device_status import MonitoredDeviceWithPlanesStatusInterface


class MonitoredDeviceStatus(MonitoredDeviceWithPlanesStatusInterface):
    def __init__(
            self,
            name: str,
            *,
            enabled_x: bool = True,
            enabled_y: bool = True,
            active: bool = False,
            sync_stat : SynchronisationStatus = SynchronisationStatus.no_sync,
            max_steps: int=20
            ):

        # make it active by default
        self.count_down = CountDown(max_steps=max_steps)
        if not active:
            self.count_down.set_expired()

        self.name = name
        self._enabled_x = enabled_x
        self._enabled_y = enabled_y
        self.sync_stat = sync_stat

    @property
    def active(self) -> bool:
        if self.count_down.status():
            return True
        else:
            return False

    @property
    def enabled_x(self):
        return self._enabled_x

    @property
    def enabled_y(self):
        return self._enabled_y

    @property
    def enabled(self):
        return self.enabled_x or self.enabled_y

    @property
    def synchronised(self) -> bool:
        return self.sync_stat == SynchronisationStatus.synchronised

    @property
    def usable(self) ->  bool:
        return self.synchronised and self.count_down.status()

    def update_active(self, active: bool) -> bool:
        if not active:
            # use heart beat instead ... finds itself inactive
            raise AssertionError("Should not be sent any more")

        changed_status = not (active == self.active)
        self.count_down.reset()
        return changed_status

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
                self._enabled_x = status
                return True

        elif plane == PlaneNames.y:
            if self.enabled_y == status:
                return False
            else:
                self._enabled_y = status
                return True

        raise AssertionError("should not end up here")

    def heart_beat(self) -> None:
        self.count_down.step()

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"name={self.name},"
            f" usable={self.usable},"
            f" enabled={{x: {self.enabled_x}, y: {self.enabled_y} }},"
            f" active={self.active},"
            f" synchronised={self.synchronised},"
            ")"
        )