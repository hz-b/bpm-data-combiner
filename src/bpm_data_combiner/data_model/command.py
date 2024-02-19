from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Command:
    cmd : str
    dev_name : str
    kwargs : dict
    timestamp: datetime
