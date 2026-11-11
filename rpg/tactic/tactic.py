from abc import ABC, abstractmethod
from ..combat.combatant import Combatant
from .action import Action

class Tactic(ABC):
    @abstractmethod
    def get_code(self) -> str: ...

    @abstractmethod
    def get_display_name(self) -> str: ...

    @abstractmethod
    def get_description(self) -> str: ...

    @abstractmethod
    def choose_action(self, round_num: int, hero: Combatant, enemy: Combatant) -> Action: ...