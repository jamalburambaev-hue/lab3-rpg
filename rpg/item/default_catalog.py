from .armor import Armor
from .bow import Bow
from .catalog import ItemCatalog
from .staff import Staff
from .sword import Sword

TRAINING_SWORD = "training-sword"
HUNTING_BOW = "hunting-bow"
APPRENTICE_STAFF = "apprentice-staff"
CHAINMAIL = "chainmail"
LEATHER_ARMOR = "leather-armor"
LINEN_ROBE = "linen-robe"

IRON_SWORD = "iron-sword"
ELVEN_BOW = "elven-bow"
EMBER_STAFF = "ember-staff"
PLATE_ARMOR = "plate-armor"

GOBLIN_CLEAVER = "goblin-cleaver"
BONE_BOW = "bone-bow"
NECROMANCER_STAFF = "necromancer-staff"
KNIGHT_BLADE = "knight-blade"
CRYPT_MAIL = "crypt-mail"
DAWN_BLADE = "dawn-blade"
DRAGONSCALE_ARMOR = "dragonscale-armor"


def create_default_catalog() -> ItemCatalog:
    catalog = ItemCatalog()

    catalog.register(Sword(TRAINING_SWORD, "Тренировочный меч", 20, 12))
    catalog.register(Bow(HUNTING_BOW, "Охотничий лук", 20, 10, 0.3))
    catalog.register(Staff(APPRENTICE_STAFF, "Посох ученика", 20, 14, 0.3))
    catalog.register(Armor(CHAINMAIL, "Кольчуга", 40, 0.3))
    catalog.register(Armor(LEATHER_ARMOR, "Кожаная броня", 30, 0.2))
    catalog.register(Armor(LINEN_ROBE, "Льняная роба", 15, 0.1))

    catalog.register(Sword(IRON_SWORD, "Железный меч", 80, 17))
    catalog.register(Bow(ELVEN_BOW, "Эльфийский лук", 90, 14, 0.4))
    catalog.register(Staff(EMBER_STAFF, "Тлеющий посох", 90, 20, 0.3))
    catalog.register(Armor(PLATE_ARMOR, "Латы", 120, 0.4))

    catalog.register(Sword(GOBLIN_CLEAVER, "Гоблинский тесак", 40, 15))
    catalog.register(Bow(BONE_BOW, "Костяной лук", 140, 17, 0.4))
    catalog.register(Staff(NECROMANCER_STAFF, "Посох некроманта", 150, 25, 0.35))
    catalog.register(Sword(KNIGHT_BLADE, "Клинок рыцаря", 150, 23))
    catalog.register(Armor(CRYPT_MAIL, "Кольчуга стража склепа", 160, 0.45))
    catalog.register(Sword(DAWN_BLADE, "Клинок рассвета", 500, 35))
    catalog.register(Armor(DRAGONSCALE_ARMOR, "Драконья чешуя", 500, 0.55))

    return catalog