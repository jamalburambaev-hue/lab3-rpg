from ..combat.combatant import Combatant


class Enemy(Combatant):
    def get_experience_reward(self) -> int: ...
    
    def roll_gold_reward(self) -> int: ...