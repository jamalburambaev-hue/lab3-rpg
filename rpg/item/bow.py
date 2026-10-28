from ..combat.hit import Hit
from ..core.dice import Dice
from .weapon import Weapon


class Bow(Weapon):
    CRITICAL_MULTIPLIER = 2

    def __init__(
        self, code: str, name: str, base_price: int, damage: int, critical_chance: float
    ) -> None:
        super().__init__(code, name, base_price, damage)
        self._critical_chance = critical_chance

    def roll_damage(self) -> Hit:
        if Dice().chance(self._critical_chance):
            return Hit(self.get_damage() * self.CRITICAL_MULTIPLIER, True)
        return Hit(self.get_damage(), False)

    def copy(self) -> "Bow":
        clone = Bow.__new__(Bow)
        self._copy_weapon_into(clone)
        clone._critical_chance = self._critical_chance
        return clone

    def get_description(self) -> str:
        return (
            f"урон {self.get_damage()}, "
            f"шанс крита {round(self._critical_chance * 100)}%"
        )