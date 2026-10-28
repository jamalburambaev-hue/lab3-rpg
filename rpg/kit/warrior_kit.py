from ..item.armor import Armor
from ..item.catalog import ItemCatalog
from ..item.default_catalog import CHAINMAIL, TRAINING_SWORD
from ..item.weapon import Weapon
from .starter_kit import StarterKitFactory


class WarriorKitFactory(StarterKitFactory):
    def __init__(self, catalog: ItemCatalog) -> None:
        self._catalog = catalog

    def create_weapon(self) -> Weapon:
        return self._catalog.create_weapon(TRAINING_SWORD)

    def create_armor(self) -> Armor:
        return self._catalog.create_armor(CHAINMAIL)