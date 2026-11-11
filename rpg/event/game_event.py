from dataclasses import dataclass
from .game_event_type import GameEventType

@dataclass(frozen=True)
class GameEvent:
    type: GameEventType
    hero: any          # Твой класс Hero
    expedition: any    # Твой класс ExpeditionReport