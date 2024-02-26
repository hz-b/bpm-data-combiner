import numpy as np

from ..data_model.bpm_data_collection import BPMDataCollection, BPMDataCollectionStats
import logging
from typing import Sequence

import pydev

logger = logging.getLogger("bpm-data-combiner")


def string_array_to_bytes(names: Sequence[str], *, encoding="utf8"):
    return [bytes(name, encoding) for name in names]


class ViewBPMMonitoring:
    def __init__(self, prefix: str):
        self.prefix = prefix

    def update(self, names: Sequence[str], active: Sequence[bool]):
        names = string_array_to_bytes(names)
        label = self.prefix + ":" + "names"
        logger.debug("Update active view label %s, values %s", label, names)
        pydev.iointr(label, names)

        # int number wrong by a factor of 2: why?
        active = [bool(v) for v in active]
        active = np.array(active, dtype=np.int32)
        label = self.prefix + ":" + "active"
        logger.debug("Update active view label %s, values %s", label, active)
        pydev.iointr(label, active)


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
            vals = [bool(v) for v in var.valid]
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
                logger.warning("label %s var %s", label, var)
                pydev.iointr(label, var)

        # which data count? not there yet
        # ("cnt", data.cnt)
        for suffix, var in [
            ("names", string_array_to_bytes(data.names)),
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
        """ """
        n_entries = len(data.x.values)
        bdata = np.empty(8, n_entries, dtype=np.float)
        bdata.setfield(np.nan)
        bdata[0] = data.x.values
        bdata[1] = data.x.std
        bdata[6] = data.y.values
        bdata[7] = data.y.std

        label = f"{self.prefix}:bdata"
        pydev.iointr(label, bdata.ravel())


class ViewStringBuffer:
    def __init__(self, label: str):
        self.label = label

    def update(self, buf: Sequence[str]):
        # logger.warning(f'View string {self.label}:"{t_str}"')
        pydev.iointr(self.label, string_array_to_bytes(buf))


class Views:
    def __init__(self, prefix: str):
        self.ready_data = ViewBPMDataCollection(prefix + ":out:100ms")
        self.periodic_data = ViewBPMDataCollectionStats(prefix + ":out:2s")
        self.monitor_bpms = ViewBPMMonitoring(prefix + ":mon")
        self.monitor_update_cmd_errors = ViewStringBuffer(prefix + ":im:cmd_err")
