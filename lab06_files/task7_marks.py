"""Завдання 7. Аналіз результатів КМР з marks.csv.

Структура рядка CSV (заголовка немає):
    id, час початку, час завершення, тривалість ("15 хв 17 сек"),
    оцінка (з 10, кома як десятковий роздільник), бали за 20 питань.
Значення "-" означає, що на питання не відповіли (0 балів).
"""
import csv
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

BASE = Path(__file__).parent
CSV_PATH = Path(sys.argv[1]) if len(sys.argv) > 1 else BASE / "marks.csv"
REPORT = BASE / "marks_stat.txt"


def to_float(value):
    return 0.0 if value.strip() == "-" else float(value.replace(",", "."))


def duration_minutes(text):
    """'1 год 2 хв 30 сек' -> 62.5 хв."""
    total = 0.0
    for number, unit in re.findall(r"(\d+)\s*(год|хв|сек)", text):
        total += int(number) * {"год": 60, "хв": 1, "сек": 1 / 60}[unit]
    return total


students = []
with open(CSV_PATH, encoding="utf-8-sig") as f:
    for row in csv.reader(f):
        if not row:
            continue
        students.append({
            "id": row[0],
            "minutes": duration_minutes(row[3]),
            "mark": to_float(row[4]),
            "answers": [to_float(v) for v in row[5:]],
        })

# 1. Кількість студентів.
print(f"Кількість студентів, що проходили тестування: {len(students)}")

# 2. Яку оцінку набрала відповідна кількість студентів.
print("\nРозподіл оцінок (оцінка: кількість студентів):")
for mark, n in sorted(Counter(s["mark"] for s in students).items()):
    print(f"  {mark:5.2f}: {n}")

# 3. Середня оцінка залежно від часу виконання (крок 1 хв).
by_minute = defaultdict(list)
for s in students:
    by_minute[int(s["minutes"])].append(s["mark"])
print("\nСередня оцінка за часом виконання КМР:")
for minute in sorted(by_minute):
    marks = by_minute[minute]
    print(f"  {minute:2}-{minute + 1:2} хв: {sum(marks) / len(marks):5.2f} (студентів: {len(marks)})")

# 4. Статистика правильних відповідей по кожному питанню.
# Правильною вважаємо відповідь з максимальним балом за питання.
questions = len(students[0]["answers"])
lines = ["Статистика відповідей по питаннях:"]
for q in range(questions):
    scores = [s["answers"][q] for s in students]
    max_score = max(scores)
    correct = sum(1 for x in scores if x == max_score) / len(scores) * 100
    lines.append(f"  Питання {q + 1:2}: правильних {correct:6.2f}%, неправильних {100 - correct:6.2f}%")

# 5. П'ять найкращих співвідношень оцінка / час.
best = sorted(students, key=lambda s: s["mark"] / s["minutes"], reverse=True)[:5]
lines.append("\n5 найкращих результатів (оцінка / хвилина):")
for i, s in enumerate(best, 1):
    lines.append(f"  {i}. {s['id']}  оцінка {s['mark']:.2f}, час {s['minutes']:.2f} хв, "
                 f"{s['mark'] / s['minutes']:.3f} бала/хв")

report = "\n".join(lines)
print("\n" + report)
REPORT.write_text(report + "\n", encoding="utf-8")
print(f"\nСтатистику записано у {REPORT.name}")
