"""Завдання 2. Парність чисел, переданих у командному рядку.

Запуск: python task2_parity.py 4 7 -2 15
"""
import sys
from pathlib import Path

OUT = Path(__file__).parent / "parity.txt"

if len(sys.argv) < 2:
    print("Передайте цілі числа в командному рядку, напр.: python task2_parity.py 4 7 -2")
    sys.exit(1)

lines = []
for arg in sys.argv[1:]:
    try:
        n = int(arg)
    except ValueError:
        lines.append(f"{arg}: не є цілим числом")
        continue
    lines.append(f"{n}: {'парне' if n % 2 == 0 else 'непарне'}")

with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

print("\n".join(lines))
print(f"Результат записано у файл {OUT.name}")
