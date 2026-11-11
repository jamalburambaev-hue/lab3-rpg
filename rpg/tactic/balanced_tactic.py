from .tactic import Tactic
from .action import Action
from ..combat.combatant import Combatant

class BalancedTactic(Tactic):
    def get_code(self) -> str: return "balanced"
    def get_display_name(self) -> str: return "Баланс"
    def get_description(self) -> str: return "обычный удар каждый раунд"

    def choose_action(self, round_num: int, hero: Combatant, enemy: Combatant) -> Action:
        return Action.ATTACK