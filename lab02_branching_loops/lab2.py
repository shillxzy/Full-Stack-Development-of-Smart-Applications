"""Лабораторна робота №2. Розгалуження та цикли.

Кожне завдання оформлене окремою функцією. Під час запуску програма
питає номер завдання (0 - виконати всі по черзі).
"""
import math


def read_int(prompt):
    return int(input(prompt))


def read_float(prompt):
    return float(input(prompt).replace(",", "."))


def task1():
    """Вибрати з трьох цілих чисел ті, що належать відрізку [1, 3]."""
    numbers = [read_int(f"Ціле число {i}: ") for i in range(1, 4)]
    inside = [n for n in numbers if 1 <= n <= 3]
    if inside:
        print("Належать інтервалу [1,3]:", *inside)
    else:
        print("Жодне число не належить інтервалу [1,3]")


def is_leap(year):
    # Високосний: ділиться на 4, але не на 100, або ділиться на 400.
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def task2():
    """Кількість днів у році."""
    year = read_int("Номер року: ")
    if year <= 0:
        print("Рік має бути додатним цілим числом")
        return
    days = 366 if is_leap(year) else 365
    print(f"У {year} році {days} днів")


def task3():
    """Вартість покупки зі знижкою: >500 грн - 3%, >1000 грн - 5%."""
    total = read_float("Сума покупки, грн: ")
    if total > 1000:
        discount = 5
    elif total > 500:
        discount = 3
    else:
        discount = 0
    to_pay = total * (1 - discount / 100)
    print(f"Знижка {discount}%, до сплати: {to_pay:.2f} грн")


def task4():
    """Косинус мінімального з 4 чисел."""
    numbers = [read_float(f"Число {i}: ") for i in range(1, 5)]
    m = min(numbers)
    print(f"Мінімальне число {m}, cos({m}) = {math.cos(m):.6f}")


def task5():
    """Синус максимального з 3 чисел."""
    numbers = [read_float(f"Число {i}: ") for i in range(1, 4)]
    m = max(numbers)
    print(f"Максимальне число {m}, sin({m}) = {math.sin(m):.6f}")


def task6():
    """Площа рівнобедреного трикутника за основою та бічною стороною."""
    base = read_float("Основа a: ")
    side = read_float("Бічна сторона b: ")
    if base <= 0 or side <= 0 or 2 * side <= base:
        print("Трикутник з такими сторонами не існує")
        return
    height = math.sqrt(side ** 2 - (base / 2) ** 2)
    area = base * height / 2
    print(f"Площа трикутника: {area:g}")
    # "Парною" площа може бути лише тоді, коли вона ціле число.
    if area.is_integer() and int(area) % 2 == 0:
        print(f"Площа парна, ділимо на 2: {area / 2:g}")
    else:
        print("Не можу ділити на 2!")


MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]


def task7():
    """Назва місяця англійською за номером 1-12."""
    n = read_int("Номер місяця (1-12): ")
    if 1 <= n <= 12:
        print(MONTHS[n - 1])
    else:
        print("Такого місяця немає")


def task8():
    """Кількість додатних серед трьох чисел."""
    numbers = [read_float(f"Число {i}: ") for i in range(1, 4)]
    count = 0
    for x in numbers:
        if x > 0:
            count += 1
    print("Кількість додатних чисел:", count)


def read_a_less_b():
    a = read_int("A: ")
    b = read_int("B (B > A): ")
    if a >= b:
        raise ValueError("Має виконуватись умова A < B")
    return a, b


def task9():
    """Сума цілих від A до B включно (for)."""
    a, b = read_a_less_b()
    s = 0
    for i in range(a, b + 1):
        s += i
    print(f"Сума чисел від {a} до {b}: {s}")


def task10():
    """Сума квадратів цілих від A до B включно (for)."""
    a, b = read_a_less_b()
    s = 0
    for i in range(a, b + 1):
        s += i ** 2
    print(f"Сума квадратів від {a} до {b}: {s}")


def task11():
    """Середнє арифметичне цілих від a до 200 (for), a <= 200."""
    a = read_int("a (a <= 200): ")
    if a > 200:
        print("Має бути a <= 200")
        return
    s, count = 0, 0
    for i in range(a, 201):
        s += i
        count += 1
    print(f"Середнє арифметичне чисел від {a} до 200: {s / count}")


def task12():
    """Сума цілих від a до b (while), b >= a."""
    a = read_int("a: ")
    b = read_int("b (b >= a): ")
    if b < a:
        print("Має бути b >= a")
        return
    s, i = 0, a
    while i <= b:
        s += i
        i += 1
    print(f"Сума чисел від {a} до {b}: {s}")


def task13():
    """Сума квадратів цілих від a до 50 (for), 0 <= a <= 50."""
    a = read_int("a (0..50): ")
    if not 0 <= a <= 50:
        print("Має бути 0 <= a <= 50")
        return
    s = 0
    for i in range(a, 51):
        s += i * i
    print(f"Сума квадратів від {a} до 50: {s}")


def task14():
    """Найменше K, для якого 5**K > N (while), N > 1."""
    n = read_int("N (N > 1): ")
    if n <= 1:
        print("Має бути N > 1")
        return
    k = 0
    while 5 ** k <= n:
        k += 1
    print(f"Найменше K: {k} (5^{k} = {5 ** k} > {n})")


def task15():
    """Серед 1, 4, 9, 16, ... перше число, більше n (for)."""
    n = read_int("n: ")
    # Квадрат числа i перевищить n не пізніше, ніж при i = |n| + 1.
    for i in range(1, abs(n) + 2):
        if i * i > n:
            print(f"Перше число послідовності, більше {n}: {i * i}")
            break


def task16():
    """Серед 1, 5, 10, 17, 26, ... перше число, більше n (while, без if).

    Члени послідовності (крім першого) мають вигляд i^2 + 1.
    """
    n = read_int("n: ")
    value, i = 1, 1
    # Умова циклу сама "перевіряє" значення, тому оператор if не потрібен.
    while value <= n:
        i += 1
        value = i * i + 1
    print(f"Перше число послідовності, більше {n}: {value}")


TASKS = [task1, task2, task3, task4, task5, task6, task7, task8,
         task9, task10, task11, task12, task13, task14, task15, task16]


def main():
    choice = read_int("Номер завдання (1-16, 0 - усі): ")
    selected = TASKS if choice == 0 else [TASKS[choice - 1]]
    for func in selected:
        print(f"\n--- Завдання {TASKS.index(func) + 1}. {func.__doc__.splitlines()[0]}")
        try:
            func()
        except ValueError as e:
            print("Помилка введення:", e)


if __name__ == "__main__":
    main()
