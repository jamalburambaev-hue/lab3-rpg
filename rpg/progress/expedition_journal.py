from typing import Dict, List
from ..event.game_event import GameEvent

class ExpeditionJournal:
    def __init__(self):
        self._entries: Dict[str, List] = {}

    def on_event(self, event: GameEvent) -> None:
        self._entries.setdefault(event.hero.get_name(), []).append(event.expedition)

    def get_entries(self, hero_name: str) -> List:
        return self._entries.get(hero_name, [])