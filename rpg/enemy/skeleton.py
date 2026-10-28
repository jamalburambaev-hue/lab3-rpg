from .abstract_enemy import AbstractEnemy


class Skeleton(AbstractEnemy):
    RESISTANCE = 0.3

    def __init__(self) -> None:
        super().__init__("skeleton", "Скелет", 110, 10, 24, 90, 70)

    def _reduce_damage(self, damage: int) -> int:
        return round(damage * (1 - self.RESISTANCE))