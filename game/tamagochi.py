"""Модуль с интерфейсом и реализациями класса тамагочи"""

from abc import ABC, abstractmethod

from .exceptions import TamagochiIsGone
from .models import Food, Medicine


class AbstractTamagochi(ABC):
    """Интерфейс логики тамагочи"""

    @abstractmethod
    def feed(self, food: Food) -> None:
        """Покормить тамагочи."""
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
        """Лечение тамагочи."""
        raise NotImplementedError

    @property
    @abstractmethod
    def status(self) -> dict[str, int]:
        """Доступ к состояниям тамагочи."""
        raise NotImplementedError

    @abstractmethod
    def is_alive(self) -> bool:
        """Жив ли тамагочи?"""
        raise NotImplementedError

    @abstractmethod
    def is_sick(self) -> bool:
        """Не болеет ли тамагочи?"""
        raise NotImplementedError

    @abstractmethod
    def update(self) -> None:
        """Обновление состояния тамагочи."""
        raise NotImplementedError


class SimpleTamagochi(AbstractTamagochi):
    """Простая реализация питомца для игры."""

    MAX_VALUE = 100

    INITIAL_HUNGER = 20
    INITIAL_HP = 100
    INITIAL_ENERGY = 100
    INITIAL_FATIGUE = 0

    FEED_ENERGY = 5

    PLAY_ENERGY = 10
    PLAY_HUNGER = 10
    PLAY_FATIGUE = 10

    REST_POWER = 40
    SICK_REST_POWER = 20
    REST_HUNGER = 5

    TICK_HUNGER = 5
    TICK_ENERGY = 5
    TICK_FATIGUE = 5

    SICK_HUNGER = 80
    SICK_FATIGUE = 75
    SICK_HP_LOSS = 5
    STARVATION_HUNGER = 90
    STARVATION_HP_LOSS = 10
    LOW_ENERGY = 10
    LOW_ENERGY_HP_LOSS = 10

    def __init__(self) -> None:
        """Создать питомца с начальными показателями"""
        self._hunger = self.INITIAL_HUNGER
        self._hp = self.INITIAL_HP
        self._energy = self.INITIAL_ENERGY
        self._fatigue = self.INITIAL_FATIGUE
        self._sick = False

    @property
    def status(self) -> dict[str, int]:
        """Вернуть текущие показатели питомца."""
        return {
            "hunger": self._hunger,
            "hp": self._hp,
            "energy": self._energy,
            "fatigue": self._fatigue,
        }

    def is_alive(self) -> bool:
        """Проверить, жив ли питомец."""
        return self._hp > 0

    def is_sick(self) -> bool:
        """True, если питомец болеет, иначе False."""
        return self._sick

    def feed(self, food: Food) -> None:
        """Покормить питомца."""
        if not self.is_alive():
            raise TamagochiIsGone("Питомец умер, его нельзя покормить.")

        self._hunger = max(0, self._hunger - food.satiety)
        self._energy = min(
            self.MAX_VALUE,
            self._energy + self.FEED_ENERGY,
        )

    def play(self) -> None:
        """Поиграть с питомцем."""
        if not self.is_alive():
            raise TamagochiIsGone("Питомец умер, с ним нельзя играть.")

        self._energy = max(0, self._energy - self.PLAY_ENERGY)
        self._hunger = min(
            self.MAX_VALUE,
            self._hunger + self.PLAY_HUNGER,
        )
        self._fatigue = min(
            self.MAX_VALUE,
            self._fatigue + self.PLAY_FATIGUE,
        )

    def rest(self) -> None:
        """Дать питомцу отдохнуть."""
        if not self.is_alive():
            raise TamagochiIsGone("Питомец умер, он не может отдыхать")

        rest_power = self.SICK_REST_POWER if self.is_sick() else self.REST_POWER
        self._energy = min(self.MAX_VALUE, self._energy + rest_power)
        self._fatigue = max(0, self._fatigue - rest_power)
        self._hunger = min(
            self.MAX_VALUE,
            self._hunger + self.REST_HUNGER,
        )

    def heal(self, medicine: Medicine) -> None:
        """Вылечить питомца лекарством."""
        if not self.is_alive():
            raise TamagochiIsGone("Питомец умер, его нельзя лечить")

        if medicine.is_empty():
            raise ValueError("У лекарства закончились применения")

        medicine.uses += 1
        self._hp = min(self.MAX_VALUE, self._hp + medicine.heal_hp)
        self._sick = False

    def update(self) -> None:
        """Обновить состояние питомца на один игровой тик."""
        self._hunger = min(
            self.MAX_VALUE,
            self._hunger + self.TICK_HUNGER,
        )
        self._energy = max(0, self._energy - self.TICK_ENERGY)
        self._fatigue = min(
            self.MAX_VALUE,
            self._fatigue + self.TICK_FATIGUE,
        )

        if self._hunger >= self.SICK_HUNGER or self._fatigue >= self.SICK_FATIGUE:
            self._sick = True

        if self._sick:
            self._hp = max(0, self._hp - self.SICK_HP_LOSS)
            self._fatigue = min(
                self.MAX_VALUE,
                self._fatigue + self.TICK_FATIGUE,
            )

        if self._hunger >= self.STARVATION_HUNGER:
            self._hp = max(0, self._hp - self.STARVATION_HP_LOSS)

        if self._energy <= self.LOW_ENERGY:
            self._hp = max(0, self._hp - self.LOW_ENERGY_HP_LOSS)
