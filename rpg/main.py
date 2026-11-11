from pathlib import Path
from .game.game_facade import GameFacade
from .view import ConsoleView
from .hero.hero import Hero

VIEW = ConsoleView()

def main() -> None:
    save_file = Path("saves") / "heroes.json"
    game = GameFacade(save_file)
    
    hero = choose_or_create_hero(game)
    print(f"{hero.get_name()} разбивает лагерь на опушке мистического леса.")

    while True:
        print()
        VIEW.print_hero(hero)
        print("1 - отправиться в экспедицию, 2 - снаряжение, 3 - торговец, 4 - журнал, 0 - выйти из игры")
        choice = input().strip()

        if choice == "1":
            go_on_expedition(game, hero)
        elif choice == "2":
            manage_equipment(game, hero)
        elif choice == "3":
            visit_merchant(game, hero)
        elif choice == "4":
            print_journal(game, hero)
        elif choice == "0":
            break
        else:
            print("Такого варианта нет")

def choose_or_create_hero(game: GameFacade) -> Hero:
    saved = game.get_saved_heroes()
    if saved:
        print("Выберите героя (0 - создать нового):")
        for i, h in enumerate(saved):
            print(f"{i + 1} - {h.get_name()}, {h.get_hero_class().get_display_name()} {h.get_level()} ур.")
        try:
            idx = int(input().strip()) - 1
            if 0 <= idx < len(saved):
                return saved[idx]
        except ValueError:
            pass
    return create_hero(game)

def create_hero(game: GameFacade) -> Hero:
    print("Создайте своего героя!")
    while True:
        print("Выберите класс:")
        classes = game.hero_classes
        for i, hc in enumerate(classes):
            kit = hc.get_starter_kit(game._catalog)
            w, a = kit.create_weapon(), kit.create_armor()
            print(f"{i + 1} - {hc.get_display_name()} (здоровье {hc.get_base_health()}): "
                  f"{VIEW.describe_item(w)}, {VIEW.describe_item(a)}")
        try:
            idx = int(input().strip()) - 1
            if idx < 0 or idx >= len(classes): raise ValueError
            hero_class = classes[idx]
        except ValueError:
            print("Неверный выбор.")
            continue

        print("Введите имя:")
        name = input().strip()
        try:
            return game.create_hero(name, hero_class)
        except ValueError as e:
            print(f"Ошибка: {e}")

def go_on_expedition(game: GameFacade, hero: Hero) -> None:
    locs = game.get_locations()
    print("Куда отправимся?")
    for i, loc in enumerate(locs):
        print(f"{i + 1} - {loc.get_display_name()} (рекомендуемый уровень {loc.get_recommended_level()})")
    try:
        idx = int(input().strip()) - 1
        if idx < 0 or idx >= len(locs): raise ValueError
    except ValueError:
        return

    loc = locs[idx]
    
    print("Выберите тактику:")
    for i, t in enumerate(game.tactics):
        print(f"{i + 1} - {t.get_display_name()}: {t.get_description()}")
    try:
        t_idx = int(input().strip()) - 1
        if t_idx < 0 or t_idx >= len(game.tactics): raise ValueError
    except ValueError:
        return
        
    tactic = game.tactics[t_idx]

    report = game.explore(hero, loc, tactic)
    print()
    VIEW.print_report(report, loc.get_display_name())

def manage_equipment(game: GameFacade, hero: Hero) -> None:
    inv = hero.get_inventory()
    if not inv:
        print("Инвентарь пуст")
        return
    print("Что экипировать? (0 - назад)")
    for i, item in enumerate(inv):
        print(f"{i + 1} - {VIEW.describe_item(item)}")
    try:
        idx = int(input().strip()) - 1
        if idx < 0 or idx >= len(inv): return
    except ValueError:
        return
    
    item = inv[idx]
    game.equip(hero, item)
    print(f"Экипировано: {VIEW.describe_item(item)}")

def visit_merchant(game: GameFacade, hero: Hero) -> None:
    print(f'Торговец: "Чего желаешь?" (золото: {hero.get_gold()})')
    print("1 - купить, 2 - продать, 0 - назад")
    choice = input().strip()
    if choice == "1":
        showcase = game.get_showcase()
        for i, item in enumerate(showcase):
            print(f"{i + 1} - {VIEW.describe_item(item)}: {item.get_price()} золота")
        try:
            idx = int(input().strip()) - 1
            if idx < 0 or idx >= len(showcase): return
            item = game.buy(hero, showcase[idx].get_code())
            print(f"Куплено: {VIEW.describe_item(item)}")
        except (ValueError, IndexError) as e:
            print(e)
    elif choice == "2":
        inv = hero.get_inventory()
        if not inv:
            print("Нечего продавать.")
            return
        for i, item in enumerate(inv):
            print(f"{i + 1} - {VIEW.describe_item(item)}: {game.get_sell_price(item)} золота")
        try:
            idx = int(input().strip()) - 1
            if idx < 0 or idx >= len(inv): return
            price = game.sell(hero, inv[idx])
            print(f"Продано за {price} золота")
        except (ValueError, IndexError) as e:
            print(e)

def print_journal(game: GameFacade, hero: Hero) -> None:
    entries = game.get_journal(hero.get_name())
    if not entries:
        print("Журнал пуст.")
        return
    for i, entry in enumerate(entries):
        res = "Победа" if entry.battle.outcome.name == "VICTORY" else "Поражение"
        print(f"{i + 1}. {entry.location_code} — {res}")

if __name__ == "__main__":
    main()