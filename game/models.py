"""Модуль с моделями"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Food:
    """Модель объекта еды"""

    name: str
    satiety: int
    price: int

    def __repr__(self) -> str:
        """Метод для красивого принтинга объекта"""
        return f"{self.name} стоимость: {self.price}, утоляет голод на {self.satiety} единиц"


@dataclass
class Medicine:
    """Модель объекта лекарства"""

    name: str
    price: int
    heal_hp: int
    number_of_uses: int
    uses: int = 0

    def is_empty(self) -> bool:
        """
        Проверяет, закончились ли использования лекарства

        :return: True, если закончилось, иначе False
        """
        return self.uses >= self.number_of_uses

    def __repr__(self) -> str:
        """Метод для красивого принтинга объекта"""
        return (
            f"{self.name} стоимость: {self.price}, лечит на {self.heal_hp} HP, "
            f"использований: {self.number_of_uses - self.uses}/{self.number_of_uses}"
        )
