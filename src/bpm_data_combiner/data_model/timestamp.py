from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class DataArrived:
    cnt:int
    name: str
    plane: str
    timestamp: datetime

    @property
    def dev_name(self):
        return self.name + ":" + self.plane