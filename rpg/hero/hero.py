from typing import List

from ..combat.combatant import Combatant
from ..combat.hit import Hit
from ..item.armor import Armor
from ..item.item import Item
from ..item.weapon import Weapon
from ..kit.starter_kit import StarterKitFactory
from .hero_class import HeroClass


class Hero(Combatant):
    MAX_NAME_LENGTH = 20
    STARTING_GOLD = 50
    HEALTH_PER_LEVEL = 15
    DAMAGE_PER_LEVEL = 3
    EXPERIENCE_PER_LEVEL = 100

    def __init__(self, builder: "Hero.Builder") -> None:
        self._name = builder.name
        self._hero_class = builder.hero_class
        self._level = builder.level
        self._experience = 0
        self._gold = builder.gold
        self._weapon = builder.weapon
        self._armor = builder.armor
        self._inventory: List[Item] = []
        self._health = self.get_max_health()

    class Builder:
        def __init__(self) -> None:
            self.name: str | None = None
            self.hero_class: HeroClass | None = None
            self.weapon: Weapon | None = None
            self.armor: Armor | None = None
            self.level: int = 1
            self.gold: int = Hero.STARTING_GOLD

        def set_name(self, name: str) -> "Hero.Builder":
            self.name = name
            return self

        def set_hero_class(self, hero_class: HeroClass) -> "Hero.Builder":
            self.hero_class = hero_class
            return self

        def set_starter_kit(self, starter_kit: StarterKitFactory) -> "Hero.Builder":
            self.weapon = starter_kit.create_weapon()
            self.armor = starter_kit.create_armor()
            return self

        def set_level(self, level: int) -> "Hero.Builder":
            self.level = level
            return self

        def set_gold(self, gold: int) -> "Hero.Builder":
            self.gold = gold
            return self

        def build(self) -> "Hero":
            if not self.name or not self.name.strip():
                raise ValueError("У героя должно быть имя")
            if len(self.name) > Hero.MAX_NAME_LENGTH:
                raise ValueError(f"Имя героя не может быть длиннее {Hero.MAX_NAME_LENGTH} символов")
            if self.hero_class is None:
                raise ValueError("Не выбран класс героя")
            if self.weapon is None or self.armor is None:
                raise ValueError("Герою нужны оружие и броня")
            if self.level < 1:
                raise ValueError("Уровень героя не может быть меньше 1")
            if self.gold < 0:
                raise ValueError("Золота не может быть меньше нуля")
            
            return Hero(self)

    def get_code(self) -> str:
        return self._hero_class.get_code()

    def get_name(self) -> str:
        return self._name

    def get_health(self) -> int:
        return self._health

    def get_max_health(self) -> int:
        return self._hero_class.get_base_health() + (self._level - 1) * self.HEALTH_PER_LEVEL

    def is_alive(self) -> bool:
        return self._health > 0

    def roll_damage(self) -> Hit:
        hit = self._weapon.roll_damage()
        return Hit(hit.damage + (self._level - 1) * self.DAMAGE_PER_LEVEL, hit.critical)

    def receive_hit(self, damage: int) -> int:
        reduced_damage = round(damage * (1 - self._armor.get_defense()))
        dealt = max(1, reduced_damage)
        self._health = max(0, self._health - dealt)
        return dealt

    def restore_health(self) -> None:
        self._health = self.get_max_health()

    def gain_experience(self, amount: int) -> int:
        self._experience += amount
        levels_gained = 0
        while self._experience >= self.get_experience_to_next_level():
            self._experience -= self.get_experience_to_next_level()
            self._level += 1
            levels_gained += 1
        return levels_gained

    def add_gold(self, amount: int) -> None:
        self._gold += amount

    def spend_gold(self, amount: int) -> None:
        if amount > self._gold:
            raise ValueError(f"Не хватает золота: нужно {amount}, есть {self._gold}")
        self._gold -= amount

    def add_item(self, item: Item) -> None:
        self._inventory.append(item)

    def remove_item(self, item: Item) -> None:
        if item not in self._inventory:
            raise ValueError(f"В инвентаре нет предмета {item.get_name()}")
        self._inventory.remove(item)

    def equip(self, item: Item) -> None:
        if isinstance(item, Weapon):
            self.remove_item(item)
            self._inventory.append(self._weapon)
            self._weapon = item
        elif isinstance(item, Armor):
            self.remove_item(item)
            self._inventory.append(self._armor)
            self._armor = item
        else:
            raise ValueError(f"Предмет нельзя экипировать: {item.get_name()}")

    def get_hero_class(self) -> HeroClass:
        return self._hero_class

    def get_level(self) -> int:
        return self._level

    def get_experience(self) -> int:
        return self._experience

    def get_experience_to_next_level(self) -> int:
        return self._level * self.EXPERIENCE_PER_LEVEL

    def get_gold(self) -> int:
        return self._gold

    def get_weapon(self) -> Weapon:
        return self._weapon

    def get_armor(self) -> Armor:
        return self._armor

    def get_inventory(self) -> List[Item]:
        return list(self._inventory)