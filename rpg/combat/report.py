from dataclasses import dataclass
from enum import Enum
from typing import List

from .combatant import Combatant


class Side(Enum):
    HERO = "hero"
    ENEMY = "enemy"


class EventType(Enum):
    HIT = "hit"
    CRITICAL_HIT = "critical_hit"
    DEATH = "death"


class Outcome(Enum):
    VICTORY = "victory"
    DEFEAT = "defeat"


@dataclass(frozen=True)
class BattleEvent:
    round: int
    type: EventType
    source: Side
    target: Side
    amount: int
    target_health_after: int


@dataclass(frozen=True)
class Participant:
    code: str
    name: str
    max_health: int

    @classmethod
    def of(cls, combatant: Combatant) -> "Participant":
        return cls(combatant.get_code(), combatant.get_name(), combatant.get_max_health())


@dataclass(frozen=True)
class BattleReport:
    hero: Participant
    enemy: Participant
    outcome: Outcome
    events: List[BattleEvent]