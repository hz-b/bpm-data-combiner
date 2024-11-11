from typing import Sequence, Dict

import numpy as np
from ..data_model.bpm_data_accumulation import BPMDataAccumulation, BPMDataAccumulationForSignal, BPMDataAccumlationPos, \
    BPMDataAccumlationQuality, BPMDataAccumlationButtons
from ..data_model.bpm_data_collection import BPMDataCollection, BPMDataCollectionSignal, BPMDataCollectionPos, \
    BPMDataCollectionQuality, BPMDataCollectionButtons
from ..data_model.bpm_data_reading import BPMReading


def _combine_collections_by_device_names(
    collections: Sequence[Dict[str, BPMReading]], dev_names_index: dict, *, default_value
) -> (np.ndarray, np.ndarray):
    """use the name to stuff data into correct location
    """
    # data and valid handled as two arrays: profiling showed that it was
    # considerably faster than using masked arrays
    pos = np.empty([len(collections), 2, len(dev_names_index)], dtype=np.int32)
    pos.fill(default_value)
    pos_valid = np.empty([len(collections), 2, len(dev_names_index)], dtype=bool)
    pos_valid.fill(False)

    quality = np.empty([len(collections), 2, len(dev_names_index)], dtype=np.int32)
    quality.fill(default_value)
    quality_valid = np.empty([len(collections), 2, len(dev_names_index)], dtype=bool)
    quality_valid.fill(False)

    buttons = np.empty([len(collections), 4, len(dev_names_index)], dtype=np.int32)
    buttons.fill(default_value)
    buttons_valid = np.empty([len(collections), 4, len(dev_names_index)], dtype=bool)
    buttons_valid.fill(False)

    # now fill data at appropriate place
    for row, data_collection in enumerate(collections):
        for name, bpm_data in data_collection.items():
            col = dev_names_index[name]
            for plane, val in enumerate([bpm_data.pos.x, bpm_data.pos.y]):
                if val is not None:
                    pos_valid[row, plane, col] = True
                    pos[row, plane, col] = val
            del plane
            if bpm_data.quality:
                for type_, val in enumerate([bpm_data.quality.sum, bpm_data.quality.q]):
                    quality_valid[row, type_, col] = True
                    quality[row, type_, col] = val
                del type_
            if bpm_data.buttons:
                bb = bpm_data.buttons
                for button, val in enumerate([bb.a, bb.b, bb.c, bb.d]):
                    if val is not None:
                        buttons_valid[row, button, col] = True
                        buttons[row, button, col] = val

    return (pos, pos_valid), (quality, quality_valid), (buttons, buttons_valid)


def collection_to_bpm_data_collection(
    collection: Dict[str, BPMReading], dev_names_index: Dict, default_value=2**31-1
):
    pos_t, quality_t, buttons_t = _combine_collections_by_device_names([collection], dev_names_index,
                                              default_value=default_value)

    # only one collection -> first dimension one entry
    (data,) = pos_t[0]
    (valid,) = pos_t[1]
    pos = BPMDataCollectionPos(
        x=BPMDataCollectionSignal(values=data[0], valid=valid[0]),
        y=BPMDataCollectionSignal(values=data[1], valid=valid[1]),
    )
    del pos_t

    # Todo: add a check if there is any data at all ?
    (data,) = quality_t[0]
    (valid,) = quality_t[1]
    quality = BPMDataCollectionQuality(
        sum=BPMDataCollectionSignal(values=data[0], valid=valid[0]),
        q=BPMDataCollectionSignal(values=data[1], valid=valid[1]),
    )
    del quality_t

    # Todo: add a check if there is any data at all ?
    (data,) = buttons_t[0]
    (valid,) = buttons_t[1]
    buttons = BPMDataCollectionButtons(
        a=BPMDataCollectionSignal(values=data[0], valid=valid[0]),
        b=BPMDataCollectionSignal(values=data[1], valid=valid[1]),
        c=BPMDataCollectionSignal(values=data[2], valid=valid[2]),
        d=BPMDataCollectionSignal(values=data[3], valid=valid[3]),
    )
    del buttons_t

    # need one reading to get its count
    for _, reading in collection.items():
        break
    return BPMDataCollection(
        names=tuple(dev_names_index),
        pos=pos,
        quality=quality,
        buttons=buttons,
        # assuming to be the same for both planes
        cnt=reading.cnt,
    )


def accumulated_collections_to_array(collections, dev_names_index):
    counts = np.zeros(len(collections), dtype=np.int64)
    for row, bpm_data in enumerate(collections):
        counts[row] = bpm_data.identifer

    def to_accumulated_signal(col: collections, extractor) -> BPMDataAccumulationForSignal:
        return BPMDataAccumulationForSignal(
                values=np.array([extractor(bpm_data).values for bpm_data in collections]),
                valid=np.array([extractor(bpm_data).valid for bpm_data in collections]),
            )

    return BPMDataAccumulation(
        pos=BPMDataAccumlationPos(
            x=to_accumulated_signal(collections, lambda col: col.pos.x),
            y=to_accumulated_signal(collections, lambda col: col.pos.y),
        ),
        quality=BPMDataAccumlationQuality(
            sum=to_accumulated_signal(collections, lambda col: col.quality.sum),
            q=to_accumulated_signal(collections, lambda col: col.quality.q),
        ),
        buttons=BPMDataAccumlationButtons(
            a=to_accumulated_signal(collections, lambda col: col.buttons.a),
            b=to_accumulated_signal(collections, lambda col: col.buttons.b),
            c=to_accumulated_signal(collections, lambda col: col.buttons.c),
            d=to_accumulated_signal(collections, lambda col: col.buttons.d),
        ),
        names=tuple(dev_names_index),
        counts=counts,
    )
