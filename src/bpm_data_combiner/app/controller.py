from enum import Enum
import logging
from typing import Sequence, Union


from collector import Collector, CollectionItemInterface

from ..bl.accumulator import Accumulator
from ..interfaces.controller import ControllerInterface
from ..monitor_devices import (
    MonitorDevicesStatus,
    MonitorDeviceSynchronisation,
    StatusField,
)
from ..post_processor.combine import (
    collection_to_bpm_data_collection,
    accumulated_collections_to_array,
)
from ..post_processor.handle_active_planes import pass_data_for_active_planes
from ..post_processor.statistics import compute_mean_weights_for_planes

from .bdata import stat_data_to_bdata
from .config import Config
from .view import Views

logger = logging.getLogger("bpm-data-combiner")


class ValidCommands(Enum):
    # Device data
    reading = "reading"
    # Device status
    active = "active"
    enabled = "enabled"
    reset = "reset"
    sync_stat = "sync_stat"
    # requesting data
    periodic = "periodic"
    cfg_comp_median = "cfg_comp_median"
    known_device_names = "known_device_names"


class Controller(ControllerInterface):
    def __init__(self, *, prefix="OrbCol"):
        self.config = Config()
        self.accumulator = Accumulator()

        self.views = Views(prefix=prefix)

        # These need to know which devices are available
        # initalise with empty
        self.monitor_devices = MonitorDevicesStatus()
        self.dev_name_index = dict()

        # These need to know which devices are usable
        self.monitor_device_synchronisation = MonitorDeviceSynchronisation(
            monitored_devices=self.monitor_devices
        )

        self.collector = Collector(devices_names=[])

    def set_device_names(self, device_names=Sequence[str]):
        self.dev_name_index = {name: idx for idx, name in enumerate(device_names)}
        self.monitor_devices.set_device_names(device_names)
        self.collector.devices_names = device_names
        # that names etc. get published
        self._on_device_status_changed()
        return len(device_names)

    def update(self, *, dev_name, tpro=False, **kwargs):
        """

        compatible to main.update facilitates testing
        """
        # extraction of command from kwargs should be the sole
        # code duplication to main.update
        cmd = next(iter(kwargs))
        return self._update(cmd=cmd, dev_name=dev_name, tpro=tpro, **kwargs)

    def _update(self, *, cmd, dev_name, tpro, **kwargs):
        cmd = ValidCommands(cmd)
        if cmd == ValidCommands.reading:
            return self.new_value(dev_name=dev_name, value=kwargs["reading"])
        elif cmd == ValidCommands.active:
            return self.dev_status(
                dev_name=dev_name, field=StatusField.active, value=kwargs["active"]
            )
        elif cmd == ValidCommands.enabled:
            plane = kwargs["plane"]
            val = kwargs["enabled"]
            if plane == "x":
                return self.dev_status(
                    dev_name=dev_name, field=StatusField.enabled_x, value=val
                )
            elif plane == "y":
                return self.dev_status(
                    dev_name=dev_name, field=StatusField.enabled_y, value=val
                )
            else:
                raise AssertionError(f"plane {plane} unknown")
        elif cmd == ValidCommands.sync_stat:
            return self.dev_status(
                dev_name, StatusField.synchronised, kwargs["sync_stat"]
            )
        elif cmd == ValidCommands.known_device_names:
            return self.set_device_names(device_names=kwargs["known_device_names"])
        elif cmd == ValidCommands.cfg_comp_median:
            self.config.request_median_computation(kwargs["cfg_comp_median"])
        elif cmd == ValidCommands.periodic:
            self.periodic_trigger()
        elif cmd == ValidCommands.reset:
            self.reset()
        else:
            raise AssertionError(f"Why command {cmd} is not handled ?")

    def reset(self):
        self.collector.reset()
        self.accumulator.swap(check_collection_length=False)

    def new_value(self, dev_name: str, value: Sequence[int]):
        cnt, x, y = value
        collection = self.collector.new_item(
            pass_data_for_active_planes(
                cnt, x, y, device_status=self.monitor_devices.devices_status[dev_name]
            )
        )
        if collection.ready:
            self._on_new_collection_ready(collection.data())
        if self.config.do_median_computation:
            self.monitor_device_synchronisation.add_new_count(dev_name, cnt)
            self.compute_show_median()

    def dev_status(
        self, dev_name: str, field: StatusField, value: Union[bool, int]
    ) -> bool:
        """gives feedback if device monitor status changed"""
        status_changed = self.monitor_devices.update(dev_name, field, value)
        if status_changed:
            self._on_device_status_changed()
        return status_changed

    def periodic_trigger(self):
        """Present new (averaged) bpm data on periodic trigger"""
        data = accumulated_collections_to_array(
            self.accumulator.get(), dev_names_index=self.dev_name_index
        )
        stat_data = compute_mean_weights_for_planes(data)
        self.views.periodic_data.update(stat_data)
        logger.debug("pushing stat data to bdata_view")
        #: todo ... need to get kwargs from config
        bdata = stat_data_to_bdata(
            stat_data,
            device_index=self.dev_name_index,
            n_bpms=32,
            scale_x_axis=1.0 / 1.4671,
        )
        self.views.bdata.update(bdata.ravel())
        logger.debug("pushing stat data to bdata_view done")

    def _on_new_collection_ready(self, col: CollectionItemInterface):
        data = collection_to_bpm_data_collection(
            col, self.dev_name_index, default_value=0
        )
        self.accumulator.add(data)
        self.views.ready_data.update(data)

    def _on_device_status_changed(self):
        # collector needs to know which devices are active
        dev_names = self.monitor_devices.get_device_names()
        # needs to know which are active
        self.collector.device_names = dev_names
        # needs to know which are active
        devices = self.monitor_devices.devices_status
        self.views.monitor_bpms.update(
            names=[ds.name for _, ds in devices.items()],
            active=[ds.active for _, ds in devices.items()],
            synchronised=[ds.synchronised for _, ds in devices.items()],
            usable=[ds.usable for _, ds in devices.items()],
        )

    def compute_show_median(self):
        self.views.monitor_device_sync.update(
            *self.monitor_device_synchronisation.offset_from_median()
        )
