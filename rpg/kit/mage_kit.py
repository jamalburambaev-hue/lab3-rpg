from ..item.armor import Armor
from ..item.catalog import ItemCatalog
from ..item.default_catalog import APPRENTICE_STAFF, LINEN_ROBE
from ..item.weapon import Weapon
from .starter_kit import StarterKitFactory


class MageKitFactory(StarterKitFactory):
    def __init__(self, catalog: ItemCatalog) -> None:
        self._catalog = catalog

    def create_weapon(self) -> Weapon:
        return self._catalog.create_weapon(APPRENTICE_STAFF)

    def create_armor(self) -> Armor:
        return self._catalog.create_armor(LINEN_ROBE)