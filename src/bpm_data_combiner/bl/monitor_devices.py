from typing import Sequence

from ..data_model.monitored_device import MonitoredDevice, SynchronisationStatus
from .event import Event


class MonitorDevices:
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

    Todo: Rename it to e.g. `MonitoredDevicesStatus`
    """

    def __init__(self, devices_status: Sequence[MonitoredDevice]):
        self.devices_status = {dev.name: dev for dev in devices_status}
        self.on_status_change = Event(name="monitor_devices_on_status_change")

    def get_devicenames(self) -> Sequence[str]:
        devs = [
            ds.name for _, ds in self.devices_status.items() if ds.active and ds.synchronised
        ]
        return devs

    def _status_changed(self):
        self.on_status_change.trigger(self.get_devicenames())

    def set_enabled(self, dev_name: str, enabled: bool, plane: str):
        required_update = self.devices_status[dev_name].update_status(plane, enabled)
        if required_update:
            self._status_changed()

    def set_active(self, dev_name: str, status: bool):
        if status == self.devices_status[dev_name].active:
            return

        self.devices_status[dev_name].active = status
        self._status_changed()

    def set_synchronisation_status(self, dev_name: str, sync_stat: SynchronisationStatus):
        self.devices_status[dev_name].sync_stat =  SynchronisationStatus(sync_stat)
