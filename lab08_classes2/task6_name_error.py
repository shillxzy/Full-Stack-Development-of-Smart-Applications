"""Завдання 6. Клас-виняток на основі ValueError для перевірки довжини імені."""


class NameTooShortError(ValueError):
    """Виникає, коли довжина імені менша за 10 символів."""

    MIN_LENGTH = 10

    def __init__(self, name):
        self.name = name
        super().__init__(f"Ім'я '{name}' занадто коротке: {len(name)} символів "
                         f"(потрібно щонайменше {self.MIN_LENGTH})")


def check_name(name):
    if len(name) < NameTooShortError.MIN_LENGTH:
        raise NameTooShortError(name)


if __name__ == "__main__":
    name = input("Введіть ім'я: ")
    check_name(name)   # для довгого імені нічого не виводиться
