"""Завдання 3. Читання learning_python.txt: перебір рядків і сортування за довжиною."""
from pathlib import Path

PATH = Path(__file__).parent / "learning_python.txt"

print("1) Перебір рядків файлу:")
with open(PATH, encoding="utf-8") as f:
    for line in f:
        print("  ", line.rstrip())

print("\n2) Рядки, збережені у список і відсортовані за довжиною (від найдовшого):")
with open(PATH, encoding="utf-8") as f:
    lines = [line.rstrip() for line in f if line.strip()]
for line in sorted(lines, key=len, reverse=True):
    print(f"   [{len(line):>3}] {line}")
