from dataclasses import dataclass

@dataclass
class Damage:
    amount: int
    evaded: bool = False
    absorbed: int = 0

    def reduce_to(self, amount: int) -> None:
        self.amount = amount

    def evade(self) -> None:
        self.amount = 0
        self.evaded = True

    def absorb(self, value: int) -> None:
        self.amount -= value
        self.absorbed += value