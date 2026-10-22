"""Завдання 4. Клас Dog, породи-нащадки і клас Pets."""


class Dog:
    # Атрибути класу - спільні для всіх собак.
    mammal = True
    nature = "дружелюбний"
    breed = "дворняга"

    def __init__(self, name, age):
        # Атрибути екземпляра - свої для кожної собаки.
        self.name = name
        self.age = age

    def description(self):
        return f"{self.name} - {self.age} р."

    def speak(self, sound="Гав!"):
        return f"{self.name} каже: {sound}"


class Labrador(Dog):
    nature = "лагідний і грайливий"
    breed = "лабрадор"

    def swim(self):
        return f"{self.name} радісно плаває в озері"


class GermanShepherd(Dog):
    nature = "відданий і пильний"
    breed = "німецька вівчарка"

    def guard(self):
        return f"{self.name} охороняє подвір'я"


class Dachshund(Dog):
    nature = "допитливий і впертий"
    breed = "такса"

    def dig(self):
        return f"{self.name} риє нору в саду"


class Pets:
    """Список домашніх улюбленців."""

    def __init__(self, animals):
        self.animals = list(animals)

    def walk(self):
        return [f"{a.name} гуляє" for a in self.animals]

    def info(self):
        lines = [f"У мене {len(self.animals)} собаки."]
        for a in self.animals:
            lines.append(f"{a.description()}, порода: {a.breed}, характер: {a.nature}. "
                         f"Ссавець: {'так' if a.mammal else 'ні'}.")
        return "\n".join(lines)


if __name__ == "__main__":
    dogs = [Labrador("Рекс", 3), GermanShepherd("Джек", 6), Dachshund("Бублик", 1)]
    for d in dogs:
        print(d.description())
    print()
    my_pets = Pets(dogs)
    print(my_pets.info())
    print()
    print(dogs[0].speak(), "|", dogs[0].swim())
    print(dogs[1].speak("Р-р-гав!"), "|", dogs[1].guard())
    print(dogs[2].speak("Тяв!"), "|", dogs[2].dig())
    print(*my_pets.walk(), sep="\n")
