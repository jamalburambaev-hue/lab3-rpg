from enum import Enum
from typing import Callable

from ..core.exceptions import UnknownCodeException
from ..item.catalog import ItemCatalog
from ..kit.mage_kit import MageKitFactory
from ..kit.ranger_kit import RangerKitFactory
from ..kit.starter_kit import StarterKitFactory
from ..kit.warrior_kit import WarriorKitFactory


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