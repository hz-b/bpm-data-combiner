from typing import Sequence, Union

from bact_analysis_bessyii.orm.model import Plane
from bpm_data_combiner.interfaces.monitor_devices_status import MonitorDevicesStatusInterface, StatusField

from ..data_model.monitored_device import MonitoredDevice, SynchronisationStatus, PlaneNames
from .event import Event

from .logger import logger


class MonitorDevicesStatus(MonitorDevicesStatusInterface):

    def __init__(self, devices_status: Sequence[MonitoredDevice]):
        self.devices_status = {dev.name: dev for dev in devices_status}
        self.on_status_change = Event(name="monitor_devices_on_status_change")

    def get_devicenames(self) -> Sequence[str]:
        """

        Todo:
            rename to "names of useable or participating devices"
        """
        devs = [
            ds.name for _, ds in self.devices_status.items() if ds.usable
        ]
        return devs

    def update(
            self, dev_name : str,
            field: StatusField,
            flag: Union[bool,SynchronisationStatus]
    ) -> bool:

        mon_info = self.devices_status["dev_name"]
        field = StatusField(field)
        if field == StatusField.active:
            updated = mon_info.update_active(flag)
        elif field == StatusField.synchronised:
            updated = mon_info.update_synchronised(flag)
        elif field == StatusField.enabled_x:
            updated = mon_info.update_plane(PlaneNames.x, flag)
        elif field == StatusField.enabled_y:
            updated = mon_info.update_plane(PlaneNames.y, flag)
        else:
            raise NotImplementedError

        if updated:
            self._status_changed()
        return updated

    def _status_changed(self):
        self.on_status_change.trigger(self.get_devicenames())

    def __repr__(self):
        txt = f"{self.__class__.__name__}(devices=dict("
        txt += ",".join([f"{name}=f{repr(dev)}" for name, dev in self.devices_status.items()])
        txt += "))"
        return txt
