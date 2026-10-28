from typing import List
from ..enemy.enemy import Enemy
from ..enemy.goblin import Goblin
from ..item.catalog import ItemCatalog
from ..item.default_catalog import GOBLIN_CLEAVER, HUNTING_BOW, LEATHER_ARMOR
from .location import Location


class Forest(Location):
    CODE = "forest"

    def __init__(self, catalog: ItemCatalog) -> None:
        super().__init__(self.CODE, "Мистический лес", 1, catalog)

    def _create_enemy(self) -> Enemy:
        return Goblin()

    def _get_loot_table(self) -> List[str]:
        return [GOBLIN_CLEAVER, HUNTING_BOW, LEATHER_ARMOR]