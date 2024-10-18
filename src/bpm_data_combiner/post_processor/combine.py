from typing import Sequence, Dict

import numpy as np
from numpy import ma as ma
from ..data_model.bpm_data_accumulation import BPMDataAccumulation, BPMDataAccumulationForPlane
from ..data_model.bpm_data_collection import BPMDataCollection, BPMDataCollectionPlane
from ..data_model.bpm_data_reading import BPMReading


def _combine_collections_by_device_names(
    collections: Sequence[Dict[str, BPMReading]], dev_names_index: dict, *, default_value
) -> ma.masked_array:
    """use the name to stuff data into correct location

    Todo:
        Should it return a masked array? Is there a better
        representation?
    """
    res = np.empty([len(collections), len(dev_names_index), 2], dtype=np.int32)
    res.fill(default_value)
    res = ma.array(res, mask=True)

    # now fill data at appropriate place
    # todo: handle that x and y plane can be enabled separately
    for row, data_collection in enumerate(collections):
        for name, bpm_data in data_collection.items():
            col = dev_names_index[name]
            res.mask[row, col, :] = False
            for plane, val in enumerate([bpm_data.x, bpm_data.y]):
                if val is None:
                    res[row, col, plane].mask = True
                else:
                    res[row, col, plane] = val

    return res


def collection_to_bpm_data_collection(
    collection: Dict[str, BPMReading], dev_names_index: Dict, default_value=2**31-1
):
    ma = _combine_collections_by_device_names([collection], dev_names_index,
                                              default_value=default_value)
    # only one collection -> first dimension one entry
    (ma,) = ma
    # need one reading to get its count
    for _, reading in collection.items():
        break
    return BPMDataCollection(
        x=BPMDataCollectionPlane(values=ma[:, 0], valid=~ma.mask[:,0]),
        y=BPMDataCollectionPlane(values=ma[:, 1], valid=~ma.mask[:,1]),
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
