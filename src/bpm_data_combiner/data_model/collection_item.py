from dataclasses import dataclass


@dataclass
class CollectionItem:
    cnt: int
    name: str
    payload : object