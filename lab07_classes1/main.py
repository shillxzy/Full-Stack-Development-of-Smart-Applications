"""Демонстрація роботи класу Person та функції modifier()."""
import shutil
from pathlib import Path

from person import Person, modifier

BASE = Path(__file__).parent

print("=== Завдання 1. Клас Person ===")
p1 = Person("Шевченко", "Тарас", "1814-03-09", "Кобзар")
p2 = Person("Коваленко", "Олена", "20 02-12-31")   # рядок у форматі з методички
for p in (p1, p2):
    print(p)
    print("  Повне ім'я:", p.get_fullname())
    print("  Вік:", p.get_age())
    print("  Тип birth_date:", type(p.birth_date).__name__, p.birth_date)

print("\n=== Завдання 2. modifier(filename) ===")
# Беремо копію вихідного файлу, щоб оригінал залишився незмінним.
source, target = BASE / "contacts_source.csv", BASE / "contacts.csv"
shutil.copy(source, target)
print("До модифікації:\n" + target.read_text(encoding="utf-8"))
modifier(target)
print("Після модифікації:\n" + target.read_text(encoding="utf-8"))
