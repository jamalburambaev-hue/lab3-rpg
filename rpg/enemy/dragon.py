from ..combat.hit import Hit
from ..core.dice import Dice
from .abstract_enemy import AbstractEnemy


class Dragon(AbstractEnemy):
    RESISTANCE = 0.25
    FIRE_BREATH_CHANCE = 0.25
    FIRE_BREATH_MULTIPLIER = 2

    def __init__(self) -> None:
        super().__init__("dragon", "Дракон", 260, 16, 22, 500, 400)

    def roll_damage(self) -> Hit:
        bite = super().roll_damage()
        if Dice().chance(self.FIRE_BREATH_CHANCE):
            return Hit(bite.damage * self.FIRE_BREATH_MULTIPLIER, True)
        return bite

    def _reduce_damage(self, damage: int) -> int:
        return round(damage * (1 - self.RESISTANCE))