from .enemy_decorator import EnemyDecorator
from ..combat.hit import Hit

class LegendaryEnemy(EnemyDecorator):
    def get_name(self) -> str:
        return "Легендарный " + super().get_name()

    def roll_damage(self) -> Hit:
        hit = super().roll_damage()
        return Hit(hit.damage * 2, hit.critical)

    def get_experience_reward(self) -> int:
        return super().get_experience_reward() * 2

    def roll_gold_reward(self) -> int:
        return super().roll_gold_reward() * 2