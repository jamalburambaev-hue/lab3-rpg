from .damage import Damage
from .damage_handler import DamageHandler

class ArmorHandler(DamageHandler):
    def __init__(self, defense: float):
        super().__init__()
        self._defense = defense

    def handle(self, damage: Damage) -> None:
        damage.reduce_to(max(1, int(damage.amount * (1 - self._defense) + 0.5)))
        self._pass_to_next(damage)