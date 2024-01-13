from typing import Sequence

from ..data_model.monitored_device import MonitoredDevice
from .event import Event


class MonitorDevices:
    """Expects to be informed on devices status, passes it on to event subscribes

    Gets informed if a device is
    * active
    * anabled

    If one of them changes the :class:``Event any:`on_status_change`
    is triggered. This will pass a sequence of valide device names
    to callers.

    These two differ by:
     * Enabled: typically a person will devide that this device
       is used
     * active: tpically an automatic monitor will check if it the
       device is active or not

    Todo: Rename it to e.g. `MonitoredDevicesStatus`
    """
    def __init__(self, devices_status: Sequence[MonitoredDevice]):
        self.devices_status = {dev.name: dev for dev in devices_status}
        self.on_status_change = Event(name="monitor_devices_on_status_change")

    def get_devicenames(self):
        devs = [
            ds.name for _, ds in self.devices_status.items() if ds.active and ds.enabled
        ]
        return devs

    def _status_changed(self):
        self.on_status_change.trigger(self.get_devicenames())

    def set_enabled(self, dev_name: str, status: bool):
        if status ==  self.devices_status[dev_name].enabled:
            return

        self.devices_status[dev_name].enabled = status
        self._status_changed()

    def set_active(self, dev_name: str, status: bool):
        if status == self.devices_status[dev_name].active:
            return

        self.devices_status[dev_name].active = status
        self._status_changed()
