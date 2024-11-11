from dataclasses import dataclass
from typing import Optional, Union, Hashable

from collector import CollectionItemInterface


@dataclass(frozen=True)
class BPMReadingButtons:
    """

    Todo:
        * could there be a better name for the position ?
        * quadrants?
        * top / bottom
        * inner / outer
    """
    a: int
    b: int
    c: int
    d: int


@dataclass(frozen=True)
class BPMReadingPos:
    """

    Todo:
        * better naming?
        * horizontal / vertical ?
        * plane 1 / 2 / 3
    """
    x: Union[int, None]
    y: Union[int, None]


@dataclass(frozen=True)
class BPMReadingQuality:
    """
    Todo: find a better name for it
    """
    sum: int
    q: int


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
    pos: BPMReadingPos
    quality : BPMReadingQuality
    buttons : BPMReadingButtons
    dev_name: str

    @property
    def identifier(self) -> Hashable:
        return self.cnt

    @property
    def source(self) -> Hashable:
        return self.dev_name


__all__ = ["BPMReading"]
