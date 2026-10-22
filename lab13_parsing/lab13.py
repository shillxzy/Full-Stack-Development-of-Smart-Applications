"""Лабораторна робота №13. Аналіз розкладу ЧНУ (ІФТКН, 8 корпус).

Завдання:
 1. В яких аудиторіях 8 корпусу проводиться найбільше занять (усі групи, усі курси).
 2. Які аудиторії з комп'ютерною технікою найчастіше залишаються незадіяними.
 3. У якій аудиторії найчастіше проходять заняття вашої групи.

Запуск:
    python lab13.py                       # група 444(2) = 444(Б), 8 корпус
    python lab13.py --group "444(1)" --building 8 --refresh
    python lab13.py --computer-rooms 8-106 8-224 8-326   # свій перелік комп. класів
"""
import argparse
import collections
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from schedule_parser import SITE_URL, load_schedule, parse_rooms, room_label

RESULTS = Path(__file__).parent / "results"
DAYS = ["Понеділок", "Вівторок", "Середа", "Четвер", "П'ятниця"]
PERIODS = range(1, 7)            # у розкладі 6 пар на день
WEEKS = (1, 2)                   # непарний / парний тиждень
TOTAL_SLOTS = len(DAYS) * len(PERIODS) * len(WEEKS)

# Ознаки занять, що потребують комп'ютерів (практичні/лабораторні з ІТ-дисциплін).
IT_KEYWORDS = [
    "програм", "алгоритм", "web", "веб", "javascript", "java", "python", "c++", "с++",
    ".net", ".nет", "android", "kotlin", "мобільн", "бази даних", "скбд", "nosql", "devops",
    "linux", "операційні системи", "системне пз", "мереж", "backend", "інжиніринг даних",
    "data engineering", "bigdata", "business intelligence", "машинне навчання",
    "штучного інтелекту", "комп'ютерн", "комп’ютерн", "ui", "ux", "3d", "motion", "інтерфейс",
    "тестування", "тест-керована", "хмарн", "cloud", "кібер", "osint", "blockchain", "ооп",
    "об'єктно-орієнтоване", "моделювання систем", "інформаційно-комунікаційні", "інтернет",
    "геоінформаційні", "it essentials", "патерни", "паттерни", "мікросервіс",
]


def sessions(records, building):
    """Унікальні заняття в аудиторіях корпусу: (аудиторія, день, тиждень, пара) -> записи.

    Лекція для кількох груп у розкладі повторюється для кожної групи, тому
    рахуємо саме зайняті часові слоти аудиторії, а не рядки розкладу.
    """
    result = collections.defaultdict(list)
    for r in records:
        for b, number in parse_rooms(r["room"]):
            if b == building:
                result[(room_label(b, number), r["day"], r["week"], r["period"])].append(r)
    return result


def is_it_class(record):
    if record["type"] not in ("practice", "lab"):
        return False
    subject = record["subject"].lower()
    return any(k in subject for k in IT_KEYWORDS)


def detect_computer_rooms(room_sessions, min_sessions=3, share=0.5):
    """Комп'ютерна аудиторія - та, де більшість практичних/лабораторних занять
    (і щонайменше min_sessions) - з ІТ-дисциплін."""
    stats = collections.defaultdict(lambda: [0, 0])          # кімната -> [ІТ-практики, усі практики]
    for (room, *_), recs in room_sessions.items():
        practical = [r for r in recs if r["type"] in ("practice", "lab")]
        if practical:
            stats[room][1] += 1
            stats[room][0] += any(is_it_class(r) for r in practical)
    return sorted(room for room, (it, total) in stats.items()
                  if it >= min_sessions and it / total >= share), stats


def count_group_rooms(group_records):
    """Скільки пар група має в кожній аудиторії.

    Одна пара = (день, тиждень, номер пари); якщо в розкладі для неї вказано
    кілька аудиторій (підгрупи), враховується кожна з них.
    """
    counter = collections.Counter()
    slots = collections.defaultdict(set)
    for r in group_records:
        slots[(r["day"], r["week"], r["period"])].update(room_label(b, n) for b, n in parse_rooms(r["room"]))
    for rooms in slots.values():
        counter.update(rooms or {"онлайн / не вказано"})
    return counter


