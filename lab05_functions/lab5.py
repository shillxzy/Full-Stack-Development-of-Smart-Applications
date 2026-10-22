"""Лабораторна робота №5. Функції."""
import math
import random
import time
from functools import wraps


def read_float(prompt):
    return float(input(prompt).replace(",", "."))


# ---------- Завдання 1. Площі трьох прямокутників ----------
def rectangle_area(a, b):
    return a * b


def task1():
    for i in range(1, 4):
        a = read_float(f"Прямокутник {i}, сторона a: ")
        b = read_float(f"Прямокутник {i}, сторона b: ")
        print(f"  Площа прямокутника {i}: {rectangle_area(a, b):g}")


# ---------- Завдання 2. Гіпотенузи двох трикутників ----------
def hypotenuse(a, b):
    return math.sqrt(a ** 2 + b ** 2)


def task2():
    c1 = hypotenuse(read_float("Трикутник 1, катет a: "), read_float("Трикутник 1, катет b: "))
    c2 = hypotenuse(read_float("Трикутник 2, катет a: "), read_float("Трикутник 2, катет b: "))
    print(f"  Гіпотенуза 1 = {c1:.4f}, гіпотенуза 2 = {c2:.4f}")
    if c1 == c2:
        print("  Гіпотенузи рівні")
    else:
        bigger, smaller = (1, 2) if c1 > c2 else (2, 1)
        print(f"  Більша гіпотенуза у трикутника {bigger}, менша - у трикутника {smaller}")


# ---------- Завдання 3. Точки всередині кола ----------
def inside_circle(x, y, a, b, r):
    """True, якщо точка (x, y) лежить строго всередині кола (x-a)^2+(y-b)^2=R^2."""
    return (x - a) ** 2 + (y - b) ** 2 < r ** 2


def task3():
    a, b = read_float("Центр кола a: "), read_float("Центр кола b: ")
    r = read_float("Радіус R: ")
    count = 0
    for name in "PFL":
        x, y = read_float(f"Точка {name}, x: "), read_float(f"Точка {name}, y: ")
        inside = inside_circle(x, y, a, b, r)
        print(f"  {name}({x:g}, {y:g}) {'всередині' if inside else 'не всередині'} кола")
        count += inside
    print("  Кількість точок усередині кола:", count)


# ---------- Завдання 4. Площа чотирикутника ----------
def heron(a, b, c):
    p = (a + b + c) / 2
    return math.sqrt(p * (p - a) * (p - b) * (p - c))


def quadrilateral_area(x, y, z, t):
    """Кут між X і Y прямий: діагональ ділить фігуру на прямокутний
    трикутник (X, Y) і трикутник (d, Z, T), площу якого шукаємо за Героном."""
    d = math.hypot(x, y)
    if not (z + t > d and z + d > t and t + d > z):
        raise ValueError("Чотирикутник з такими сторонами не існує")
    return x * y / 2 + heron(d, z, t)


def task4():
    x, y, z, t = (read_float(f"Сторона {s}: ") for s in "XYZT")
    print(f"  Площа чотирикутника: {quadrilateral_area(x, y, z, t):.4f}")


# ---------- Завдання 5. Числа до n, що діляться на всі задані ----------
def divisible_by_all(n, divisors):
    return [k for k in range(1, n + 1) if all(k % d == 0 for d in divisors)]


def task5():
    n = int(input("n: "))
    divisors = [int(x) for x in input("Дільники через пробіл: ").split()]
    print("  Результат:", divisible_by_all(n, divisors))


