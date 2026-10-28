from abc import ABC, abstractmethod
from typing import List

from ..combat.battle import Battle
from ..combat.report import Outcome
from ..core.dice import Dice
from ..enemy.enemy import Enemy
from ..hero.hero import Hero
from ..item.catalog import ItemCatalog
from ..item.item import Item
from .expedition_report import ExpeditionReport
from .rewards import Rewards


class Location(ABC):
    LOOT_CHANCE = 0.6
    ENCHANT_CHANCE = 0.3

    def __init__(self, code: str, display_name: str, recommended_level: int, catalog: ItemCatalog) -> None:
        self._code = code
        self._display_name = display_name
        self._recommended_level = recommended_level
        self._catalog = catalog

    @abstractmethod
    def _create_enemy(self) -> Enemy: ...

    @abstractmethod
    def _get_loot_table(self) -> List[str]: ...

    def explore(self, hero: Hero) -> ExpeditionReport:
        return self.explore_with_seed(hero, Dice().next_seed())

    def explore_with_seed(self, hero: Hero, seed: int) -> ExpeditionReport:
        dice = Dice()
        dice.reseed(seed)

        hero.restore_health()
        enemy = self._create_enemy()
        battle = Battle(hero, enemy).run()

        if battle.outcome == Outcome.VICTORY:
            rewards = self._reward(hero, enemy, dice)
        else:
            rewards = self._punish(hero)

        return ExpeditionReport(seed, self._code, battle, rewards)

    def _reward(self, hero: Hero, enemy: Enemy, dice: Dice) -> Rewards:
        experience = enemy.get_experience_reward()
        gold = enemy.roll_gold_reward()
        loot = self._roll_loot(dice)

        levels_gained = hero.gain_experience(experience)
        hero.add_gold(gold)
        if loot:
            hero.add_item(loot)

        return Rewards(experience, gold, loot, levels_gained)

    def _roll_loot(self, dice: Dice) -> Item | None:
        if not dice.chance(self.LOOT_CHANCE):
            return None

        loot = self._catalog.create(dice.pick(self._get_loot_table()))
        if dice.chance(self.ENCHANT_CHANCE):
            loot.enchant(dice.pick(loot.get_possible_enchantments()))
        return loot

    def _punish(self, hero: Hero) -> Rewards:
        lost_gold = hero.get_gold() // 2
        hero.spend_gold(lost_gold)
        return Rewards(0, -lost_gold, None, 0)

    def get_code(self) -> str:
        return self._code

    def get_display_name(self) -> str:
        return self._display_name

    def get_recommended_level(self) -> int:
        return self._recommended_level