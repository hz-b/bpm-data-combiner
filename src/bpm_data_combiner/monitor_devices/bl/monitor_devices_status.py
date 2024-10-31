from typing import Sequence, Union

from ..data_model.monitored_device import MonitoredDevice, SynchronisationStatus, PlaneNames
from bpm_data_combiner.monitor_devices.interfaces.monitor_devices_status import MonitorDevicesStatusInterface, StatusField


class MonitorDevicesStatus(MonitorDevicesStatusInterface):

    def __init__(self, device_names : Sequence[str] = None):
        self.devices_status = None
        _dn = device_names or []
        self.set_device_names(_dn)

    def set_device_names(self, device_names : Sequence[str]):
        self.devices_status = {name: MonitoredDevice(name) for name in device_names}

    def get_device_names(self) -> Sequence[str]:
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

        mon_info = self.devices_status[dev_name]
        field = StatusField(field)
        if field == StatusField.active:
            updated = mon_info.update_active(flag)
        elif field == StatusField.synchronised:
            updated = mon_info.update_synchronised(flag)
        elif field == StatusField.enabled_x:
            updated = mon_info.update_plane(PlaneNames.x, flag)
        elif field == StatusField.enabled_y:
            updated = mon_info.update_plane(PlaneNames.y, flag)
        elif field == StatusField.enabled:
            up1 = mon_info.update_plane(PlaneNames.x, flag)
            up2 = mon_info.update_plane(PlaneNames.y, flag)
            updated = up1 or up2
        else:
            raise NotImplementedError

        return updated


    def __repr__(self):
        txt = f"{self.__class__.__name__}(devices=dict("
        txt += ",".join([f"{name}=f{repr(dev)}" for name, dev in self.devices_status.items()])
        txt += "))"
        return txt
