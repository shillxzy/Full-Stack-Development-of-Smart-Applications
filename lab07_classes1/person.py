"""Лабораторна робота №7. Класи, ч. 1.

Завдання 1 - клас Person (запис у книзі контактів).
Завдання 2 - функція modifier(filename), що доповнює CSV-файл контактів
графами fullname (після name) та age (в кінці).
"""
import csv
import datetime


class Person:
    """Запис у книзі контактів."""

    def __init__(self, surname, first_name, birth_date, nickname=None):
        self.surname = surname
        self.first_name = first_name
        self.nickname = nickname or None   # порожній рядок -> відсутній псевдонім
        self.birth_date = self._parse_date(birth_date)

    @staticmethod
    def _parse_date(value):
        """Створює datetime.date з рядка 'РРРР-ММ-ДД'.

        Для datetime.date потрібні рік, місяць і день: дістаємо їх з рядка,
        перетворюємо на int і передаємо в конструктор.
        """
        if isinstance(value, datetime.date):
            return value
        cleaned = value.replace(" ", "")          # допускаємо '20 02-12-31'
        year, month, day = (int(part) for part in cleaned.split("-"))
        return datetime.date(year, month, day)

    def get_age(self):
        """Вік у повних роках на дату виклику, рядком: '25'."""
        today = datetime.date.today()
        had_birthday = (today.month, today.day) >= (self.birth_date.month, self.birth_date.day)
        return str(today.year - self.birth_date.year - (0 if had_birthday else 1))

    def get_fullname(self):
        """Повне ім'я: прізвище + ім'я."""
        return f"{self.surname} {self.first_name}"

    def __repr__(self):
        return (f"Person({self.surname!r}, {self.first_name!r}, "
                f"{self.birth_date.isoformat()!r}, nickname={self.nickname!r})")


def modifier(filename):
    """Читає CSV контактів, створює об'єкти Person і дописує у файл графи
    fullname (одразу після name) та age (останньою).

    Очікувані графи: surname, name, nickname, birth_date. Якщо файл уже
    оброблявся, значення fullname та age просто перераховуються.
    """
    with open(filename, encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
        if not rows:
            return []
    persons = [Person(r["surname"], r["name"], r["birth_date"], r.get("nickname")) for r in rows]

    base_fields = [c for c in rows[0].keys() if c not in ("fullname", "age")]
    fields = base_fields.copy()
    fields.insert(fields.index("name") + 1, "fullname")
    fields.append("age")

    with open(filename, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row, person in zip(rows, persons):
            row["fullname"] = person.get_fullname()
            row["age"] = person.get_age()
            writer.writerow({k: row.get(k, "") for k in fields})
    return persons
