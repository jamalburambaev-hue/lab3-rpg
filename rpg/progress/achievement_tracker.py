from ..event.game_event import GameEvent
from ..event.game_event_type import GameEventType
from .achievement import Achievement

class AchievementTracker:
    def on_event(self, event: GameEvent) -> None:
        hero = event.hero
        if event.type == GameEventType.VICTORY:
            hero.unlock(Achievement.FIRST_BLOOD)
            if getattr(event.expedition.battle.enemy, 'get_code', lambda: "")() == "dragon":
                hero.unlock(Achievement.DRAGON_SLAYER)
            loot = event.expedition.rewards.loot
            if loot and loot.get_enchantments():
                hero.unlock(Achievement.LUCKY)
        elif event.type == GameEventType.LEVEL_UP and hero.get_level() >= 5:
            hero.unlock(Achievement.VETERAN)