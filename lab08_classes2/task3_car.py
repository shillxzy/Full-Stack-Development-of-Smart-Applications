"""Завдання 3. Клас Car."""


class Car:
    def __init__(self, make, model, year):
        self.make = make        # марка
        self.model = model      # модель
        self.year = year        # рік випуску
        self.speed = 0          # початкова швидкість

    def accelerate(self):
        self.speed += 5

    def brake(self):
        # Швидкість не може стати від'ємною.
        self.speed = max(0, self.speed - 5)

    def get_speed(self):
        return self.speed


if __name__ == "__main__":
    car = Car("Toyota", "Corolla", 2020)
    print(f"Автомобіль: {car.make} {car.model}, {car.year}")
    for _ in range(5):
        car.accelerate()
        print("Прискорення -> швидкість", car.get_speed(), "км/год")
    for _ in range(5):
        car.brake()
        print("Гальмування -> швидкість", car.get_speed(), "км/год")
