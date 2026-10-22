"""Завдання 5. Гостьова книга guest_book.txt.

Формат файлу:
    Створено: <час створення>
    Останні зміни: <час останнього запису>
    <час> | Вітаємо, <ім'я>! ...
Порожнє ім'я завершує введення.
"""
from datetime import datetime
from pathlib import Path

PATH = Path(__file__).parent / "guest_book.txt"
FMT = "%Y-%m-%d %H:%M:%S"


def load():
    """Повертає (час створення, список записів) з файлу."""
    if not PATH.exists() or PATH.stat().st_size == 0:
        return datetime.now().strftime(FMT), []
    lines = PATH.read_text(encoding="utf-8").splitlines()
    created = lines[0].removeprefix("Створено: ")
    return created, lines[2:]


def save(created, entries):
    modified = datetime.now().strftime(FMT)
    with open(PATH, "w", encoding="utf-8") as f:
        f.write(f"Створено: {created}\n")
        f.write(f"Останні зміни: {modified}\n")
        f.write("\n".join(entries) + ("\n" if entries else ""))


created, entries = load()
while True:
    name = input("Ваше ім'я (Enter - завершити): ").strip()
    if not name:
        break
    greeting = f"Вітаємо, {name}! Дякуємо, що завітали."
    print(greeting)
    entries.append(f"{datetime.now().strftime(FMT)} | {greeting}")
    save(created, entries)  # записуємо одразу, щоб не втратити дані

print("\nВміст guest_book.txt:")
print(PATH.read_text(encoding="utf-8"))
