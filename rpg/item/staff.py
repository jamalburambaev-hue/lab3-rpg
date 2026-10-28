from ..combat.hit import Hit
from ..core.dice import Dice
from .weapon import Weapon


class Staff(Weapon):
    def __init__(
        self, code: str, name: str, base_price: int, damage: int, scatter: float
    ) -> None:
        super().__init__(code, name, base_price, damage)
        self._scatter = scatter

    def roll_damage(self) -> Hit:
        return Hit(Dice().roll(self._min_damage(), self._max_damage()), False)

    def copy(self) -> "Staff":
        clone = Staff.__new__(Staff)
        self._copy_weapon_into(clone)
        clone._scatter = self._scatter
        return clone

    def get_description(self) -> str:
        return f"урон {self._min_damage()}-{self._max_damage()}"

    def _min_damage(self) -> int:
        return round(self.get_damage() * (1 - self._scatter))

    def _max_damage(self) -> int:
        return round(self.get_damage() * (1 + self._scatter))