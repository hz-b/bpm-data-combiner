import numpy as np
from typing import Sequence
from ..bl.logger import logger
from ..data_model.bpm_data_collection import BPMDataCollection, BPMDataCollectionStats

import pydev

import sys
stream = sys.stdout

def string_array_to_bytes(names: Sequence[str], *, encoding="utf8"):
    return [bytes(name, encoding) for name in names]


class ViewBPMMonitoring:
    def __init__(self, prefix: str):
        self.prefix = prefix

    def update(self, *,
               names: Sequence[str],
               active: Sequence[bool],
               synchronised: Sequence[bool],
               usable: Sequence[bool],
               ):
        # names = string_array_to_bytes(names)
        names = list(names)
        label = self.prefix + ":" + "names"
        logger.debug("Update active view label %s, values %s", label, names)
        # stream.write("Update active view label %s, values %s\n" % (label, names))
        pydev.iointr(label, names)

        # int number wrong by a factor of 2: why?
        active = [bool(v) for v in active]
        active = np.array(active, dtype=np.int32)
        label = self.prefix + ":" + "active"
        logger.debug("Update active view label %s, values %s", label, active)
        pydev.iointr(label, active.tolist())

        synchronised = [bool(v) for v in synchronised]
        synchronised = np.array(synchronised, dtype=np.int32)
        label = self.prefix + ":" + "synchronised"
        logger.debug("Update active view label %s, values %s", label, synchronised)
        pydev.iointr(label, synchronised.tolist())

        usable = [bool(v) for v in usable]
        usable = np.array(usable, dtype=np.int32)
        label = self.prefix + ":" + "usable"
        logger.debug("Update active view label %s, values %s", label, usable)
        pydev.iointr(label, usable.tolist())



class ViewBPMDataCollection:
    def __init__(self, prefix: str):
        self.prefix = prefix

    def update(self, data: BPMDataCollection):
        logger.debug("viewer updating data for %s", self.prefix)
        logger.debug("viewer updating data for %s: data %s", self.prefix, data)
        for suffix, var in [("x", data.x), ("y", data.y)]:
            logger.debug("viewer updating data for %s: suffix %s", self.prefix, suffix)

            # need to ensure that new data are only set when these changed
            label = f"{self.prefix}:{suffix}:valid"
            # arrays seem not yet to be supported by PyDevice
            vals = [int(v) for v in var.valid]
            logger.debug("Update label %s, values %s", label, vals)
            pydev.iointr(label, vals)

            # How to treat masked values?
            values = var.values
            if not (~values.mask).all():
                # unmaks them and assume that the default value
                # will tell the user something is wrong
                # furthermore there is still the mask
                values = values.copy()
                values.mask = False

            label = f"{self.prefix}:{suffix}:values"
            # Todo: check if the conversion is still required given that
            # PyDevice seems not support array.
            # Todo: find out why.
            values = [int(v) for v in values]
            logger.debug("Update label %s, values %s", label, values)
            pydev.iointr(label, values)

        label = self.prefix + ":cnt"
        cnt = int(data.cnt)
        logger.debug("Update label=%s, cnt=%s type %s", label, cnt, type(cnt))
        pydev.iointr(label, cnt)

        label = self.prefix + ":names"
        names_byte_encoded = string_array_to_bytes(data.names)
        logger.debug("Update label=%s, names=%s", label, names_byte_encoded)
        pydev.iointr(label, names_byte_encoded)


class ViewBPMDataCollectionStats:
    def __init__(self, prefix: str):
        self.prefix = prefix

    def update(self, data: BPMDataCollectionStats):
        for plane, plane_var in [("x", data.x), ("y", data.y)]:
            for suffix, var in [
                ("values", [float(v) for v in plane_var.values]),
                ("std", [float(v) for v in plane_var.std]),
                ("n_readings", [int(v) for v in plane_var.n_readings]),
            ]:
                label = f"{self.prefix}:{plane}:{suffix}"
                logger.debug("label %s var %s", label, var)
                pydev.iointr(label, var)

        # which data count? not there yet
        # ("cnt", data.cnt)
        for suffix, var in [
            ("names", data.names),
        ]:
            label = self.prefix + ":" + suffix
            pydev.iointr(label, var)


