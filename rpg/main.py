from typing import List

from .camp.merchant import Merchant
from .combat.report import Outcome
from .hero.hero import Hero
from .hero.hero_class import HeroClass
from .item.default_catalog import (
    CHAINMAIL, ELVEN_BOW, EMBER_STAFF, IRON_SWORD, PLATE_ARMOR, create_default_catalog
)
from .view import ConsoleView
from .world.crypt import Crypt
from .world.dragon_lair import DragonLair
from .world.forest import Forest
from .world.registry import LocationRegistry


class Game:
    def __init__(self) -> None:
        self._catalog = create_default_catalog()
        self._locations = LocationRegistry([
            Forest(self._catalog),
            Crypt(self._catalog),
            DragonLair(self._catalog),
        ])
        self._merchant = Merchant(self._catalog, [
            IRON_SWORD, ELVEN_BOW, EMBER_STAFF, CHAINMAIL, PLATE_ARMOR
        ])
        self._view = ConsoleView()

    def run(self) -> None:
        hero = self._create_hero()
        print(f"{hero.get_name()} разбивает лагерь на опушке мистического леса.")

        while True:
            print()
            self._view.print_hero(hero)
            print("1 - отправиться в экспедицию, 2 - снаряжение, 3 - торговец, 0 - выйти из игры")
            choice = input().strip()

            if choice == "1":
                self._go_on_expedition(hero)
            elif choice == "2":
                self._manage_equipment(hero)
            elif choice == "3":
                self._visit_merchant(hero)
            elif choice == "0":
                print("До встречи!")
                break
            else:
                print("Такого варианта нет")

    def _create_hero(self) -> Hero:
        print("Создайте своего героя!")
        while True:
            print("Выберите класс:")
            classes = list(HeroClass)
            for i, hc in enumerate(classes):
                kit = hc.get_starter_kit(self._catalog)
                w = kit.create_weapon()
                a = kit.create_armor()
                print(f"{i + 1} - {hc.get_display_name()} (здоровье {hc.get_base_health()}): "
                      f"{self._view.describe_item(w)}, {self._view.describe_item(a)}")

            try:
                idx = int(input().strip()) - 1
                if idx < 0 or idx >= len(classes):
                    raise ValueError
                hero_class = classes[idx]
            except ValueError:
                print("Неверный выбор.")
                continue

            print("Введите имя:")
            name = input().strip()

            try:
                return (
                    Hero.Builder()
                    .set_name(name)
                    .set_hero_class(hero_class)
                    .set_starter_kit(hero_class.get_starter_kit(self._catalog))
                    .build()
                )
            except ValueError as e:
                print(f"Не получилось создать героя: {e}")

    def _go_on_expedition(self, hero: Hero) -> None:
        all_locs = self._locations.get_all()
        print("Куда отправимся?")
        for i, loc in enumerate(all_locs):
            print(f"{i + 1} - {loc.get_display_name()} (рекомендуемый уровень {loc.get_recommended_level()})")

        try:
            idx = int(input().strip()) - 1
            if idx < 0 or idx >= len(all_locs):
                raise ValueError
        except ValueError:
            return

        loc = all_locs[idx]
        report = loc.explore(hero)
        print()
        self._view.print_report(report, loc.get_display_name())

        if report.battle.outcome == Outcome.VICTORY and loc.get_code() == DragonLair.CODE:
            print(f"\nДракон повержен! Барды еще долго будут петь о подвиге героя по имени {hero.get_name()}.")

    def _manage_equipment(self, hero: Hero) -> None:
        inventory = hero.get_inventory()
        if not inventory:
            print("Инвентарь пуст")
            return

        print("Что экипировать? (0 - назад)")
        for i, item in enumerate(inventory):
            print(f"{i + 1} - {self._view.describe_item(item)}")

        try:
            idx = int(input().strip()) - 1
            if idx < 0 or idx >= len(inventory):
                return
        except ValueError:
            return

        item = inventory[idx]
        hero.equip(item)
        print(f"Экипировано: {self._view.describe_item(item)}")

    def _visit_merchant(self, hero: Hero) -> None:
        print(f'Торговец: "Чего желаешь?" (золото: {hero.get_gold()})')
        print("1 - купить, 2 - продать, 0 - назад")
        choice = input().strip()

        if choice == "1":
            self._buy(hero)
        elif choice == "2":
            self._sell(hero)

    def _buy(self, hero: Hero) -> None:
        showcase = self._merchant.get_showcase()
        for i, item in enumerate(showcase):
            print(f"{i + 1} - {self._view.describe_item(item)}: {item.get_price()} золота")

        try:
            idx = int(input().strip()) - 1
            if idx < 0 or idx >= len(showcase):
                return
        except ValueError:
            return

        try:
            item = self._merchant.buy(hero, showcase[idx].get_code())
            print(f"Куплено: {self._view.describe_item(item)}")
        except ValueError as e:
            print(e)

    def _sell(self, hero: Hero) -> None:
        inventory = hero.get_inventory()
        if not inventory:
            print("Продавать нечего (экипированные предметы продать нельзя)")
            return

        for i, item in enumerate(inventory):
            print(f"{i + 1} - {self._view.describe_item(item)}: {self._merchant.get_sell_price(item)} золота")

        try:
            idx = int(input().strip()) - 1
            if idx < 0 or idx >= len(inventory):
                return
        except ValueError:
            return

        item = inventory[idx]
        price = self._merchant.sell(hero, item)
        print(f"Продано: {item.get_name()} за {price} золота")