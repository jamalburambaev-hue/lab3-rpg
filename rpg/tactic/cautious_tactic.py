from .tactic import Tactic
from .action import Action
from ..combat.combatant import Combatant

class CautiousTactic(Tactic):
    def get_code(self) -> str: return "cautious"
    def get_display_name(self) -> str: return "Осторожность"
    def get_description(self) -> str: return "при здоровье ниже 40% уходить в оборону"

    def choose_action(self, round_num: int, hero: Combatant, enemy: Combatant) -> Action:
        wounded = hero.get_health() < hero.get_max_health() * 0.4
        return Action.DEFEND if wounded and round_num % 2 == 0 else Action.ATTACK