"""Модуль с интерфейсом и реализацией кликера."""

from abc import ABC, abstractmethod
from random import randint


class AbstractClicker(ABC):
    """Интерфейс для кликера."""

    @abstractmethod
    def click(self) -> None:
        """Абстрактный метод клика для получения монет."""
        raise NotImplementedError

    @property
    @abstractmethod
    def income_per_click(self) -> int:
        """Вернуть количество монет за один клик."""
        raise NotImplementedError


class SimpleRandomClicker(AbstractClicker):
    """Кликер, выдающий случайный доход в заданном диапазоне."""

    def __init__(self, min_income: int, max_income: int) -> None:
        """
        Инициализировать кликер со случайным доходом.

        :param min_income: Минимальное количество монет за клик.
        :param max_income: Максимальное количество монет за клик.
        :raises ValueError: Если минимальный доход больше максимального.
        """
        if min_income > max_income:
            raise ValueError("Минимальный доход не может быть больше максимального")

        self._min_income = min_income
        self._max_income = max_income
        self._income_per_click = 0

    @property
    def income_per_click(self) -> int:
        """Вернуть доход, полученный за последний клик."""
        return self._income_per_click

    def click(self) -> None:
        """Сгенерировать доход за один клик."""
        self._income_per_click = randint(
            self._min_income,
            self._max_income,
        )
