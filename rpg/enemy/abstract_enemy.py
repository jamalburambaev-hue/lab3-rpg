from ..combat.hit import Hit
from ..core.dice import Dice
from .enemy import Enemy


class AbstractEnemy(Enemy):
    def __init__(
        self, code: str, name: str, max_health: int,
        min_damage: int, max_damage: int,
        experience_reward: int, gold_reward: int
    ) -> None:
        self._code = code
        self._name = name
        self._max_health = max_health
        self._min_damage = min_damage
        self._max_damage = max_damage
        self._experience_reward = experience_reward
        self._gold_reward = gold_reward
        self._health = max_health

    def get_code(self) -> str:
        return self._code

    def get_name(self) -> str:
        return self._name

    def get_health(self) -> int:
        return self._health

    def get_max_health(self) -> int:
        return self._max_health

    def is_alive(self) -> bool:
        return self._health > 0

    def roll_damage(self) -> Hit:
        return Hit(Dice().roll(self._min_damage, self._max_damage), False)

    def receive_hit(self, damage: int) -> int:
        dealt = max(1, self._reduce_damage(damage))
        self._health = max(0, self._health - dealt)
        return dealt

    def _reduce_damage(self, damage: int) -> int:
        return damage

    def roll_gold_reward(self) -> int:
        return Dice().roll(self._gold_reward // 2, self._gold_reward)

    def get_experience_reward(self) -> int:
        return self._experience_reward