"""Завдання 1. Сума чисел з numbers.txt -> екран і sum_numbers.txt."""
from pathlib import Path

BASE = Path(__file__).parent

with open(BASE / "numbers.txt", encoding="utf-8") as f:
    # Порожні рядки пропускаємо; float дозволяє і цілі, і дробові числа.
    numbers = [float(line) for line in f if line.strip()]

total = sum(numbers)
total_text = f"{total:g}"
print("Числа з файлу:", ", ".join(f"{x:g}" for x in numbers))
print("Сума:", total_text)

with open(BASE / "sum_numbers.txt", "w", encoding="utf-8") as f:
    f.write(total_text + "\n")
print("Суму записано у файл sum_numbers.txt")
