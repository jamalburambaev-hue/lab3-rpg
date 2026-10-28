from abc import abstractmethod
from typing import List

from ..combat.hit import Hit
from .enchantment import FOR_WEAPONS, Enchantment
from .item import Item


class Weapon(Item):
    def __init__(self, code: str, name: str, base_price: int, damage: int) -> None:
        super().__init__(code, name, base_price)
        self._damage = damage

    @abstractmethod
    def roll_damage(self) -> Hit: ...

    @abstractmethod
    def copy(self) -> "Weapon": ...

    def get_damage(self) -> int:
        return self._damage + sum(e.bonus_damage for e in self.get_enchantments())

    def get_possible_enchantments(self) -> List[Enchantment]:
        return FOR_WEAPONS

    def _copy_weapon_into(self, target: "Weapon") -> None:
        self._copy_common_into(target)
        target._damage = self._damage