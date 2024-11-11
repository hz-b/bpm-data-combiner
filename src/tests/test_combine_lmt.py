import numpy as np

from bpm_data_combiner.app.util import combine_counts


def combine_int8(high, low):
    return (high << 8) | np.array(low).astype(np.uint8)


def combine_int16(high, low):
    return (high << 16) | np.array(low).astype(np.uint16)


def combine_int32(high, low):
    return (high << 32) | np.array(low).astype(np.uint32)


def test_combine_int8():
    for low, ref in zip([127, -128, -127], [127, 128, 129]):
        assert combine_int8(0, low) == ref

    assert combine_int8(0, -2) == 254
    assert combine_int8(0, -1) == 255
    assert combine_int8(1, 0) == 256
    assert combine_int8(1, 1) == 257


def test_combine_int16():
    val = 0x7FFF

# fmt:off
    for low, ref in zip(
        [val - 1, val, -val - 1, -val - 1 + 1],
        [val - 1, val,  val + 1,  val + 2    ]
    ):
# fmt:on
        assert combine_int16(0, low) == ref


def test_combine_int32():
    val = 0x7FFFFFFF
# fmt:off
    for low, ref in zip(
        [val - 1, val, -val - 1, -val - 1 + 1],
        [val - 1, val,  val + 1,  val + 2    ]
    ):
# fmt:on
        assert combine_int32(0, low) == ref
        assert combine_counts(0, low) == ref
        assert combine_counts(1, low) == ref + 0xffffffff + 1