from typing import List

from .combatant import Combatant
from .report import BattleEvent, BattleReport, EventType, Outcome, Participant, Side


class Battle:
    def __init__(self, hero: Combatant, enemy: Combatant) -> None:
        self._hero = hero
        self._enemy = enemy
        self._events: List[BattleEvent] = []
        self._round = 0

    def run(self) -> BattleReport:
        while self._hero.is_alive() and self._enemy.is_alive():
            self._round += 1
            self._strike(self._hero, Side.HERO, self._enemy, Side.ENEMY)
            if self._enemy.is_alive():
                self._strike(self._enemy, Side.ENEMY, self._hero, Side.HERO)

        outcome = Outcome.VICTORY if self._hero.is_alive() else Outcome.DEFEAT
        return BattleReport(
            Participant.of(self._hero),
            Participant.of(self._enemy),
            outcome,
            list(self._events),
        )

    def _strike(self, attacker, source, defender, target) -> None:
        hit = attacker.roll_damage()
        dealt = defender.receive_hit(hit.damage)
        event_type = EventType.CRITICAL_HIT if hit.critical else EventType.HIT
        self._events.append(BattleEvent(
            self._round, event_type, source, target, dealt, defender.get_health()
        ))
        if not defender.is_alive():
            self._events.append(BattleEvent(
                self._round, EventType.DEATH, source, target, 0, 0
            ))