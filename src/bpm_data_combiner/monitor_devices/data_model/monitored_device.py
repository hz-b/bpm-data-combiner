from enum import Enum, IntEnum


class PlaneNames(Enum):
    x = "x"
    y = "y"


class SynchronisationStatus(IntEnum):
    no_sync = 0
    tracking = 1
    synchronised = 2