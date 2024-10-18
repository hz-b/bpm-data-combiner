from typing import Sequence, Dict

import numpy as np
from bpm_data_combiner.data_model.bpm_data_collection import BPMDataCollection, BPMDataCollectionPlane
from bpm_data_combiner.data_model.bpm_data_reading import BPMReading
from numpy import ma as ma


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
