from dataclasses import dataclass
from typing import Optional, Union, Hashable

from collector import CollectionItemInterface


@dataclass(frozen=True)
class BPMReading(CollectionItemInterface):
    """Representation of one bpm reading"""

    # Separate class: make it clear to further processing
    # that this has already been combined. If x or y will
    # now be None, then to indicate that the data there is
    # invalid
    #
    #: time count: in steps of 0.1 second since epoc
    #: i.e. since it was last triggered to synchronise
    cnt: int
    #: x position in nano meter
    x: Union[int, None]
    #: y position in nano meter
    y: Union[int, None]
    dev_name: str

    @property
    def identifier(self) -> Hashable:
        return self.cnt

    @property
    def source(self) -> Hashable:
        return self.dev_name


__all__ = ["BPMReading"]
