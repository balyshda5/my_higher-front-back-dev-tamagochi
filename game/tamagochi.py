"""Модуль с интерфейсом и реализациями класса тамагочи"""

from abc import ABC, abstractmethod

from .models import Food, Medicine
from .exceptions import TamagochiIsGone


class AbstractTamagochi(ABC):
    """Интерфейс логики тамагочи"""

    @abstractmethod
    def feed(self, food: Food) -> None:
        """
        Абстрактный метод для кормления тамагочи

        :param food: объект еды для кормления
        """
        raise NotImplementedError

    @abstractmethod
    def play(self) -> None:
        """Абстрактный метод для игры с тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def rest(self) -> None:
        """Абстрактный метод для отдыха тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def heal(self, medicine: Medicine) -> None:
        """
        Абстрактный метод для лечения тамагочи

        :param medicine: лекарство для лечения
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def status(self) -> dict[str, int]:
        """
        Абстрактное свойство для доступа ко всем состояниям тамагочи

        :return: словарь со всеми состояниями тамагочи
        """
        raise NotImplementedError

    @abstractmethod
    def is_alive(self) -> bool:
        """
        Абстрактный метод для проверки жив ли тамагочи

        :return: True если жив, иначе False
        """
        raise NotImplementedError

    @abstractmethod
    def is_sick(self) -> bool:
        """
        Абстрактный метод для проверки, не заболел ли тамагочи

        :return: True если тамагочи болеет, иначе False
        """
        raise NotImplementedError

    @abstractmethod
    def update(self) -> None:
        """
        Абстрактный метод для обновления состояний тамагочи.
        Должен использоваться после каждого взаимодействия с тамагочи
        """
        raise NotImplementedError


class SimpleTamagochi(AbstractTamagochi):
    """Простая реализация питомца для игры."""

    MAX_VALUE = 100
    SICK_HUNGER = 80
    SICK_FATIGUE = 75

    def __init__(self) -> None:
        """Создать питомца с начальными показателями"""
        self._hunger = 20
        self._hp = 100
        self._energy = 100
        self._fatigue = 0
        self._sick = False

    @property
    def status(self) -> dict[str, int]:
        """
        Вернуть текущие показатели питомца.
        Returns:
            словарь с голодом, здоровьем, энергией и усталостью.
        """
        return {
            "hunger": self._hunger,
            "hp": self._hp,
            "energy": self._energy,
            "fatigue": self._fatigue,
        }

    def is_alive(self) -> bool:
        """Проверить, жив ли питомец.

        Returns:
            True, если здоровье больше нуля, иначе False.
        """
        return self._hp > 0

    def is_sick(self) -> bool:
        """
        Проверить, болеет ли питомец.

        Returns:
            True, если питомец болеет, иначе False.
        """
        return self._sick

    def feed(self, food: Food) -> None:
        """
        Покормить питомца.
        Args:
            food: Объект еды для кормления.
            
        Raises:
            TamagochiIsGone: Если питомец умер.
        """
        if not self.is_alive():
            raise TamagochiIsGone("Питомец умер, его нельзя покормить.")

        self._hunger = max(0, self._hunger -food.satiety)
        self._energy = min(self.MAX_VALUE, self._energy + 5)

    def play(self) -> None:
        """
        Поиграть с питомцем.
            Raises:
                TamagochiIsGone: Если питомец умер.
        """
        if not self.is_alive():
            raise TamagochiIsGone("Питомец умер, с ним нельзя играть.")

        self._energy = max(0, self._energy -10)
        self._hunger = min(self.MAX_VALUE, self._hunger + 10)
        self._fatigue = min(self.MAX_VALUE, self._fatigue + 10)

    def rest(self) -> None:
        """
        Дать питомцу отдохнуть.

        Raises:
            TamagochiIsGone: Если питомец умер.
        """
        if not self.is_alive():
            raise TamagochiIsGone("Питомец умер, он не может отдыхать")

        rest_power = 20 if self.is_sick() else 40
        self._energy = min(self.MAX_VALUE, self._energy + rest_power)
        self._fatigue = max(0, self._fatigue - rest_power)
        self._hunger = min(self.MAX_VALUE, self._hunger + 5)

    def heal(self, medicine: Medicine) -> None:
        """
        Вылечить питомца лекарством.

        Args:
            medicine: Лекарство для лечения.

        Raises:
            TamagochiIsGone: Если питомец умер.
            ValueError: Если у лекарства закончились применения.
        """
        if not self.is_alive():
            raise TamagochiIsGone("Питомец умер, его нельзя лечить")

        if medicine.is_empty():
            raise ValueError("У лекарства закончились применения")

        medicine.uses += 1
        self._hp = min(self.MAX_VALUE, self._hp + medicine.heal_hp)
        self._sick = False

    def update(self) -> None:
        """Обновить состояние питомца на один игровой тик."""
        self._hunger = min(self.MAX_VALUE, self._hunger + 5)
        self._energy = max(0, self._energy - 5)
        self._fatigue = min(self.MAX_VALUE, self._fatigue + 5)

        if (
            self._hunger >= self.SICK_HUNGER
            or self._fatigue >= self.SICK_FATIGUE
        ):
            self._sick = True

        if self._sick:
            self._hp = max(0, self._hp - 5)
            self._fatigue = min(self.MAX_VALUE, self._fatigue + 5)

        if self._hunger >= 90:
            self._hp = max(0, self._hp - 10)

        if self._energy <= 10:
            self._hp = max(0, self._hp - 10)
