from typing import List
from ..enemy.dragon import Dragon
from ..enemy.enemy import Enemy
from ..item.catalog import ItemCatalog
from ..item.default_catalog import DAWN_BLADE, DRAGONSCALE_ARMOR
from .location import Location


class DragonLair(Location):
    CODE = "dragon-lair"

    def __init__(self, catalog: ItemCatalog) -> None:
        super().__init__(self.CODE, "Логово дракона", 5, catalog)

    def _create_enemy(self) -> Enemy:
        return Dragon()

    def _get_loot_table(self) -> List[str]:
        return [DAWN_BLADE, DRAGONSCALE_ARMOR]