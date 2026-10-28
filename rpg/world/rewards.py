from dataclasses import dataclass
from typing import Optional
from ..item.item import Item

@dataclass(frozen=True)
class Rewards:
    experience: int
    gold: int
    loot: Optional[Item]
    levels_gained: int