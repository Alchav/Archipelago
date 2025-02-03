from typing import NamedTuple, Optional, Callable
from BaseClasses import ItemClassification, CollectionState

class LocData(NamedTuple):
    id: int
    region: str
    rule: Optional[Callable[[CollectionState], bool]] = None
    event_name: str = None

class ItemData(NamedTuple):
    id: int
    classification: ItemClassification
    count: int = 1

class ExitData(NamedTuple):
    destination: str
    rule: Optional[Callable[[CollectionState], bool]] = None

class RegionData(NamedTuple):
    exits: list[ExitData] = []