from .abstract_enemy import AbstractEnemy


class Goblin(AbstractEnemy):
    def __init__(self) -> None:
        super().__init__("goblin", "Гоблин", 50, 6, 14, 40, 30)