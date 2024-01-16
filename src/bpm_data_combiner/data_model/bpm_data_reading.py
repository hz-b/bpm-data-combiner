from dataclasses import dataclass
from typing import Optional, Union


@dataclass
class BPMReadingBeingProcessed:
    """don't use this class use :class:`BPMReading` instead"""

    #: time count: 0.1 s since device epoc
    #: i.e. since it was last triggered to synchronise
    cnt: int
    dev_name : str
    #: x position in nano meter
    x: Optional[int] = None
    #: y position in nano meter
    y: Optional[int] = None

    def ready(self, chk_cnt):
        return self.x is not None and self.y is not None and self.cnt == chk_cnt


@dataclass(frozen=True)
class BPMReading:
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


__all__ = ["BPMReading"]
