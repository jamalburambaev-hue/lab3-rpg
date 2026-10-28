from typing import Dict, List

from ..core.exceptions import UnknownCodeException
from .armor import Armor
from .item import Item
from .weapon import Weapon


class ItemCatalog:
    """Хранит шаблоны предметов и отдаёт наружу только их копии."""

    def __init__(self) -> None:
        self._prototypes: Dict[str, Item] = {}

    def register(self, prototype: Item) -> None:
        self._prototypes[prototype.get_code()] = prototype

    def create(self, code: str) -> Item:
        prototype = self._prototypes.get(code)
        if prototype is None:
            raise UnknownCodeException("Предмет", code)
        return prototype.copy()

    def create_weapon(self, code: str) -> Weapon:
        item = self.create(code)
        if isinstance(item, Weapon):
            return item
        raise ValueError(f"Предмет '{code}' не является оружием")

    def create_armor(self, code: str) -> Armor:
        item = self.create(code)
        if isinstance(item, Armor):
            return item
        raise ValueError(f"Предмет '{code}' не является броней")

    def get_codes(self) -> List[str]:
        return list(self._prototypes.keys())