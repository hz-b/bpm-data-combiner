from enum import Enum
from typing import Sequence, Union
import logging

from bpm_data_combiner.app.config import Config
from bpm_data_combiner.monitor_devices.bl.monitor_synchronisation import (
    MonitorDeviceSynchronisation, offset_from_median,
)
from bpm_data_combiner.monitor_devices.data_model.monitored_device import (
    MonitoredDevice,
)

from ..bl.accumulator import Accumulator
from ..data_model.bpm_data_reading import BPMReading
from ..interfaces.facade import FacadeInterface
from ..monitor_devices.bl.monitor_devices_status import MonitorDevicesStatus
from ..monitor_devices.interfaces.monitor_devices_status import (
    MonitorDevicesStatusInterface,
    StatusField,
)
from ..post_processor.combine import collection_to_bpm_data_collection, accumulated_collections_to_array
from ..post_processor.preprocessor import PreProcessor
from ..post_processor.statistics import compute_mean_weights_for_planes

from .view import Views

from collector import Collector, CollectionItemInterface

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



class Facade(FacadeInterface):
    def __init__(self, *, prefix="OrbCol"):
        self.config = Config()
        self.accumulator = Accumulator()

        self.views = Views(prefix="prefix")

        # These need to know which devices are available
        # initalise with empty
        self.monitor_devices = MonitorDevicesStatus()
        self.dev_name_index = dict()

        # These need to know which devices are usable
        self.monitor_device_synchronisation = MonitorDeviceSynchronisation(
            monitored_devices=self.monitor_devices
        )

        self.collector = Collector(devices_names=self.monitor_devices.get_device_names())
        # Todo: make it a function and move it to on_collection_ready
        self.preprocessor = PreProcessor(
            devices_status=self.monitor_devices.devices_status
        )

    def set_device_names(self, device_names=Sequence[str]):
        self.dev_name_index = {name: idx for idx, name in enumerate(device_names)}
        self.monitor_devices.set_device_names(device_names)

    def update(self, *, cmd, dev_name, tpro, **kwargs):
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
            return self.dev_status(dev_name, StatusField.synchronised, kwargs["sync_stat"])
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
        # when the one collection is ready it
        # Todo: evaluate if a collection is ready
        #       if so trigger self._on_new_collection_ready()
        collection = self.collector.new_item(BPMReading(cnt=cnt, x=x, y=y, dev_name=dev_name))
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
        data = accumulated_collections_to_array(self.accumulator.get(), dev_names_index=self.dev_name_index)
        stat_data = compute_mean_weights_for_planes(data)
        self.views.periodic_data.update(stat_data)
        logger.debug("pushing stat data to bdata_view")
        self.views.bdata.update(stat_data)
        logger.debug("pushing stat data to bdata_view done")

    def _on_new_collection_ready(self, col: CollectionItemInterface):
        data = collection_to_bpm_data_collection(
            col, self.dev_name_index, default_value=0
        )
        self.accumulator.add(data)
        self.views.ready_data.update(data)
        # Todo: add preprocessor step

    def _on_device_status_changed(self):
        # collector needs to know which devices are active
        dev_names = self.monitor_devices.get_device_names()
        # needs to know which are active
        self.collector.device_names = dev_names
        # needs to know which are active
        self.preprocessor.device_names = dev_names
        devices = self.monitor_devices.devices_status
        self.views.monitor_bpms.update(
            names=[ds.name for _, ds in devices.items()],
            active=[ds.active for _, ds in devices.items()],
            synchronised=[ds.synchronised for _, ds in devices.items()],
            usable=[ds.usable for _, ds in devices.items()],
        )

    def compute_show_median(self):
        self.views.monitor_device_sync.update(
            *offset_from_median(self.monitor_device_synchronisation.get_last_indices())
        )

