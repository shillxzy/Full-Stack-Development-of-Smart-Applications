"""Завдання 5. Клас Buffer - суми п'ятірок послідовності, що надходить частинами."""


class Buffer:
    def __init__(self):
        # Зберігаємо лише елементи, які ще не увійшли в повну п'ятірку.
        self._items = []

    def add(self, *a):
        """Додає наступну частину послідовності й друкує суми готових п'ятірок."""
        self._items.extend(a)
        sums = []
        while len(self._items) >= 5:
            sums.append(sum(self._items[:5]))
            print(sums[-1])
            del self._items[:5]   # видаляємо використані елементи
        return sums

    def get_current_part(self):
        """Повертає збережені елементи у порядку додавання."""
        return list(self._items)


if __name__ == "__main__":
    buf = Buffer()
    buf.add(1, 2, 3)
    print("Поточна частина:", buf.get_current_part())    # [1, 2, 3]
    buf.add(4, 5, 6)                                     # 15
    print("Поточна частина:", buf.get_current_part())    # [6]
    buf.add(7, 8, 9, 10)                                 # 40
    print("Поточна частина:", buf.get_current_part())    # []
    buf.add(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)             # 5, 5
    print("Поточна частина:", buf.get_current_part())    # [1]
