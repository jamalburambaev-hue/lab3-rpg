from abc import ABC, abstractmethod
from .damage import Damage

class DamageHandler(ABC):
    def __init__(self):
        self._next = None

    def set_next(self, handler):
        self._next = handler
        return handler

    @abstractmethod
    def handle(self, damage: Damage) -> None:
        ...

    def _pass_to_next(self, damage: Damage) -> None:
        if self._next:
            self._next.handle(damage)