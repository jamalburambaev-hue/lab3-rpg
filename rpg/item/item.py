from abc import ABC, abstractmethod
from typing import List

from .enchantment import Enchantment


class Item(ABC):
    """Базовый класс предмета. Каждый предмет умеет создавать свою копию."""

    def __init__(self, code: str, name: str, base_price: int) -> None:
        self._code = code
        self._name = name
        self._base_price = base_price
        self._enchantments: List[Enchantment] = []

    @abstractmethod
    def copy(self) -> "Item":
        """Возвращает независимую копию предмета."""

    @abstractmethod
    def get_possible_enchantments(self) -> List[Enchantment]:
        """Какие зачарования подходят этому виду предмета."""

    @abstractmethod
    def get_description(self) -> str:
        """Описание характеристик, например 'урон 12'."""

    def enchant(self, enchantment: Enchantment) -> None:
        if enchantment not in self.get_possible_enchantments():
            raise ValueError(
                f"Зачарование '{enchantment.name}' не подходит "
                f"для предмета '{self._name}'"
            )
        self._enchantments.append(enchantment)

    def get_code(self) -> str:
        return self._code

    def get_name(self) -> str:
        return self._name

    def get_price(self) -> int:
        return self._base_price + sum(e.bonus_price for e in self._enchantments)

    def get_enchantments(self) -> List[Enchantment]:
        return list(self._enchantments)

    def _copy_common_into(self, target: "Item") -> None:
        target._code = self._code
        target._name = self._name
        target._base_price = self._base_price
        target._enchantments = list(self._enchantments)