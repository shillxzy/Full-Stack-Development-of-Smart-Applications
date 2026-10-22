"""Запускає консольні програми лабораторних з підготовленими вхідними даними
і зберігає реальний вивід у <лаба>/outputs/<скрипт>.txt (використовується у звітах).

Запуск: .venv\\Scripts\\python run_all.py [префікс_папки ...]
"""
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent

# (папка, скрипт, аргументи, рядки вводу[, назва файлу виводу])
RUNS = [
    ("lab01_python_basics", "lab1.py", [], ["7", "3", "2.5", "1.5", "Студент Тестовий"]),
    ("lab02_branching_loops", "lab2.py", [], [
        "0",
        "2", "5", "1",            # 1
        "1900",                   # 2
        "1200",                   # 3
        "3", "-1.5", "8", "0.5",  # 4
        "1", "4", "2",            # 5
        "6", "5",                 # 6
        "10",                     # 7
        "-2", "0", "7",           # 8
        "1", "10",                # 9
        "1", "5",                 # 10
        "190",                    # 11
        "3", "7",                 # 12
        "45",                     # 13
        "100",                    # 14
        "30",                     # 15
        "20",                     # 16
    ]),
    ("lab03_strings", "lab3.py", [], ["", "п", "Python", "", "N", "P"]),
    ("lab04_lists", "lab4.py", [], ["5 -3 17 0 8 -12 4", "5 -3 17 0 8 -12 4"]),
    ("lab05_functions", "lab5.py", [], [
        "0",
        "3", "4", "2.5", "6", "10", "1",      # 1
        "3", "4", "6", "8",                   # 2
        "0", "0", "5", "1", "2", "4", "4", "-3", "-1",  # 3
        "3", "4", "4", "6",                   # 4
        "60", "3 4",                          # 5
        "1", "100",                           # 6
        "50", "list",                         # 7
        "15", "10", "5",                      # 8
    ]),
    ("lab05_functions", "lab5.py", [], ["8", "abc"], "lab5_err_type"),
    ("lab05_functions", "lab5.py", [], ["8", "10", "2.5"], "lab5_err_float"),
    ("lab05_functions", "lab5.py", [], ["8", "10", "60", "60"], "lab5_err_range"),
    ("lab06_files", "task1_sum_numbers.py", [], []),
    ("lab06_files", "task2_parity.py", ["4", "7", "-2", "15", "0", "abc"], []),
    ("lab06_files", "task3_learning_python.py", [], []),
    ("lab06_files", "task4_replace_language.py", [], ["C", "т", "т", "н", "т", "н", "т", "т"]),
    ("lab06_files", "task5_guest_book.py", [], ["Олена", "Андрій", "Ірина", ""]),
    ("lab06_files", "task6_frequency.py", [], ["python", "code", "z", "variable", ""]),
    ("lab06_files", "task7_marks.py", [], []),
    ("lab07_classes1", "main.py", [], []),
    ("lab08_classes2", "task1_bank.py", [], []),
    ("lab08_classes2", "task2_coin.py", [], ["10"]),
    ("lab08_classes2", "task3_car.py", [], []),
    ("lab08_classes2", "task4_dogs.py", [], []),
    ("lab08_classes2", "task5_buffer.py", [], []),
    ("lab08_classes2", "task6_name_error.py", [], ["Ivan"]),
    ("lab08_classes2", "task6_name_error.py", [], ["Maximilian Petrenko"], "task6_name_ok"),
    ("lab08_classes2", "task7_roman.py", [], []),
    ("lab08_classes2", "shop_main.py", [], []),
    ("lab08_classes2", "import_shop.py", [], []),
    ("lab08_classes2", "users_main.py", [], []),
    ("lab08_classes2", "import_admin.py", [], []),
    ("lab09_classes3", "task1_alphabet.py", [], []),
    ("lab09_classes3", "task2_human_house.py", [], []),
    ("lab09_classes3", "task3_garden.py", [], []),
    ("lab09_classes3", "task4_kmr.py", [], []),
    ("lab12_telegram_bot", "demo_console.py", [], ["1", "2", "1", "3", "1", "4", "1", "1", "2", "1"]),
    ("lab13_parsing", "lab13.py", [], []),
]


