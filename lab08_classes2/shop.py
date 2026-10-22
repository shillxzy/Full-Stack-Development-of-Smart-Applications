"""Завдання 8. Модуль з класами Shop і Discount (онлайн-магазин).

Методи, що "виводять" інформацію, друкують її і повертають той самий рядок -
так їх зручно і показувати в консолі, і перевіряти тестами.
"""


class Shop:
    def __init__(self, shop_name, store_type, number_of_units=0):
        self.shop_name = shop_name
        self.store_type = store_type
        self.number_of_units = number_of_units   # кількість видів товару

    def describe_shop(self):
        text = f"Магазин «{self.shop_name}», тип: {self.store_type}"
        print(text)
        return text

    def open_shop(self):
        text = f"Онлайн-магазин «{self.shop_name}» відкритий!"
        print(text)
        return text

    def set_number_of_units(self, number):
        if number < 0:
            raise ValueError("Кількість видів товару не може бути від'ємною")
        self.number_of_units = number

    def increment_number_of_units(self, amount):
        if amount < 0:
            raise ValueError("Приріст не може бути від'ємним")
        self.number_of_units += amount


class Discount(Shop):
    def __init__(self, shop_name, store_type, discount_products=None, number_of_units=0):
        super().__init__(shop_name, store_type, number_of_units)
        # Новий список для кожного екземпляра (не спільний аргумент за замовчуванням).
        self.discount_products = list(discount_products) if discount_products else []

    def get_discounts_ptoducts(self):
        """Назва методу збережена так, як у методичці."""
        text = "Товари зі знижкою: " + (", ".join(self.discount_products) or "немає")
        print(text)
        return text
