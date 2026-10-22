"""Завдання 6. Частотний аналіз літер і слів у python_article.txt.

Результати виводяться в консоль і зберігаються у frequency_report.txt разом із
часом створення звіту, часом кожної зміни (дописування), результатами пошуку
та часом, витраченим на пошук.
"""
import re
import time
from collections import Counter
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).parent
ARTICLE = BASE / "python_article.txt"
REPORT = BASE / "frequency_report.txt"
FMT = "%Y-%m-%d %H:%M:%S"


def now():
    return datetime.now().strftime(FMT)


def append(text):
    """Дописує блок у звіт з позначкою часу зміни і дублює його в консоль."""
    print(text)
    with open(REPORT, "a", encoding="utf-8") as f:
        f.write(f"\n[Зміна: {now()}]\n{text}\n")


text = ARTICLE.read_text(encoding="utf-8").lower()   # регістр не враховуємо
words = re.findall(r"[a-z']+", text)
letters = [ch for ch in text if "a" <= ch <= "z"]
word_freq = Counter(words)
letter_freq = Counter(letters)

with open(REPORT, "w", encoding="utf-8") as f:
    f.write(f"Звіт частотного аналізу файлу {ARTICLE.name}\nСтворено: {now()}\n")

append(f"Слів у тексті: {len(words)}, різних слів: {len(word_freq)}, літер: {len(letters)}")
append("Частота літер:\n" + "\n".join(
    f"  {ch}: {n:5} ({n / len(letters):6.2%})" for ch, n in sorted(letter_freq.items())))
append("20 найчастіших слів:\n" + "\n".join(
    f"  {w:<12} {n}" for w, n in word_freq.most_common(20)))

# Пошук окремих літер чи слів, введених користувачем.
while True:
    query = input("Літера або слово для пошуку (Enter - завершити): ").strip().lower()
    if not query:
        break
    start = time.perf_counter()
    if len(query) == 1:
        count, kind = letter_freq.get(query, 0), "літера"
    else:
        count, kind = word_freq.get(query, 0), "слово"
    elapsed = time.perf_counter() - start
    append(f"Пошук: {kind} '{query}' - знайдено {count} раз(ів); час пошуку {elapsed * 1e6:.1f} мкс")

print(f"\nЗвіт збережено у {REPORT.name}")
