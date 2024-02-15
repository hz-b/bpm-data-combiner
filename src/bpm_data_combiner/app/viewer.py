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
        for suffix, var in [("x", data.x), ("y", data.y), ("names", data.names), ("cnt", data.cnt)]:
            label = self.prefix + ":" + suffix
            pydev.iointr(label, var)


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
        self.ready_data = ViewBPMDataCollection(prefix + ":ready")
        self.periodic_data = ViewBPMDataCollectionStats(prefix + ":periodic")
        self.monitor_bpms = ViewBPMMonitoring(prefix + ":mon")
