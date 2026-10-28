from abc import ABC, abstractmethod

from .hit import Hit


class Combatant(ABC):
    """Всё, что может участвовать в бою: и герой, и враги."""

    @abstractmethod
    def get_code(self) -> str: ...

    @abstractmethod
    def get_name(self) -> str: ...

    @abstractmethod
    def get_health(self) -> int: ...

    @abstractmethod
    def get_max_health(self) -> int: ...

    @abstractmethod
    def is_alive(self) -> bool: ...

    @abstractmethod
    def roll_damage(self) -> Hit: ...

    @abstractmethod
    def receive_hit(self, damage: int) -> int: ...