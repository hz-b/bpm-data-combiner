from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class DataArrived:
    cnt:int
    dev_name: str
    timestamp: datetime | float
