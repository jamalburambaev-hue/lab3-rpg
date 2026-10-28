import random
from typing import List, TypeVar

T = TypeVar("T")


class Dice:
    """Одиночка: единственный источник случайности на всю игру."""

    _instance: "Dice | None" = None

    def __new__(cls) -> "Dice":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        if self._initialized:
            return
        self._random = random.Random()
        self._initialized = True

    def reseed(self, seed: int) -> None:
        self._random.seed(seed)

    def next_seed(self) -> int:
        return self._random.randint(0, 999_999)

    def roll(self, min_value: int, max_value: int) -> int:
        return self._random.randint(min_value, max_value)

    def chance(self, probability: float) -> bool:
        return self._random.random() < probability

    def pick(self, options: List[T]) -> T:
        return options[self._random.randrange(len(options))]