from ..data_model.bpm_data_collection import BPMDataCollection, BPMDataCollectionStats
import pydev

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
