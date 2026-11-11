from pathlib import Path
from typing import List

from ..camp.merchant import Merchant
from ..combat.report import Outcome
from ..event.game_event import GameEvent
from ..event.game_event_publisher import GameEventPublisher
from ..event.game_event_type import GameEventType
from ..hero.hero import Hero
from ..hero.hero_class import HeroClass
from ..item.default_catalog import (
    IRON_SWORD, ELVEN_BOW, EMBER_STAFF, CHAINMAIL, PLATE_ARMOR, create_default_catalog
)
from ..item.item import Item
from ..progress.achievement_tracker import AchievementTracker
from ..progress.expedition_journal import ExpeditionJournal
from ..storage.caching_hero_repository import CachingHeroRepository
from ..storage.file_hero_repository import FileHeroRepository
from ..tactic.balanced_tactic import BalancedTactic
from ..tactic.aggressive_tactic import AggressiveTactic
from ..tactic.cautious_tactic import CautiousTactic
from ..tactic.tactic import Tactic
from ..world.crypt import Crypt
from ..world.dragon_lair import DragonLair
from ..world.forest import Forest
from ..world.haunted_manor import HauntedManor
from ..world.registry import LocationRegistry
from ..world.expedition_report import ExpeditionReport


class GameFacade:
    def __init__(self, save_file: Path) -> None:
        self._catalog = create_default_catalog()
        self._locations = LocationRegistry([
            Forest(self._catalog),
            HauntedManor(self._catalog),
            Crypt(self._catalog),
            DragonLair(self._catalog),
        ])
        
        self._merchant = Merchant(self._catalog, [
            IRON_SWORD, ELVEN_BOW, EMBER_STAFF, CHAINMAIL, PLATE_ARMOR
        ])
        self.tactics = [BalancedTactic(), AggressiveTactic(), CautiousTactic()]

        self._heroes = CachingHeroRepository(FileHeroRepository(save_file, self._catalog))

        self._events = GameEventPublisher()
        self._journal = ExpeditionJournal()
        tracker = AchievementTracker()
        self._events.subscribe(GameEventType.VICTORY, tracker)
        self._events.subscribe(GameEventType.LEVEL_UP, tracker)
        self._events.subscribe(GameEventType.VICTORY, self._journal)
        self._events.subscribe(GameEventType.DEFEAT, self._journal)

    @property
    def hero_classes(self) -> List[HeroClass]:
        return list(HeroClass)

    def get_saved_heroes(self) -> List[Hero]:
        return self._heroes.find_all()

    def get_hero(self, name: str) -> Hero:
        hero = self._heroes.find_by_name(name)
        if not hero:
            raise ValueError("Герой не найден")
        return hero

    def create_hero(self, name: str, hero_class: HeroClass) -> Hero:
        hero = (
            Hero.Builder()
            .set_name(name)
            .set_hero_class(hero_class)
            .set_starter_kit(hero_class.get_starter_kit(self._catalog))
            .build()
        )
        self._heroes.save(hero)
        return hero

    def get_locations(self) -> List:
        return self._locations.get_all()

    def explore(self, hero: Hero, location, tactic: Tactic) -> ExpeditionReport:
        report = location.explore(hero, tactic)
        
        result_type = GameEventType.VICTORY if report.battle.outcome == Outcome.VICTORY else GameEventType.DEFEAT
        self._events.publish(GameEvent(result_type, hero, report))
        if report.rewards.levels_gained > 0:
            self._events.publish(GameEvent(GameEventType.LEVEL_UP, hero, report))
            
        self._heroes.save(hero)
        return report

    def get_journal(self, hero_name: str):
        return self._journal.get_entries(hero_name)

    def get_showcase(self) -> List[Item]:
        return self._merchant.get_showcase()

    def get_sell_price(self, item: Item) -> int:
        return self._merchant.get_sell_price(item)

    def buy(self, hero: Hero, item_code: str) -> Item:
        item = self._merchant.buy(hero, item_code)
        self._heroes.save(hero)
        return item

    def sell(self, hero: Hero, item: Item) -> int:
        price = self._merchant.sell(hero, item)
        self._heroes.save(hero)
        return price

    def equip(self, hero: Hero, item: Item) -> None:
        hero.equip(item)
        self._heroes.save(hero)