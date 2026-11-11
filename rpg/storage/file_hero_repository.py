import json
from pathlib import Path
from typing import List, Optional
from ..hero.hero import Hero
from ..hero.hero_class import HeroClass
from ..item.catalog import ItemCatalog
from ..item.enchantment import by_code
from ..progress.achievement import Achievement
from .hero_repository import HeroRepository

class FileHeroRepository:
    def __init__(self, file: Path, catalog: ItemCatalog) -> None:
        self._file = file
        self._catalog = catalog

    def find_by_name(self, name: str) -> Optional[Hero]:
        for hero in self.find_all():
            if hero.get_name() == name:
                return hero
        return None

    def find_all(self) -> List[Hero]:
        if not self._file.exists():
            return []
        text = self._file.read_text(encoding="utf-8")
        if not text.strip():
            return []
        saves = json.loads(text)
        return [self._restore(save) for save in saves]

    def save(self, hero: Hero) -> None:
        saves = [self._snapshot(h) for h in self.find_all() if h.get_name() != hero.get_name()]
        saves.append(self._snapshot(hero))
        self._file.parent.mkdir(parents=True, exist_ok=True)
        self._file.write_text(json.dumps(saves, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def _snapshot(self, hero: Hero) -> dict:
        return {
            "name": hero.get_name(),
            "heroClass": hero.get_hero_class().get_code(),
            "level": hero.get_level(),
            "experience": hero.get_experience(),
            "gold": hero.get_gold(),
            "weapon": self._snapshot_item(hero.get_weapon()),
            "armor": self._snapshot_item(hero.get_armor()),
            "inventory": [self._snapshot_item(item) for item in hero.get_inventory()],
            "achievements": [a.code for a in hero.get_achievements()],
        }

    def _snapshot_item(self, item) -> dict:
        return {
            "code": item.get_code(),
            "enchantments": [e.code for e in item.get_enchantments()]
        }

    def _restore_item(self, save: dict):
        item = self._catalog.create(save["code"])
        for code in save["enchantments"]:
            item.enchant(by_code(code))
        return item

    def _restore(self, save: dict) -> Hero:
        hero = (
            Hero.Builder()
            .set_name(save["name"])
            .set_hero_class(HeroClass.by_code(save["heroClass"]))
            .set_level(save["level"])
            .set_gold(save["gold"])
            .set_weapon(self._restore_item(save["weapon"]))
            .set_armor(self._restore_item(save["armor"]))
            .build()
        )
        return hero