def run(folder, script, args, inputs, name=None):
    cwd = ROOT / folder
    stdin = "\n".join(inputs) + "\n"
    env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")
    proc = subprocess.run([sys.executable, str(ROOT / "_echo_runner.py"), script, *args], cwd=cwd, input=stdin,
                          capture_output=True, text=True, encoding="utf-8", env=env, timeout=600)
    # Прибираємо з traceback службові кадри запускача, щоб вивід був як при python script.py.
    err_lines = proc.stderr.splitlines(keepends=True)
    cleaned, skip = [], False
    for line in err_lines:
        if line.startswith("  File ") and ("_echo_runner.py" in line or "<frozen runpy>" in line):
            skip = True
            continue
        if skip and line.startswith("    "):
            continue
        skip = False
        cleaned.append(line)
    stderr = "".join(cleaned)
    out = proc.stdout + (("\n" + stderr) if stderr else "")
    out_dir = cwd / "outputs"
    out_dir.mkdir(exist_ok=True)
    cmd = " ".join(["python", script, *args])
    header = f"$ {cmd}\n"
    (out_dir / f"{name or Path(script).stem}.txt").write_text(header + out, encoding="utf-8")
    return proc.returncode


MAIN_PY = sys.executable
FASTAPI_PY = str(ROOT / ".venv-fastapi" / "Scripts" / "python.exe")
PG_URL = "postgresql://user:password@localhost:5433/"

# Прогони, вивід яких зберігається як є: (папка, назва файлу, команда, додаткові змінні, показана команда)
COMMANDS = [
    ("lab10_unittest", "pytest_initial_version", [MAIN_PY, "-m", "pytest", "-v", "--tb=line"],
     {"LAB10_SRC": "initial_version"}, "set LAB10_SRC=initial_version && python -m pytest -v"),
    ("lab10_unittest", "pytest_final", [MAIN_PY, "-m", "pytest", "-v"], {}, "python -m pytest -v"),
    ("lab11_flask", "pytest", [MAIN_PY, "-m", "pytest", "-v", "test_app.py"], {}, "python -m pytest -v test_app.py"),
    ("lab12_telegram_bot", "pytest", [MAIN_PY, "-m", "pytest", "-v", "test_quiz.py"], {}, "python -m pytest -v test_quiz.py"),
    ("lab13_parsing", "pytest", [MAIN_PY, "-m", "pytest", "-v", "test_parser.py"], {}, "python -m pytest -v test_parser.py"),
    # ЛР 14-15 - на локальному PostgreSQL (спершу start_postgres.ps1)
    ("lab14_fastapi_ormar", "pytest",
     [FASTAPI_PY, "-m", "pytest", "-v", "-s", "-W", "ignore::DeprecationWarning", "test_main.py"],
     {"DATABASE_URL": PG_URL + "booksdb"},
     "set DATABASE_URL=postgresql://user:***@localhost:5433/booksdb && python -m pytest -v -s test_main.py"),
    ("lab15_fastapi_fk", "pytest",
     [FASTAPI_PY, "-m", "pytest", "-v", "-s", "-W", "ignore::DeprecationWarning", "test_main.py"],
     {"DATABASE_URL": PG_URL + "booksdb_fk"},
     "set DATABASE_URL=postgresql://user:***@localhost:5433/booksdb_fk && python -m pytest -v -s test_main.py"),
    ("lab16_ml_web", "train_model", [MAIN_PY, "train_model.py"], {}, "python train_model.py"),
    ("lab16_ml_web", "pytest", [MAIN_PY, "-m", "pytest", "-v", "test_app.py"], {}, "python -m pytest -v test_app.py"),
]


def run_command(folder, name, cmd, extra_env, shown):
    cwd = ROOT / folder
    env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1", **extra_env)
    proc = subprocess.run([*cmd, "-p", "no:cacheprovider"] if "pytest" in cmd else cmd, cwd=cwd,
                          capture_output=True, text=True, encoding="utf-8", env=env, timeout=1800)
    # службові рядки pytest з шляхами до середовища у звіті не потрібні
    lines = [l for l in (proc.stdout + proc.stderr).splitlines()
             if not l.startswith(("platform ", "cachedir:", "rootdir:", "plugins:"))]
    out_dir = cwd / "outputs"
    out_dir.mkdir(exist_ok=True)
    (out_dir / f"{name}.txt").write_text(f"$ {shown}\n" + "\n".join(lines) + "\n", encoding="utf-8")
    return proc.returncode


if __name__ == "__main__":
    prefixes = sys.argv[1:]
    selected = lambda folder: not prefixes or any(folder.startswith(p) for p in prefixes)
    for folder, script, args, inputs, *name in RUNS:
        if selected(folder):
            code = run(folder, script, args, inputs, *name)
            print(f"{'OK ' if code == 0 else 'ERR'} {folder}/{script} (код {code})")
    for folder, name, cmd, extra_env, shown in COMMANDS:
        if selected(folder):
            code = run_command(folder, name, cmd, extra_env, shown)
            # pytest для початкової версії в ЛР 10 має падати - це очікувано
            print(f"{'OK ' if code == 0 else 'ERR'} {folder}/{name} (код {code})")
