from dataclasses import dataclass
from typing import Optional


@dataclass
class BPMReadingBeingProcessed:
    """Representation of one bpm reading
    """
    #: time count: 0.1 s since device epoc:
    #: i.e. since it was last triggered to synchronise
    cnt: int
    #: x position in nano meter
    x: Optional[int] = None
    #: y position in nano meter
    y: Optional[int] = None

    def ready(self, chk_cnt):
        return self.x is not None and self.y is not None and self.cnt == chk_cnt


#: used to be sent further around:
#: todo: an unncessary optimisation ?
@dataclass(frozen=True)
class BPMReading:
    # Separate class: make it clear to further processing
    # that this will not change
    #: time count: 0.1 s since device epoc:
    #: i.e. since it was last triggered to synchronise
    cnt: int
    #: x position in nano meter
    x: int
    #: y position in nano meter
    y: int
    dev_name: str