def bar_chart(labels, values, title, xlabel, path, color):
    fig, ax = plt.subplots(figsize=(10, 4.8))
    bars = ax.bar(labels, values, color=color)
    ax.bar_label(bars, fontsize=8)
    ax.set(title=title, xlabel=xlabel, ylabel="Кількість")
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()
    fig.savefig(path, dpi=110)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--group", default="444(2)", help="група як у розкладі (444(Б) = 444(2))")
    parser.add_argument("--building", type=int, default=8)
    parser.add_argument("--refresh", action="store_true", help="перезавантажити розклад із сайту")
    parser.add_argument("--computer-rooms", nargs="*", help="власний перелік комп'ютерних аудиторій, напр. 8-106")
    parser.add_argument("--top", type=int, default=10)
    args = parser.parse_args()

    records = load_schedule(refresh=args.refresh)
    RESULTS.mkdir(exist_ok=True)
    lines = [f"Джерело: {SITE_URL}", f"Записів у розкладі: {len(records)}, груп: "
             f"{len({r['group'] for r in records})}", ""]

    # ---------- Завдання 1 ----------
    room_sessions = sessions(records, args.building)
    per_room = collections.Counter(room for room, *_ in room_sessions)
    per_room_records = collections.Counter()
    for (room, *_), recs in room_sessions.items():
        per_room_records[room] += len(recs)
    lines.append(f"1. Аудиторії {args.building} корпусу з найбільшою кількістю занять "
                 f"(пар за 2 тижні; усього аудиторій: {len(per_room)})")
    lines.append(f"   {'Аудиторія':<10}{'Пар':>6}{'Зайнятість':>12}{'Записів груп':>14}")
    for room, n in per_room.most_common(args.top):
        lines.append(f"   {room:<10}{n:>6}{n / TOTAL_SLOTS:>12.0%}{per_room_records[room]:>14}")
    top = per_room.most_common(args.top)
    bar_chart([r for r, _ in top], [n for _, n in top],
              f"Найбільш завантажені аудиторії {args.building} корпусу (пар за 2 тижні)",
              "Аудиторія", RESULTS / "task1_busiest_rooms.png", "#4a90e2")

    # ---------- Завдання 2 ----------
    if args.computer_rooms:
        computer_rooms = sorted(args.computer_rooms)
        how = "задані користувачем"
    else:
        computer_rooms, stats = detect_computer_rooms(room_sessions)
        how = "визначені з розкладу: більшість практичних/лабораторних - з ІТ-дисциплін"
    lines += ["", f"2. Комп'ютерні аудиторії {args.building} корпусу ({how}): {len(computer_rooms)}",
              f"   Можливих слотів за 2 тижні: {len(DAYS)} днів x {len(PERIODS)} пар x 2 тижні = {TOTAL_SLOTS}",
              f"   {'Аудиторія':<10}{'Вільно':>8}{'Зайнято':>9}{'Вільних, %':>12}"]
    free = sorted(((TOTAL_SLOTS - per_room.get(r, 0), r) for r in computer_rooms), reverse=True)
    for n_free, room in free:
        lines.append(f"   {room:<10}{n_free:>8}{TOTAL_SLOTS - n_free:>9}{n_free / TOTAL_SLOTS:>12.0%}")
    if free:
        most_free = [r for n, r in free if n == free[0][0]]
        lines.append(f"   Найчастіше не задіяна: {', '.join(most_free)} ({free[0][0]} вільних пар із {TOTAL_SLOTS})")
        bar_chart([r for _, r in free], [n for n, _ in free],
                  "Вільні пари комп'ютерних аудиторій за 2 тижні", "Аудиторія",
                  RESULTS / "task2_free_computer_rooms.png", "#2e7d32")

    # ---------- Завдання 3 ----------
    group_records = [r for r in records if r["group"] == args.group]
    if not group_records:
        similar = sorted({r["group"] for r in records if args.group.split("(")[0] in r["group"]})
        raise SystemExit(f"Групу {args.group!r} не знайдено. Схожі: {similar}")
    group_rooms = count_group_rooms(group_records)
    # Вибіркові дисципліни кожен студент обирає сам, тому окремо рахуємо
    # лише обов'язкові - їх відвідує вся група.
    mandatory_rooms = count_group_rooms([r for r in group_records if "ВИБІРКОВА" not in r["subject"]])
    for title, counter in ((f"усі заняття, пар за 2 тижні: {sum(group_rooms.values())}", group_rooms),
                           (f"лише обов'язкові дисципліни, пар: {sum(mandatory_rooms.values())}", mandatory_rooms)):
        lines += ["", f"3. Аудиторії групи {args.group} ({title}):"]
        for room, n in counter.most_common():
            lines.append(f"   {room:<22}{n:>4}")
        best_n = counter.most_common(1)[0][1]
        best = [r for r, n in counter.items() if n == best_n]
        lines.append(f"   Найчастіше: {', '.join(best)} ({best_n} пар)")
    items = group_rooms.most_common()
    bar_chart([r for r, _ in items], [n for _, n in items], f"Аудиторії групи {args.group} (пар за 2 тижні)",
              "Аудиторія", RESULTS / "task3_group_rooms.png", "#c62828")

    report = "\n".join(lines)
    print(report)
    (RESULTS / "report.txt").write_text(report + "\n", encoding="utf-8")
    print(f"\nЗвіт і графіки збережено в {RESULTS}")


if __name__ == "__main__":
    main()
