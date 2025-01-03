"""Give an idea if the id's are synchronised
"""
from typing import Sequence, Tuple

from bpm_data_combiner.monitor_devices.bl.monitor_devices_status import MonitorDevicesStatus
import numpy as np


def offset_from_median(data: Sequence[int]) -> Tuple[int, Sequence[int]]:
    data = np.asarray(data)
    median = np.median(data)
    return median, data - median


class MonitorDeviceSynchronisation:
    def __init__(self, monitored_devices : MonitorDevicesStatus):
        self.dev_names = [dev_stat.name for _, dev_stat in monitored_devices.devices_status.items()]
        self.dev_index = {name: cnt for cnt, name in enumerate(self.dev_names)}
        # todo: how to initialise these indices
        self.lact_indices = np.zeros(len(self.dev_names), np.int32)

    def add_new_count(self, dev_name, reading_index):
        self.lact_indices[self.dev_index[dev_name]] = reading_index

    def get_last_indices(self):
        return self.lact_indices

    def offset_from_median(self) -> Tuple[int, Sequence[int]]:
        return offset_from_median(self.get_last_indices())
