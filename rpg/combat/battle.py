from typing import List
from .combatant import Combatant
from .report import BattleEvent, BattleReport, EventType, Outcome, Participant, Side
from ..tactic.action import Action
from ..tactic.tactic import Tactic

class Battle:
    def __init__(self, hero: Combatant, enemy: Combatant, tactic: Tactic | None = None) -> None:
        self._hero = hero
        self._enemy = enemy
        self._events: List[BattleEvent] = []
        self._round = 0
        from ..tactic.balanced_tactic import BalancedTactic
        self._tactic = tactic if tactic is not None else BalancedTactic()

    def run(self) -> BattleReport:
        while self._hero.is_alive() and self._enemy.is_alive():
            self._round += 1
            
            action = self._tactic.choose_action(self._round, self._hero, self._enemy)
            
            self._strike(self._hero, Side.HERO, self._enemy, Side.ENEMY, action.attack_multiplier)
            if self._enemy.is_alive():
                self._strike(self._enemy, Side.ENEMY, self._hero, Side.HERO, action.incoming_multiplier)

        outcome = Outcome.VICTORY if self._hero.is_alive() else Outcome.DEFEAT
        return BattleReport(
            Participant.of(self._hero),
            Participant.of(self._enemy),
            outcome,
            list(self._events),
        )

    def _strike(self, attacker, source, defender, target, multiplier: float) -> None:
        hit = attacker.roll_damage()
        
        modified_damage = max(1, int(hit.damage * multiplier + 0.5))
        damage = defender.receive_hit(modified_damage)
        dealt = damage.amount

        event_type = EventType.CRITICAL_HIT if hit.critical else EventType.HIT
        self._events.append(BattleEvent(
            self._round, event_type, source, target, dealt, defender.get_health()
        ))
        if not defender.is_alive():
            self._events.append(BattleEvent(
                self._round, EventType.DEATH, source, target, 0, 0
            ))