"""Завдання 4. Аналіз результатів КМР: KmrCsv, Statistic, Plots, KmrWork.

Рядок CSV (без заголовка): id, початок, кінець, тривалість ("15 хв 17 сек"),
оцінка з 10 (десяткова кома), далі бали за кожне питання ("-" = 0).
"""
import csv
import re
from pathlib import Path

import matplotlib
matplotlib.use("Agg")            # будуємо графіки без вікна, лише у файли
import matplotlib.pyplot as plt

BASE = Path(__file__).parent


def to_float(value):
    return 0.0 if value.strip() == "-" else float(value.replace(",", "."))


def duration_minutes(text):
    units = {"год": 60, "хв": 1, "сек": 1 / 60}
    return sum(int(n) * units[u] for n, u in re.findall(r"(\d+)\s*(год|хв|сек)", text))


class KmrCsv:
    ref = str(BASE / "kmr1.csv")   # посилання на CSV з оцінками за замовчуванням
    num = 1                         # номер КМР за замовчуванням

    def set_ref(self, ref):
        self.ref = str(ref)

    def get_ref(self):
        return self.ref

    def set_num(self, num):
        self.num = num

    def get_num(self):
        return self.num

    def read_file(self):
        """Зчитує CSV у список словників і повертає його."""
        self.data = []
        with open(self.ref, encoding="utf-8-sig") as f:
            for row in csv.reader(f):
                if row:
                    self.data.append({
                        "id": row[0],
                        "minutes": duration_minutes(row[3]),
                        "mark": to_float(row[4]),
                        "answers": [to_float(v) for v in row[5:]],
                    })
        return self.data

    def file_info(self):
        text = f"КМР №{self.num}: файл {Path(self.ref).name}, виконали {len(self.data)} студентів"
        print(text)
        return text


class Statistic:
    """Міксин зі статистикою; працює з self.data, заповненим KmrCsv.read_file()."""

    def avg_stat(self):
        """Відсоток правильних відповідей (з максимальним балом) на кожне питання."""
        result = []
        for q in range(len(self.data[0]["answers"])):
            scores = [s["answers"][q] for s in self.data]
            best = max(scores)
            result.append(round(sum(x == best for x in scores) / len(scores) * 100, 2))
        return tuple(result)

    def marks_stat(self):
        """{оцінка: кількість студентів}."""
        stat = {}
        for s in self.data:
            stat[s["mark"]] = stat.get(s["mark"], 0) + 1
        return dict(sorted(stat.items()))

    def marks_per_time(self):
        """{id студента: середній бал за хвилину}."""
        return {s["id"]: round(s["mark"] / s["minutes"], 4) for s in self.data}

    def best_marks_per_time(self, bottom_margin, top_margin):
        """П'ять найкращих (id, оцінка, бал/хв) серед оцінок у [bottom_margin, top_margin]."""
        selected = [s for s in self.data if bottom_margin <= s["mark"] <= top_margin]
        selected.sort(key=lambda s: s["mark"] / s["minutes"], reverse=True)
        return tuple((s["id"], s["mark"], round(s["mark"] / s["minutes"], 4)) for s in selected[:5])


class Plots:
    """Міксин для побудови і збереження гістограм."""
    plots_dir = BASE / "plots"

    def set_cat(self, path):
        self.plots_dir = Path(path)

    def _save(self, fig, name):
        self.plots_dir.mkdir(parents=True, exist_ok=True)
        path = self.plots_dir / name
        fig.tight_layout()
        fig.savefig(path, dpi=110)
        plt.close(fig)
        print("Графік збережено:", path)
        return path

    def avg_plot(self, avg, title="Відсоток правильних відповідей", name=None):
        fig, ax = plt.subplots(figsize=(9, 4))
        ax.bar(range(1, len(avg) + 1), avg, color="#4a90e2")
        ax.set(xlabel="Номер питання", ylabel="Правильних відповідей, %", title=title, ylim=(0, 100))
        ax.set_xticks(range(1, len(avg) + 1))
        return self._save(fig, name or f"avg_kmr{self.num}.png")

    def marks_plot(self, marks):
        fig, ax = plt.subplots(figsize=(9, 4))
        ax.bar([f"{m:g}" for m in marks], marks.values(), color="#2e7d32")
        ax.set(xlabel="Оцінка", ylabel="Кількість студентів", title=f"Розподіл оцінок, КМР №{self.num}")
        ax.tick_params(axis="x", rotation=60)
        return self._save(fig, f"marks_kmr{self.num}.png")

    def best_marks_plot(self, best):
        fig, ax = plt.subplots(figsize=(8, 4))
        labels = [f"{sid[:6]}…\n({mark:g})" for sid, mark, _ in best]
        ax.bar(labels, [r for *_, r in best], color="#c62828")
        ax.set(ylabel="Бал за хвилину", title=f"5 найкращих результатів, КМР №{self.num}")
        return self._save(fig, f"best_kmr{self.num}.png")


