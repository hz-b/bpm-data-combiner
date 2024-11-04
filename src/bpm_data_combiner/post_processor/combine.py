from typing import Sequence, Dict

import numpy as np
from ..data_model.bpm_data_accumulation import BPMDataAccumulation, BPMDataAccumulationForPlane
from ..data_model.bpm_data_collection import BPMDataCollection, BPMDataCollectionPlane
from ..data_model.bpm_data_reading import BPMReading


def _combine_collections_by_device_names(
    collections: Sequence[Dict[str, BPMReading]], dev_names_index: dict, *, default_value
) -> (np.ndarray, np.ndarray):
    """use the name to stuff data into correct location
    """
    # data and valid handled as two arrays: profiling showed that it was
    # considerably faster than using masked arrays
    res = np.empty([len(collections), 2, len(dev_names_index)], dtype=np.int32)
    res.fill(default_value)
    valid = np.empty([len(collections), 2, len(dev_names_index)], dtype=bool)
    valid.fill(False)

    # now fill data at appropriate place
    for row, data_collection in enumerate(collections):
        for name, bpm_data in data_collection.items():
            col = dev_names_index[name]
            for plane, val in enumerate([bpm_data.x, bpm_data.y]):
                if val is not None:
                    valid[row, plane, col] = True
                    res[row, plane, col] = val

    return res, valid


def collection_to_bpm_data_collection(
    collection: Dict[str, BPMReading], dev_names_index: Dict, default_value=2**31-1
):
    data, valid = _combine_collections_by_device_names([collection], dev_names_index,
                                              default_value=default_value)
    # only one collection -> first dimension one entry
    (data,) = data
    (valid,) = valid
    # need one reading to get its count
    for _, reading in collection.items():
        break
    return BPMDataCollection(
        x=BPMDataCollectionPlane(values=data[0], valid=valid[0]),
        y=BPMDataCollectionPlane(values=data[1], valid=valid[1]),
        names=list(dev_names_index),
        # assuming to be the same for both planes
        cnt=reading.cnt,
    )


def accumulated_collections_to_array(collections, dev_names_index):
    counts = np.zeros(len(collections), dtype=np.int64)
    for row, bpm_data in enumerate(collections):
        counts[row] = bpm_data.identifer

    x_values = np.array([bpm_data.x.values for bpm_data in collections])
    y_values = np.array([bpm_data.y.values for bpm_data in collections])
    x_valid = np.array([~bpm_data.x.valid for bpm_data in collections])
    y_valid = np.array([~bpm_data.y.valid for bpm_data in collections])

    return BPMDataAccumulation(
        x=BPMDataAccumulationForPlane(values=x_values, valid=~x_valid),
        y=BPMDataAccumulationForPlane(values=y_values, valid=~y_valid),
        names=list(dev_names_index),
        counts=counts,
    )
