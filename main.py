import os

from game.clicker import SimpleRandomClicker
from game.exceptions import NotEnoughMoney, TamagochiIsGone
from game.game import SimpleGame
from game.models import Food, Medicine
from game.tamagochi import SimpleTamagochi

STATUS_TEMPLATE = (
    "\nСтатус: голод {hunger}, здоровье {hp}, энергия {energy}, монет {coins}\n"
)

MENU = [
    "1. Пойти на работу\n",
    "2. Купить еду\n",
    "3. Купить лекарство\n",
    "4. Покормить\n",
    "5. Вылечить\n",
    "6. Играть\n",
    "7. Отдых\n",
    "0. Выход",
]


def main() -> None:
    all_food = [
        Food(name="Бургер", satiety=20, price=40),
        Food(name="Салат", satiety=10, price=20),
        Food(name="Яблоко", satiety=10, price=15),
    ]

    all_medicine = [
        Medicine(
            name="Ибупрофен",
            price=30,
            heal_hp=20,
            number_of_uses=2,
        )
    ]

    tamagochi = SimpleTamagochi()
    clicker = SimpleRandomClicker(10, 20)
    game = SimpleGame(
        tamagochi,
        clicker,
        all_food=all_food,
        all_medicine=all_medicine,
    )

    print("Добро пожаловать в Тамагочи-кликер!")
    output = ""

    while True:
        print(output)

        print(f"Сумка с едой: {game.food}\nСумка с лекарствами: {game.medicine}")

        print(STATUS_TEMPLATE.format(**game.get_status()))

        if not game.tamagochi.is_alive():
            print("=======Тамагочи умер=======\nИгра окончена.")
            break
        if game.tamagochi.is_sick():
            print(
                "=======Тамагочи болеет======\n"
                "=======Отдых действует менее эффективно======="
            )

        print(MENU)

        try:
            match input("Выберите действие: "):
                case "1":
                    income = game.work()
                    output = f"Вы заработали {income} монет"
                case "2":
                    game.buy_food()
                case "3":
                    game.buy_medicine()
                case "4":
                    game.feed_tamagochi()
                case "5":
                    game.heal_tamagochi()
                case "6":
                    game.play_with_tamagochi()
                    output = "Вы поиграли с питомцем"
                case "7":
                    game.rest_tamagochi()
                    output = "Питомец отдохнул"
                case "0":
                    break
                case _:
                    output = "Неверная команда"
        except NotEnoughMoney:
            output = "Недостаточно монет для покупки."
        except TamagochiIsGone:
            output = "Питомец умер. Игра окончена."
            break

        os.system("cls" if os.name == "nt" else "clear")


if __name__ == "__main__":
    main()
