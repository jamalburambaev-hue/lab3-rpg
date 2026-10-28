from abc import ABC, abstractmethod

from ..item.armor import Armor
from ..item.weapon import Weapon


class StarterKitFactory(ABC):
    """Абстрактная фабрика: стартовый набор снаряжения."""

    @abstractmethod
    def create_weapon(self) -> Weapon: ...

    @abstractmethod
    def create_armor(self) -> Armor: ...