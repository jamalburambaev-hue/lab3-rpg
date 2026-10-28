from typing import List
from ..enemy.enemy import Enemy
from ..enemy.skeleton import Skeleton
from ..item.catalog import ItemCatalog
from ..item.default_catalog import BONE_BOW, CRYPT_MAIL, KNIGHT_BLADE, NECROMANCER_STAFF
from .location import Location


class Crypt(Location):
    CODE = "crypt"

    def __init__(self, catalog: ItemCatalog) -> None:
        super().__init__(self.CODE, "Заброшенный склеп", 3, catalog)

    def _create_enemy(self) -> Enemy:
        return Skeleton()

    def _get_loot_table(self) -> List[str]:
        return [KNIGHT_BLADE, BONE_BOW, NECROMANCER_STAFF, CRYPT_MAIL]