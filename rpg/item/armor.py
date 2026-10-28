from typing import List

from .enchantment import FOR_ARMOR, Enchantment
from .item import Item


class Armor(Item):
    MAX_DEFENSE = 0.75

    def __init__(
        self, code: str, name: str, base_price: int, defense: float
    ) -> None:
        super().__init__(code, name, base_price)
        self._defense = defense

    def copy(self) -> "Armor":
        clone = Armor.__new__(Armor)
        self._copy_common_into(clone)
        clone._defense = self._defense
        return clone

    def get_defense(self) -> float:
        total = self._defense + sum(
            e.bonus_defense for e in self.get_enchantments()
        )
        return min(total, self.MAX_DEFENSE)

    def get_possible_enchantments(self) -> List[Enchantment]:
        return FOR_ARMOR

    def get_description(self) -> str:
        return f"защита {round(self.get_defense() * 100)}%"