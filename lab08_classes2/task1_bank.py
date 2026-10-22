"""Завдання 1. Клас Bank - прості операції з банківським рахунком."""


class Bank:
    def __init__(self, balance=0):
        if balance < 0:
            raise ValueError("Початковий баланс не може бути від'ємним")
        self.__balance = balance          # приватний атрибут (name mangling)

    def deposit(self, amount):
        """Покласти кошти на рахунок."""
        if amount <= 0:
            raise ValueError("Сума поповнення має бути додатною")
        self.__balance += amount
        return self.__balance

    def withdraw(self, amount):
        """Зняти кошти, якщо їх достатньо. Повертає True при успіху."""
        if amount <= 0:
            raise ValueError("Сума зняття має бути додатною")
        if amount > self.__balance:
            print(f"Недостатньо коштів: на рахунку {self.__balance:.2f}, потрібно {amount:.2f}")
            return False
        self.__balance -= amount
        return True

    def get_balance(self):
        """Переглянути рахунок."""
        return self.__balance


if __name__ == "__main__":
    account = Bank(1000)
    print("Початковий баланс:", account.get_balance())
    account.deposit(500)
    print("Після поповнення на 500:", account.get_balance())
    account.withdraw(300)
    print("Після зняття 300:", account.get_balance())
    account.withdraw(5000)
    print("Після спроби зняти 5000:", account.get_balance())
    try:
        print(account.__balance)
    except AttributeError as e:
        print("Прямий доступ до __balance заборонено:", e)
