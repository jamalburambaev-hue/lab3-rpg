from ..combat.hit import Hit
from .weapon import Weapon


class Sword(Weapon):
    def roll_damage(self) -> Hit:
        return Hit(self.get_damage(), False)

    def copy(self) -> "Sword":
        clone = Sword.__new__(Sword)
        self._copy_weapon_into(clone)
        return clone

    def get_description(self) -> str:
        return f"урон {self.get_damage()}"