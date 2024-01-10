from dataclasses import dataclass
from datetime import datetime
from typing import Union


@dataclass(frozen=True)
class DataArrived:
    cnt:int
    dev_name: str
    timestamp: Union[datetime, float]
