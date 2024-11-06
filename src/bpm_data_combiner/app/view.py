from itertools import count

import numpy as np
from typing import Sequence
from softioc import builder

from ..bl.logger import logger
from ..data_model.bpm_data_collection import BPMDataCollection, BPMDataCollectionStats, BPMDataCollectionPlane, \
    BPMDataCollectionStatsPlane


def string_array_to_bytes(names: Sequence[str], *, encoding="utf8"):
    return [bytes(name, encoding) for name in names]


class ViewBPMMonitoring:
    def __init__(self, prefix: str):
        self.prefix = prefix
        self.names = builder.WaveformIn(
            f"{prefix}:names", initial_value=[""], length=128
        )
        self.active = builder.WaveformIn(
            f"{prefix}:active", initial_value=[0], length=128
        )
        self.synchronised = builder.WaveformIn(
            f"{prefix}:synchronised", initial_value=[0], length=128
        )
        self.usable = builder.WaveformIn(
            f"{prefix}:usable", initial_value=[0], length=128
        )

    def update(
        self,
        *,
        names: Sequence[str],
        active: Sequence[bool],
        synchronised: Sequence[bool],
        usable: Sequence[bool],
    ):
        self.names.set(names)
        self.active.set(active)
        self.synchronised.set(synchronised)
        self.usable.set(usable)


class ViewBPMDataCollectionPlane:
    def __init__(self, prefix: str):
        self.vals = builder.WaveformIn(
            f"{prefix}:values", initial_value=[0.0] * 128, length=128
        )
        self.valid = builder.WaveformIn(
            f"{prefix}:valid", initial_value=[0.0] * 128, length=128
        )

    def update(self, vals: BPMDataCollectionPlane):
        self.vals.set(vals.values)
        self.valid.set(vals.valid)


class ViewBPMDataCollection:
    def __init__(self, prefix: str):
        self.x = ViewBPMDataCollectionPlane(f"{prefix}:x")
        self.y = ViewBPMDataCollectionPlane(f"{prefix}:y")
        self.names = builder.WaveformIn(f"{prefix}:name", initial_value=[""], length=128)
        self.cnt = builder.longIn(f"{prefix}:cnt", initial_value=0)

    def update(self, data: BPMDataCollection):
        self.x.update(data.x)
        self.y.update(data.y)
        self.names.set(data.names)
        self.cnt.set(data.cnt)



class ViewBPMDataCollectionStatsPlane:
    def __init__(self, prefix: str):
        self.values = builder.WaveformIn(
            f"{prefix}:values", initial_value=[0.0]* 128, length=128
        )
        self.std = builder.WaveformIn(
            f"{prefix}:std", initial_value=[0.0]* 128, length=128
        )
        self.n_readings = builder.WaveformIn(
            f"{prefix}:n_readings", initial_value=[0.0]* 128, length=128
        )

    def update(self, data: BPMDataCollectionStatsPlane):
        self.values.set(data.values)
        self.std.set(data.std)
        self.n_readings.set(data.n_readings)


class ViewBPMDataCollectionStats:
    def __init__(self, prefix: str):
        self.x = ViewBPMDataCollectionStatsPlane(f"{prefix}:x")
        self.y = ViewBPMDataCollectionStatsPlane(f"{prefix}:y")
        self.names = builder.WaveformIn(f"{prefix}:name", initial_value=[""], length=128)

    def update(self, data: BPMDataCollectionStats):
        self.x.update(data.x)
        self.y.update(data.y)
        self.names.set(data.names)


class ViewBPMDataAsBData:
    """Combine mean and std for x and y as expected by legacy BESSY II

    similar to :class:``ViewBpmDataCollectionStats, but organsied in a flat
    array.

    Todo:
       check necessary coordinate conversion
    """

    def __init__(self, prefix: str):
        self.bdata = builder.WaveformIn(
            f"{prefix}", initial_value=np.array([0]*1024).astype(np.int16), length=1024
        )
        self.cnt = builder.longIn(f"{prefix}:cnt", initial_value=0)
        self.counter = count()

    def update(self, bdata: Sequence[int]):
        """prepare data as expected"""
        bdata = np.asarray(bdata).astype(np.int16)
        logger.warning("publishing bdata {bdata}")
        self.bdata.set(bdata)


class ViewStringBuffer:
    def __init__(self, name: str):
        self.buf = builder.WaveformIn(
            name=name, initial_value = [""] * 256, length=256
        )

    def update(self, buf: Sequence[str]):
        self.buf.set(buf)


class ViewCollectorStatus:
    def __init__(self, label: str):
        self.cnt = builder.longIn(label, initial_value=0)

    def update(self, cnt: int):
        self.cnt.set(cnt)


class ViewDeviceSynchronisation:
    def __init__(self, prefix: str):
        self.median = builder.longIn(f"{prefix}:median", initial_value=0)
        self.offset = builder.WaveformIn(
            f"{prefix}:offset",  initial_value=[0] * 128, length=128
        )

    def update(self, median: int, offset_from_median: Sequence[np.int32]):
        self.median.set(median)
        self.offset.set(offset_from_median)


class ViewConfiguration:
    def __init__(self, prefix: str):
        self.comp_median = builder.boolIn(f"{prefix}:comp:median", "inactive", "active")

    def update(self, median_computation: bool):
        self.comp_median.set(median_computation)


class Views:
    def __init__(self, prefix: str):
        self.ready_data = ViewBPMDataCollection(prefix + "out:100ms")
        self.periodic_data = ViewBPMDataCollectionStats(prefix + "out:2s")
        self.bdata = ViewBPMDataAsBData(prefix + "bdata")
        self.monitor_bpms = ViewBPMMonitoring(prefix + "mon")
        self.monitor_update_cmd_errors = ViewStringBuffer(prefix + "im:cmd_err")
        self.collector = ViewCollectorStatus(prefix + "mon:col:cnt")
        self.monitor_device_sync = ViewDeviceSynchronisation(prefix + "mon:sync")
        self.configuration = ViewConfiguration(prefix + "mon:cfg")


__all__ = [
    "Views",
    "ViewStringBuffer",
    "ViewBPMDataAsBData",
    "ViewBPMDataCollection",
    "ViewBPMDataCollectionStats",
    "ViewBPMMonitoring",
]