# ---------- Декоратор для завдання 9 ----------
def timer(func):
    """Декоратор: вимірює і друкує час виконання функції."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        wrapper.last_time = time.perf_counter() - start
        return result
    wrapper.last_time = 0.0
    return wrapper


# ---------- Завдання 6. Числа з [M, N] з найбільшою кількістю дільників ----------
@timer
def most_divisors(m, n):
    """Кількість дільників рахуємо «решетом»: кожне d додає 1 усім своїм кратним.
    Складність O(N log N) замість O(N*sqrt(N)) при переборі."""
    counts = [0] * (n + 1)
    for d in range(1, n + 1):
        for multiple in range(d, n + 1, d):
            counts[multiple] += 1
    best = max(counts[m:n + 1])
    return best, [k for k in range(m, n + 1) if counts[k] == best]


def task6():
    m, n = int(input("M: ")), int(input("N: "))
    best, numbers = most_divisors(m, n)
    print(f"  Найбільша кількість дільників: {best}; числа: {numbers}")


# ---------- Завдання 7. Прості числа від 0 до N ----------
@timer
def primes(n, fmt="list"):
    """Решето Ератосфена. fmt: 'list' - список, 'column' - рядок у стовпчик,
    'count' - лише кількість."""
    sieve = bytearray([1]) * (n + 1)
    sieve[:2] = b"\x00\x00"[:n + 1]
    for i in range(2, int(n ** 0.5) + 1):
        if sieve[i]:
            sieve[i * i::i] = bytearray(len(range(i * i, n + 1, i)))
    found = [i for i in range(n + 1) if sieve[i]]
    if fmt == "list":
        return found
    if fmt == "column":
        return "\n".join(map(str, found))
    if fmt == "count":
        return len(found)
    raise ValueError("Формат має бути list, column або count")


def task7():
    n = int(input("N: "))
    fmt = input("Формат (list / column / count): ").strip()
    print(primes(n, fmt))


# ---------- Завдання 8. Вибірка з діапазону [MIN+bottom, MAX-upper] ----------
class RangeError(Exception):
    """Межі вибірки виходять за мінімальне/максимальне значення списку."""


def parse_natural(text, name):
    """Перетворює введений рядок на невід'ємне ціле з поясненням помилки."""
    try:
        value = float(text.replace(",", "."))
    except ValueError:
        raise ValueError(f"{name}: '{text}' - не число") from None
    if not value.is_integer():
        raise ValueError(f"{name}: дробові числа не допускаються ({text})")
    if value < 0:
        raise ValueError(f"{name}: значення не може бути від'ємним")
    return int(value)


@timer
def select_range(numbers, bottom, upper):
    lo, hi = min(numbers) + bottom, max(numbers) - upper
    if lo > hi:
        raise RangeError(f"MIN+bottom={lo} більше за MAX-upper={hi}")
    return [x for x in numbers if lo <= x <= hi]


def task8():
    try:
        length = parse_natural(input("Довжина списку: "), "Довжина")
        if length == 0:
            raise ValueError("Довжина: список не може бути порожнім")
        numbers = [random.randint(1, 100) for _ in range(length)]
        print("  Список:", numbers, f"(MIN={min(numbers)}, MAX={max(numbers)})")
        bottom = parse_natural(input("bottom: "), "bottom")
        upper = parse_natural(input("upper: "), "upper")
        print("  Новий список:", select_range(numbers, bottom, upper))
    except (ValueError, RangeError) as e:
        print("  Помилка:", e)


# ---------- Завдання 9. Час виконання для 10**n елементів ----------
def task9():
    print(f"  {'n':>2} {'елементів':>10} {'завд.6, с':>12} {'завд.7, с':>12} {'завд.8, с':>12}")
    for n in range(1, 7):
        size = 10 ** n
        most_divisors(1, size)
        primes(size, "count")
        select_range([random.randint(1, size) for _ in range(size)], 1, 1)
        print(f"  {n:>2} {size:>10} {most_divisors.last_time:>12.6f} "
              f"{primes.last_time:>12.6f} {select_range.last_time:>12.6f}")


TASKS = [task1, task2, task3, task4, task5, task6, task7, task8, task9]


def main():
    choice = int(input("Номер завдання (1-9, 0 - усі): "))
    selected = TASKS if choice == 0 else [TASKS[choice - 1]]
    for func in selected:
        print(f"\n--- Завдання {TASKS.index(func) + 1}")
        try:
            func()
        except ValueError as e:
            print("Помилка:", e)


if __name__ == "__main__":
    main()
