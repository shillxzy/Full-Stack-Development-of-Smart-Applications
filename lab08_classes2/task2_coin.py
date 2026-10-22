"""Завдання 2. Клас Coin - монета, яку можна підкидати."""
import random


class Coin:
    SIDES = ("heads", "tails")   # heads - орел, tails - решка

    def __init__(self):
        self.__sideup = "heads"

    def toss(self):
        """Випадково визначає, якою стороною догори впала монета."""
        self.__sideup = random.choice(self.SIDES)
        return self.__sideup

    def get_sideup(self):
        return self.__sideup


if __name__ == "__main__":
    n = int(input("Скільки разів підкинути монету? "))
    coin = Coin()
    print("Початкова сторона:", coin.get_sideup())
    results = [coin.toss() for _ in range(n)]
    for i, side in enumerate(results, 1):
        print(f"Підкидання {i}: {side} ({'орел' if side == 'heads' else 'решка'})")
    print(f"Орлів: {results.count('heads')}, решок: {results.count('tails')}")
