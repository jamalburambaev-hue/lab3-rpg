from .combat.report import BattleReport, EventType, Outcome, Participant, Side
from .hero.hero import Hero
from .item.item import Item
from .world.expedition_report import ExpeditionReport


class ConsoleView:
    def describe_item(self, item: Item) -> str:
        desc = item.get_name()
        if item.get_enchantments():
            names = ", ".join(e.name for e in item.get_enchantments())
            desc += f" [{names}]"
        return f"{desc} ({item.get_description()})"

    def print_hero(self, hero: Hero) -> None:
        print(f"{hero.get_name()}, {hero.get_hero_class().get_display_name()} {hero.get_level()} ур. | "
              f"здоровье {hero.get_max_health()} | опыт {hero.get_experience()}/{hero.get_experience_to_next_level()} | "
              f"золото {hero.get_gold()}")
        print(f"  Оружие: {self.describe_item(hero.get_weapon())}")
        print(f"  Броня:  {self.describe_item(hero.get_armor())}")

    def print_report(self, report: ExpeditionReport, location_name: str) -> None:
        battle = report.battle
        print(f"=== {location_name} (сид {report.seed}) ===")
        print(f"{battle.hero.name} встречает врага: {battle.enemy.name} ({battle.enemy.max_health} здоровья)")

        for event in battle.events:
            source = battle.hero if event.source == Side.HERO else battle.enemy
            target = battle.hero if event.target == Side.HERO else battle.enemy

            if event.type == EventType.HIT:
                print(f"[раунд {event.round}] {source.name} -> {target.name}: {event.amount} урона, "
                      f"осталось {event.target_health_after}/{target.max_health}")
            elif event.type == EventType.CRITICAL_HIT:
                print(f"[раунд {event.round}] {source.name} -> {target.name}: КРИТ! {event.amount} урона, "
                      f"осталось {event.target_health_after}/{target.max_health}")
            elif event.type == EventType.DEATH:
                print(f"{target.name} повержен!")

        self._print_rewards(battle, report)

    def _print_rewards(self, battle: BattleReport, report: ExpeditionReport) -> None:
        rewards = report.rewards
        if battle.outcome == Outcome.DEFEAT:
            print(f"Поражение... {battle.hero.name} едва уносит ноги и теряет {-rewards.gold} золота")
            return

        print(f"Победа! +{rewards.experience} опыта, +{rewards.gold} золота")
        if rewards.loot:
            print(f"Добыча: {self.describe_item(rewards.loot)}")
        if rewards.levels_gained > 0:
            print("Новый уровень!")