from ..data_model.bpm_data_collection import BPMDataCollection, BPMDataCollectionStats
import logging
from typing import Sequence

import pydev

logger = logging.getLogger("bpm-data-combiner")

def string_array_to_bytes(names: Sequence[str], *, encoding = "utf8"):
    return [bytes(name, encoding) for name in names]


class ViewBPMMonitoring:
    def __init__(self, prefix: str):
        self.prefix = prefix

    def update(self, names : Sequence[str], active: Sequence[bool]):
        names =  string_array_to_bytes(names)
        label = self.prefix + ":" + "names"
        logger.debug("Update active view label %s, values %s", label, names)
        pydev.iointr(label, names)

        # int number wrong by a factor of 2: why?
        active = [bool(v) for v in active]
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

            label = f"{self.prefix}:{suffix}:active"
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
            # ints are now used
            values = [int(v) for v in values]
            logger.debug("Update label %s, values %s", label, values)
            pydev.iointr(label, values)


        label = self.prefix + ":names"
        pydev.iointr(label, string_array_to_bytes(data.names))

        label = self.prefix + ":cnt"
        pydev.iointr(label, data.cnt)


class ViewBPMDataCollectionStats:
    def __init__(self, prefix: str):
        self.prefix = prefix

    def update(self, data: BPMDataCollectionStats):
        for plane, plane_var in [("x", data.x), ("y", data.y)]:
            for suffix, var in [("values", plane_var.values), ("std", plane_var.std)]:
                label = f"{self.prefix}:{plane}:{suffix}"
                pydev.iointr(label, var)

        for suffix, var in[("names", string_array_to_bytes(data.names)), ("cnt", data.cnt)]:
            label = self.prefix + ":" + suffix
            pydev.iointr(label, var)


class ViewStringBuffer:
    def __init__(self, label: str):
        self.label = label

    def update(self, buf: Sequence[str]):
        # logger.warning(f'View string {self.label}:"{t_str}"')
        pydev.iointr(self.label, string_array_to_bytes(buf))


class Views:
    def __init__(self, prefix: str):
        self.ready_data = ViewBPMDataCollection(prefix + ":out:100ms")
        self.periodic_data = ViewBPMDataCollectionStats(prefix + ":periodic")
        self.monitor_bpms = ViewBPMMonitoring(prefix + ":mon")
        self.monitor_update_cmd_errors =  ViewStringBuffer(prefix + ":im:cmd_err")