class KmrWork(KmrCsv, Statistic, Plots):
    kmrs = {1: str(BASE / "kmr1.csv"), 2: str(BASE / "kmr2.csv")}
    cat = BASE / "results"

    def __init__(self, ref, num):
        self.set_ref(ref)
        self.set_num(num)
        self.set_cat(KmrWork.cat)
        self.read_file()

    def summary(self):
        marks = [s["mark"] for s in self.data]
        minutes = [s["minutes"] for s in self.data]
        return len(self.data), sum(marks) / len(marks), sum(minutes) / len(minutes)

    @classmethod
    def compare_csv(cls, num1=1, num2=2):
        """Порівняння двох КМР: кількість робіт, середній бал, середній час."""
        works = [cls(cls.kmrs[n], n) for n in (num1, num2)]
        lines = [f"{'Показник':<28}{'КМР №' + str(num1):>12}{'КМР №' + str(num2):>12}"]
        (c1, m1, t1), (c2, m2, t2) = (w.summary() for w in works)
        lines.append(f"{'Кількість виконаних КМР':<28}{c1:>12}{c2:>12}")
        lines.append(f"{'Середній бал':<28}{m1:>12.2f}{m2:>12.2f}")
        lines.append(f"{'Середній час виконання, хв':<28}{t1:>12.2f}{t2:>12.2f}")
        text = "\n".join(lines)
        print(text)
        cls.cat.mkdir(parents=True, exist_ok=True)
        (cls.cat / "compare.txt").write_text(text + "\n", encoding="utf-8")
        print("Порівняння збережено:", cls.cat / "compare.txt")
        return text

    @classmethod
    def compare_avg_plots(cls, num1=1, num2=2):
        """Дві гістограми відсотків правильних відповідей на одному рисунку."""
        works = [cls(cls.kmrs[n], n) for n in (num1, num2)]
        fig, axes = plt.subplots(2, 1, figsize=(9, 7), sharex=True)
        for ax, w in zip(axes, works):
            avg = w.avg_stat()
            ax.bar(range(1, len(avg) + 1), avg, color="#4a90e2")
            ax.set(ylabel="Правильних, %", title=f"КМР №{w.num}", ylim=(0, 100))
        axes[-1].set_xlabel("Номер питання")
        axes[-1].set_xticks(range(1, len(avg) + 1))
        return works[0]._save(fig, "compare_avg.png")


if __name__ == "__main__":
    kmr1 = KmrWork(KmrWork.kmrs[1], 1)
    kmr2 = KmrWork(KmrWork.kmrs[2], 2)
    kmr1.file_info()
    kmr2.file_info()
    print("\navg_stat (КМР 2):", kmr2.avg_stat())
    print("marks_stat (КМР 2):", kmr2.marks_stat())
    mpt = kmr2.marks_per_time()
    print("marks_per_time (КМР 2), перші 5:", dict(list(mpt.items())[:5]))
    best = kmr2.best_marks_per_time(8, 10)
    print("best_marks_per_time(8, 10) (КМР 2):")
    for row in best:
        print("  ", row)
    print()
    kmr2.avg_plot(kmr2.avg_stat(), "Відсоток правильних відповідей, КМР №2")
    kmr2.marks_plot(kmr2.marks_stat())
    kmr2.best_marks_plot(best)
    print()
    KmrWork.compare_csv()
    KmrWork.compare_avg_plots()
