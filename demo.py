from rpg.combat.battle import Battle
from rpg.core.dice import Dice
from rpg.enemy.goblin import Goblin
from rpg.hero.hero import Hero
from rpg.hero.hero_class import HeroClass
from rpg.item.default_catalog import IRON_SWORD, create_default_catalog
from rpg.item.enchantment import FIERY
from rpg.view import ConsoleView

def main():
    catalog = create_default_catalog()
    view = ConsoleView()

    print("===== Одиночка (Singleton) =====")
    print("Dice() возвращает один и тот же объект:", Dice() is Dice())

    print("\n===== Прототип (Prototype) =====")
    plain = catalog.create(IRON_SWORD)
    fiery = catalog.create(IRON_SWORD)
    fiery.enchant(FIERY)
    print("Первая копия:        ", view.describe_item(plain))
    print("Вторая копия:        ", view.describe_item(fiery))
    print("Новая копия шаблона: ", view.describe_item(catalog.create(IRON_SWORD)))
    print("Копии - разные объекты:", plain is not fiery)

    print("\n===== Абстрактная фабрика (Abstract Factory) =====")
    for hc in HeroClass:
        kit = hc.get_starter_kit(catalog)
        print(f"{hc.get_display_name()}: {view.describe_item(kit.create_weapon())}, {view.describe_item(kit.create_armor())}")

    print("\n===== Строитель (Builder) =====")
    try:
        Hero.Builder().set_hero_class(HeroClass.MAGE).build()
    except ValueError as e:
        print("Герой без имени не создается:", e)

    hero = (
        Hero.Builder()
        .set_name("Артур")
        .set_hero_class(HeroClass.WARRIOR)
        .set_starter_kit(HeroClass.WARRIOR.get_starter_kit(catalog))
        .set_level(3)
        .build()
    )
    print("Создан герой через Билдер:")
    view.print_hero(hero)

    print("\n===== Фабричный метод (Factory Method) =====")
    print("Локация 'Лес' создает Гоблина:")
    battle_report = Battle(hero, Goblin()).run()
    print(f"Исход боя с {battle_report.enemy.name}: {battle_report.outcome.name}")

if __name__ == "__main__":
    main()