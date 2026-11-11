from ..combat.hit import Hit
from ..core.dice import Dice
from ..defense.damage import Damage
from ..item.weapon import Weapon
from .enemy import Enemy

class HauntedWeapon(Enemy):
    def __init__(self, weapon: Weapon):
        self._weapon = weapon
        self._max_health = weapon.get_damage() * 5
        self._health = self._max_health

    def get_code(self) -> str:
        return "haunted-weapon"

    def get_name(self) -> str:
        return "Одержимый " + self._weapon.get_name()

    def get_health(self) -> int:
        return self._health

    def get_max_health(self) -> int:
        return self._max_health

    def is_alive(self) -> bool:
        return self._health > 0

    def roll_damage(self) -> Hit:
        return self._weapon.roll_damage()

    def receive_hit(self, amount: int) -> Damage:
        damage = Damage(amount)
        self._health = max(0, self._health - damage.amount)
        return damage

    def get_experience_reward(self) -> int:
        return self._weapon.get_price() // 2

    def roll_gold_reward(self) -> int:
        return Dice().roll(self._weapon.get_price() // 4, self._weapon.get_price() // 2)