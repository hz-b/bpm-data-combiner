from dataclasses import dataclass


@dataclass(frozen=True)
class Command:
    cmd : str
    dev_name : str
    kwargs : dict
    datetime: datetime
