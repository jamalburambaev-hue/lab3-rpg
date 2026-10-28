from dataclasses import dataclass


@dataclass(frozen=True)
class Hit:
    damage: int
    critical: bool = False