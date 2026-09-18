"""Модуль с интерфейсом и реализацией класса игры"""

from abc import ABC, abstractmethod
from typing import Any

from .tamagochi import AbstractTamagochi
from .clicker import AbstractClicker
from .models import Food, Medicine
from .exceptions import NotEnoughMoney


class AbstractGame(ABC):
    """Интерфейс для логики игры"""

    @abstractmethod
    def __init__(
        self,
        tamagochi: AbstractTamagochi,
        clicker: AbstractClicker,
        all_food: list[Food],
        all_medicine: list[Medicine]
    ):
        """
        Абстрактный метод инициализации класса игры

        :param tamagochi: экземпляр тамагочи
        :param clicker: экземпляр кликера
        :param all_food: все доступные варианты еды
        :param all_medicine: все доступные варианты лекарств
        """
        raise NotImplementedError

    @abstractmethod
    def work(self) -> int:
        """
        Абстрактный метод для логики действия "работа

        :return: количество заработанных монет
        """
        raise NotImplementedError

    @abstractmethod
    def buy_food(self) -> None:
        """Абстрактный метод для покупки еды"""
        raise NotImplementedError

    @abstractmethod
    def buy_medicine(self) -> None:
        """Абстрактный метод для покупки лекарства"""
        raise NotImplementedError

    @abstractmethod
    def feed_tamagochi(self) -> None:
        """Абстрактный метод для кормления тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def heal_tamagochi(self) -> None:
        """Абстрактный метод для лечения тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def rest_tamagochi(self):
        """Абстрактный метод для отдыха тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def play_with_tamagochi(self):
        """Абстрактный метод для игры с тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def get_status(self) -> dict[str, Any]:
        """
        Абстрактный метод для получения статуса (всех характеристик) тамагочи

        :return: словарь со всеми характеристиками тамагочи
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def food(self) -> list[Food]:
        """
        Абстрактное свойство для доступа к сумке с едой

        :return: список с имеющимися (купленными) объектами еды
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def medicine(self) -> list[Medicine]:
        """
        Абстрактное свойство для доступа к сумке с лекарствами

        :return: список с имеющимися (купленными) объектами лекарств
        """
        raise NotImplementedError


class SimpleGame(AbstractGame):
    """Реализация игровой сессии тамагочи-кликера."""

    def __init__(
        self,
        tamagochi: AbstractTamagochi,
        clicker: AbstractClicker,
        all_food: list[Food],
        all_medicine: list[Medicine],
    ) -> None:
        """
        Создать игровую сессию.

        Args:
            tamagochi: Созданный питомец.
            clicker: Кликер для заработка монет.
            all_food: Вся еда, доступная в магазине.
            all_medicine: Все лекарства, доступные в магазине.
        """
        self.tamagochi = tamagochi
        self.clicker = clicker
        self._all_food = all_food
        self._all_medicine = all_medicine
        self._food: list[Food] = []
        self._medicine: list[Medicine] = []
        self._coins = 0

    @property
    def food(self) -> list[Food]:
        """
        Вернуть еду из сумки игрока.

        Returns:
            Копия списка купленной еды.
        """
        return list(self._food)
    
    @property
    def medicine(self) -> list[Medicine]:
        """
        Вернуть лекарства из сумки игрока.

        Returns:
            Копия списка купленных лекарств.
        """
        return list(self._medicine)
    
    def work(self) -> int:
        """
        Выполнить работу и начислить монеты.

        Returns:
            Количество монет, заработанных за работу.
        """
        self.clicker.click()
        income = self.clicker.income_per_click
        self._coins += income
        self.tamagochi.update()

        return income

    def get_status(self) -> dict[str, Any]:
        """
        Вернуть статус питомца и баланс игрока.

        Returns:
            Словарь с показателями питомца и количеством монет.
        """
        status = dict(self.tamagochi.status)
        status["coins"] = self._coins

        return status
    
    def buy_food(self) -> None:
        """
        Купить еду и положить её в сумку.

        Raises:
            NotEnoughMoney: Если монет на покупку не хватает.
        """
        if not self._all_food:
            print("В магазине нет еды.")
            return

        print("Доступная еда:")
        for number, food in enumerate(self._all_food, start=1):
            print(f"{number}. {food}")

        try:
            choice = int(input("Выберите номер еды: "))
        except ValueError:
            print("Нужно ввести целое число.")
            return

        if not 1 <= choice <= len(self._all_food):
            print("Еды с таким номером нет.")
            return

        selected_food = self._all_food[choice - 1]

        if self._coins < selected_food.price:
            raise NotEnoughMoney("Недостаточно монет для покупки еды.")

        self._coins -= selected_food.price
        self._food.append(selected_food)
        self.tamagochi.update()

    def buy_medicine(self) -> None:
        """
        Купить лекарство и положить его в сумку.

        Raises:
            NotEnoughMoney: Если монет на покупку не хватает.
        """
        if not self._all_medicine:
            print("В магазине нет лекарств.")
            return

        print("Доступные лекарства:")
        for number, medicine in enumerate(self._all_medicine, start=1):
            print(f"{number}. {medicine}")

        try:
            choice = int(input("Выберите номер лекарства: "))
        except ValueError:
            print("Нужно ввести целое число.")
            return

        if not 1 <= choice <= len(self._all_medicine):
            print("Лекарства с таким номером нет.")
            return

        selected_medicine = self._all_medicine[choice - 1]

        if self._coins < selected_medicine.price:
            raise NotEnoughMoney("Недостаточно монет для покупки лекарства.")

        purchased_medicine = Medicine(
            name=selected_medicine.name,
            price=selected_medicine.price,
            heal_hp=selected_medicine.heal_hp,
            number_of_uses=selected_medicine.number_of_uses,
        )

        self._coins -= purchased_medicine.price
        self._medicine.append(purchased_medicine)
        self.tamagochi.update()

    def feed_tamagochi(self) -> None:
        """Покормить питомца едой из сумки."""
        if not self._food:
            print("В сумке нет еды.")
            return

        print("Еда в сумке:")
        for number, food in enumerate(self._food, start=1):
            print(f"{number}. {food}")

        try:
            choice = int(input("Выберите номер еды: "))
        except ValueError:
            print("Нужно ввести целое число.")
            return

        if not 1 <= choice <= len(self._food):
            print("Еды с таким номером нет.")
            return

        selected_food = self._food[choice - 1]
        self.tamagochi.feed(selected_food)
        self._food.remove(selected_food)
        self.tamagochi.update()

    def heal_tamagochi(self) -> None:
        """Вылечить питомца лекарством из сумки."""
        if not self._medicine:
            print("В сумке нет лекарств.")
            return

        print("Лекарства в сумке:")
        for number, medicine in enumerate(self._medicine, start=1):
            print(f"{number}. {medicine}")

        try:
            choice = int(input("Выберите номер лекарства: "))
        except ValueError:
            print("Нужно ввести целое число.")
            return

        if not 1 <= choice <= len(self._medicine):
            print("Лекарства с таким номером нет.")
            return

        selected_medicine = self._medicine[choice - 1]
        self.tamagochi.heal(selected_medicine)
        self.tamagochi.update()

    def rest_tamagochi(self) -> None:
        """Дать питомцу отдохнуть."""
        self.tamagochi.rest()
        self.tamagochi.update()

    def play_with_tamagochi(self) -> None:
        """Поиграть с питомцем."""
        self.tamagochi.play()
        self.tamagochi.update()