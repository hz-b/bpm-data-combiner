from dataclasses import dataclass
from typing import Union, Hashable


@dataclass
class CollectionItem:
    #: identifier of the package, unique for the sender
    id_: Union[int|Hashable]
    #: identifier for the sender
    name: str
    payload : object