from .enemy import Enemy
from ..combat.hit import Hit
from ..defense.damage import Damage

class EnemyDecorator(Enemy):
    def __init__(self, wrapped: Enemy):
        self._wrapped = wrapped

    def get_code(self) -> str:
        return self._wrapped.get_code()

    def get_name(self) -> str:
        return self._wrapped.get_name()

    def get_health(self) -> int:
        return self._wrapped.get_health()

    def get_max_health(self) -> int:
        return self._wrapped.get_max_health()

    def is_alive(self) -> bool:
        return self._wrapped.is_alive()

    def roll_damage(self) -> Hit:
        return self._wrapped.roll_damage()

    def receive_hit(self, amount: int) -> Damage:
        return self._wrapped.receive_hit(amount)

    def get_experience_reward(self) -> int:
        return self._wrapped.get_experience_reward()

    def roll_gold_reward(self) -> int:
        return self._wrapped.roll_gold_reward()