class ViewBPMDataAsBData:
    """Combine mean and std for x and y as expected by legacy BESSY II

    similar to :class:``ViewBpmDataCollectionStats, but organsied in a flat
    array.

    Todo:
       check necessary coordinate conversion
    """

    def __init__(self, prefix: str):
        self.prefix = prefix

    def update(self, data: BPMDataCollectionStats):
        """prepare data as expected
        """
        logger.debug("view bdata: publishing data %s", data)
        nm2mm = 1e-6
        n_entries = len(data.x.values)
        # MLS are 32 bpms ...
        n_bpms = 32
        if n_entries > n_bpms:
            raise ValueError("number of bpms %s too many. max %s", n_entries, n_bpms)

        bdata = np.empty([8, n_bpms], dtype=float)
        bdata.fill(0.0)
        # is this the correct way to convert the data ?
        scale_bits = 2**15/10
        # flipping coordinate system to get the dispersion on the correct side
        # todo: check at which state this should be done
        # fmt:off
        bdata[0, :n_entries] = - data.x.values * nm2mm * scale_bits
        bdata[1, :n_entries] =   data.y.values * nm2mm * scale_bits
        # fmt:on
        # intensity z 1.3
        # bdata[2] = 3
        # intensityz z 1.3
        # bdata[3] = 3
        # AGC status needs to be three for valid data
        # todo: find out what to set if only one plane is valid?
        bdata[4,:n_entries] = np.where((data.x.n_readings > 0) | (data.y.n_readings > 0), 3, 0)
        bdata[4, -1] = 2
        # scale rms so that the slow orbit feedback accepts the data
        # factor 100 seems to be enough.
        # I think I should add some check that the noise is large enough
        scale_rms = 20
        # todo: invalid data: set rms to 0
        bdata[6, :n_entries] = np.where(data.x.n_readings > 0, data.x.std * nm2mm * scale_bits * scale_rms, 0)
        bdata[7, :n_entries] = np.where(data.y.n_readings > 0, data.y.std * nm2mm * scale_bits * scale_rms, 0)

        label = f"{self.prefix}"
        bdata = [int(v) for v in bdata.ravel()]
        pydev.iointr(label, bdata)
        logger.debug("view bdata: label %s,  %d n_entries", label, n_entries)
        # logger.warning("view bdata: label %s bdata %s", label, bdata)


class ViewStringBuffer:
    def __init__(self, label: str):
        self.label = label

    def update(self, buf: Sequence[str]):
        pydev.iointr(self.label, list(buf))
        # logger.warning(f'View string {self.label}:"{t_str}"')


class ViewCollectorStatus:
    def __init__(self, label: str):
        self.label = label

    def update(self, cnt: int):
        # stream.write(f"updating {self.label} with cnt {cnt}\n")
        # stream.flush()
        pydev.iointr(self.label, cnt)


class ViewDeviceSynchronisation:
    def __init__(self, prefix: str):
        self.prefix = prefix

    def update(self, median: int, offset_from_median: Sequence[np.int32]):
        # stream.write(f"updating {self.prefix} with median {median}\n")
        # stream.flush()
        pydev.iointr(self.prefix + ':median', median)
        pydev.iointr(self.prefix + ':offset', list(offset_from_median))


class ViewConfiguration:
    def __init__(self, prefix: str):
        self.prefix = prefix

    def update(self, median_computation: bool):
        stream.write(f"updating {self.prefix} with median {median_computation}\n")
        stream.flush()
        pydev.iointr(self.prefix + ':comp:median', bool(median_computation))


class Views:
    def __init__(self, prefix: str):
        self.ready_data = ViewBPMDataCollection(prefix + ":out:100ms")
        self.periodic_data = ViewBPMDataCollectionStats(prefix + ":out:2s")
        self.bdata = ViewBPMDataAsBData(prefix + ":bdata")
        self.monitor_bpms = ViewBPMMonitoring(prefix + ":mon")
        self.monitor_update_cmd_errors = ViewStringBuffer(prefix + ":im:cmd_err")
        self.collector = ViewCollectorStatus(prefix + ":mon:col:cnt")
        self.monitor_device_sync = ViewDeviceSynchronisation(prefix + ":mon:sync")
        self.configuration = ViewConfiguration(prefix + ":mon:cfg")


__all__ = [
    "Views",
    "ViewStringBuffer",
    "ViewBPMDataAsBData",
    "ViewBPMDataCollection",
    "ViewBPMDataCollectionStats",
    "ViewBPMMonitoring",
]
