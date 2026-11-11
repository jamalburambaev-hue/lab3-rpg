from .enemy_decorator import EnemyDecorator
from ..combat.hit import Hit

class WindfuryEnemy(EnemyDecorator):
    def get_name(self) -> str:
        return "Неистовый " + super().get_name()

    def roll_damage(self) -> Hit:
        first = super().roll_damage()
        second = super().roll_damage()
        return Hit(first.damage + second.damage, first.critical or second.critical)

    def get_experience_reward(self) -> int:
        reward = super().get_experience_reward()
        return reward + reward // 2

    def roll_gold_reward(self) -> int:
        reward = super().roll_gold_reward()
        return reward + reward // 2