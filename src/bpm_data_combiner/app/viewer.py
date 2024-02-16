from ..data_model.bpm_data_collection import BPMDataCollection, BPMDataCollectionStats
import pydev

import logging
from typing import Sequence

logger = logging.getLogger("bpm-data-combiner")


class ViewBPMMonitoring:
    def __init__(self, prefix: str):
        self.prefix = prefix

    def update(self, names : Sequence[str], active: Sequence[bool]):
        names = [bytes(name, "utf8") for name in names]
        active = [bool(v) for v in active]
        label = self.prefix + ":" + "names"
        logger.debug("Update active view label %s, values %s", label, names)
        pydev.iointr(label, names)

        # int number wrong by a factor of 2: why?
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
            # ints are now used
            vals = [int(v) for v in values]
            logger.debug("Update label %s, values %s", label, vals)
            pydev.iointr(label, vals)


        label = self.prefix + ":names"
        names = [bytes(name, "utf8") for name in data.names]
        pydev.iointr(label, names)


class ViewBPMDataCollectionStats:
    def __init__(self, prefix: str):
        self.prefix = prefix

    def update(self, data: BPMDataCollectionStats):
        for plane, plane_var in [("x", data.x), ("y", data.y)]:
            for suffix, var in [("values", plane_var.values), ("weights", plane_var.weights)]:
                label = f"{self.prefix}:{plane}:{suffix}"
                pydev.iointr(label, var)

        for suffix, var in[("names", data.names), ("cnt", data.cnt)]:
            label = self.prefix + ":" + suffix
            pydev.iointr(label, var)


class Viewer:
    def __init__(self, prefix: str):
        self.ready_data = ViewBPMDataCollection(prefix + ":out:100ms")
        self.periodic_data = ViewBPMDataCollectionStats(prefix + ":periodic")
        self.monitor_bpms = ViewBPMMonitoring(prefix + ":mon")
