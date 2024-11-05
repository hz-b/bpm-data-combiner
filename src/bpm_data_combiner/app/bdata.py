from typing import Sequence, Mapping
import numpy as np

from ..data_model.bpm_data_collection import BPMDataCollectionStats

# is this the correct way to convert the data ?
scale_bits = 2 ** 15 / 10

# scale rms so that the slow orbit feedback accepts the data
# factor 100 seems to be enough.
# I think I should add some check that the noise is large enough
scale_rms = 20

nm2mm = 1e-6


def convert(data: Sequence[float], scale_axis: float = 1.0):
    """
    Todo:
        include conversion to np.int16 at this stage?
    """
    return (np.asarray(data) * (nm2mm * scale_bits * scale_axis)).astype(np.int16)


def convert_noise(data, scale_axis: float = 1):
    noise = convert(data.std, scale_axis=scale_axis * scale_rms)
    # at least one bit has to be set ...
    # otherwise it will not consider it as noise
    noise[data.n_readings > 0] = np.clip(noise, 1, None)[data.n_readings > 0]
    # so sofb Orbit will consider it as not existing
    noise[data.n_readings <= 0] = 0
    return noise


def stat_data_to_bdata(
    data: BPMDataCollectionStats,
    *,
    device_index: Mapping[str, int],
    n_bpms: int,
    scale_x_axis: float
):
    """
    device_names: need to contain empty ones too, e.g. as None empty or any
                  other unique place holder

    Todo:
        do I need to map data to positions again?
        How is stat handling it
    """
    n_entries = len(data.x.values)
    if n_entries > n_bpms:
        raise ValueError("number of bpms %s too many. max %s", n_entries, n_bpms)

    bdata = np.empty([8, n_bpms], dtype=np.int16)
    bdata.fill(0.0)

    indices = [device_index[name] for name in data.names]
    # flipping coordinate system to get the dispersion on the correct side
    # todo: check at which state this should be done
    # fmt:off
    bdata[0, indices] = - convert(data.x.values, scale_axis=scale_x_axis)
    bdata[1, indices] =   convert(data.y.values)
    # fmt:on
    # intensity z 1.3
    # bdata[2] = 3
    # intensityz z 1.3
    # bdata[3] = 3
    # AGC status needs to be three for valid data
    # todo: find out what to set if only one plane is valid?
    bdata[4, indices] = np.where(
        (data.x.n_readings > 0) | (data.y.n_readings > 0), 3, 0
    )
    bdata[4, -1] = 2

    bdata[6, indices] = convert_noise(data.x, scale_axis=scale_x_axis)
    bdata[7, indices] = convert_noise(data.y)

    return bdata


__all__ = ["stat_data_to_bdata"]
