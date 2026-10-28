from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Enchantment:
    """Зачарование неизменяемо: его нельзя поменять после создания."""
    code: str
    name: str
    bonus_damage: int
    bonus_defense: float
    bonus_price: int


SHARP = Enchantment("sharp", "Острое", 3, 0.0, 20)
FIERY = Enchantment("fiery", "Огненное", 6, 0.0, 50)
STURDY = Enchantment("sturdy", "Прочное", 0, 0.05, 20)
WARDING = Enchantment("warding", "Охранное", 0, 0.10, 50)

FOR_WEAPONS: List[Enchantment] = [SHARP, FIERY]
FOR_ARMOR: List[Enchantment] = [STURDY, WARDING]