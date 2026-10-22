"""Завдання 4. Замінити "Python" на іншу мову й розсортувати твердження.

1. Кожен рядок learning_python.txt виводиться із заміною Python -> мова.
2. Змінений текст записується у файл в новому каталозі <мова>_language/.
3. Користувач для кожного рядка вирішує, чи твердження істинне.
   Істинні залишаються в поточному файлі, хибні - у false_statements.txt.
"""
from pathlib import Path

BASE = Path(__file__).parent
language = input("Назва іншої мови (Enter - C): ").strip() or "C"

with open(BASE / "learning_python.txt", encoding="utf-8") as f:
    lines = [line.rstrip().replace("Python", language) for line in f if line.strip()]

print(f"\nТвердження для мови {language}:")
for line in lines:
    print("  ", line)

folder = BASE / f"{language.lower().replace(' ', '_')}_language"
folder.mkdir(exist_ok=True)
current = folder / f"learning_{language.lower().replace(' ', '_')}.txt"
with open(current, "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")
print(f"\nФайл зі зміненими фразами: {current.relative_to(BASE)}")

# Відкриваємо створений файл і читаємо його построково.
true_lines, false_lines = [], []
with open(current, encoding="utf-8") as f:
    for line in f:
        line = line.rstrip()
        answer = input(f"Актуально? (т/н) {line} -> ").strip().lower()
        (true_lines if answer in ("т", "так", "y", "yes", "+") else false_lines).append(line)

with open(current, "w", encoding="utf-8") as f:
    f.write("\n".join(true_lines) + ("\n" if true_lines else ""))
with open(folder / "false_statements.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(false_lines) + ("\n" if false_lines else ""))

print(f"\nІстинних: {len(true_lines)} -> {current.name}")
print(f"Хибних: {len(false_lines)} -> false_statements.txt")
