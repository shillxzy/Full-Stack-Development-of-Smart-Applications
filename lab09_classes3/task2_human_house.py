"""Завдання 2. Класи Human, House, SmallHouse."""


class House:
    def __init__(self, area=100, price=100_000):
        self._area = area
        self._price = price

    def final_price(self, discount):
        """Ціна з урахуванням знижки у відсотках."""
        return self._price * (1 - discount / 100)

    def __repr__(self):
        return f"{type(self).__name__}(площа={self._area} м2, ціна={self._price})"


class SmallHouse(House):
    def __init__(self, price=40_000):
        super().__init__(40, price)   # маленький будинок завжди 40 м2


class Human:
    default_name = "Невідомий"
    default_age = 18

    def __init__(self, name=default_name, age=default_age, money=0, house=None):
        self.name = name
        self.age = age
        self.__money = money
        self.__house = house

    def info(self):
        print(f"Ім'я: {self.name}\nВік: {self.age}\nБудинок: {self.__house}\nГроші: {self.__money:.2f}")

    @staticmethod
    def default_info():
        print(f"Ім'я за замовчуванням: {Human.default_name}\nВік за замовчуванням: {Human.default_age}")

    def __make_deal(self, house, price):
        """Технічна реалізація покупки: списати гроші і записати будинок."""
        self.__money -= price
        self.__house = house

    def earn_money(self, amount):
        if amount <= 0:
            raise ValueError("Сума заробітку має бути додатною")
        self.__money += amount

    def buy_house(self, house, discount=10):
        price = house.final_price(discount)
        if self.__money < price:
            print(f"Попередження: недостатньо грошей! Потрібно {price:.2f}, є {self.__money:.2f}")
            return False
        self.__make_deal(house, price)
        print(f"{self.name} купив(ла) {house} за {price:.2f}")
        return True


if __name__ == "__main__":
    Human.default_info()
    print()
    person = Human("Іван", 30, 10_000)
    person.info()
    print()
    small = SmallHouse()
    print("Створено:", small)
    person.buy_house(small)
    person.earn_money(30_000)
    print("Після earn_money(30000):")
    person.buy_house(small)
    print()
    person.info()
