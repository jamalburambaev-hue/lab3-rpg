from .enemy_decorator import EnemyDecorator
from ..defense.damage import Damage

class ArmoredEnemy(EnemyDecorator):
    def get_name(self) -> str:
        return "Бронированный " + super().get_name()

    def receive_hit(self, amount: int) -> Damage:
        if amount < 0:
            raise ValueError("Урон не может быть отрицательным")
        if amount == 0:
            return Damage(0)
        return super().receive_hit(amount - amount // 2)