from .tactic import Tactic
from .action import Action
from ..combat.combatant import Combatant

class AggressiveTactic(Tactic):
    def get_code(self) -> str: return "aggressive"
    def get_display_name(self) -> str: return "Натиск"
    def get_description(self) -> str: return "безрассудные удары, пока у врага больше здоровья"

    def choose_action(self, round_num: int, hero: Combatant, enemy: Combatant) -> Action:
        return Action.POWER_STRIKE if enemy.get_health() > hero.get_health() else Action.ATTACK