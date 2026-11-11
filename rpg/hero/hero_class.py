from enum import Enum
from typing import Callable

from ..core.exceptions import UnknownCodeException
from ..item.catalog import ItemCatalog
from ..kit.mage_kit import MageKitFactory
from ..kit.ranger_kit import RangerKitFactory
from ..kit.starter_kit import StarterKitFactory
from ..kit.warrior_kit import WarriorKitFactory

from ..item.armor import Armor
from ..defense.armor_handler import ArmorHandler
from ..defense.barrier_handler import BarrierHandler
from ..defense.evasion_handler import EvasionHandler
from ..defense.damage_handler import DamageHandler


class HeroClass(Enum):
    WARRIOR = ("warrior", "Воин", 120, WarriorKitFactory)
    RANGER = ("ranger", "Следопыт", 100, RangerKitFactory)
    MAGE = ("mage", "Маг", 85, MageKitFactory)

    def __init__(
        self, code: str, display_name: str, base_health: int,
        kit_factory: Callable[[ItemCatalog], StarterKitFactory]
    ) -> None:
        self._code = code
        self._display_name = display_name
        self._base_health = base_health
        self._kit_factory = kit_factory

    def get_starter_kit(self, catalog: ItemCatalog) -> StarterKitFactory:
        return self._kit_factory(catalog)

    @classmethod
    def by_code(cls, code: str) -> "HeroClass":
        for hero_class in cls:
            if hero_class.get_code() == code:
                return hero_class
        raise UnknownCodeException("Класс героя", code)

    def get_code(self) -> str:
        return self._code

    def get_display_name(self) -> str:
        return self._display_name

    def get_base_health(self) -> int:
        return self._base_health

    def create_defense(self, armor: Armor, level: int) -> DamageHandler:
        evasion = 0.15 if self == HeroClass.RANGER else 0.0
        barrier = 30 if self == HeroClass.MAGE else 0
        
        if self == HeroClass.WARRIOR and level >= 3:
            barrier = 20
        elif self == HeroClass.RANGER and level >= 5:
            barrier = 15
        elif self == HeroClass.MAGE and level >= 3:
            evasion = 0.10

        armor_handler = ArmorHandler(armor.get_defense())
        first = armor_handler

        if evasion > 0:
            first = EvasionHandler(evasion)
            first.set_next(armor_handler)
        
        if barrier > 0:
            armor_handler.set_next(BarrierHandler(barrier))

        return first