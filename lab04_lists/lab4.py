"""Лабораторна робота №4. Робота зі списками."""
import random


def read_int_list(prompt):
    """Зчитує цілі числа, введені через пробіл."""
    return [int(x) for x in input(prompt).split()]


def task1(numbers):
    """Максимальний елемент і список у зворотному порядку."""
    return max(numbers), numbers[::-1]


def task2(numbers):
    """Додатні елементи - в один список, решту - в інший."""
    positive = [x for x in numbers if x > 0]
    other = [x for x in numbers if x <= 0]
    return positive, other


def task3(numbers):
    """Сума елементів з непарними індексами (1, 3, 5, ...)."""
    return sum(numbers[1::2])


def task4(numbers):
    """Максимум, його порядковий номер і непарні числа за спаданням."""
    m = max(numbers)
    position = numbers.index(m) + 1  # порядковий номер рахуємо з 1
    odd = sorted((x for x in numbers if x % 2 != 0), reverse=True)
    return m, position, odd


def task5(numbers):
    """Пари від'ємних чисел, що стоять поруч."""
    return [(a, b) for a, b in zip(numbers, numbers[1:]) if a < 0 and b < 0]


def task6(numbers):
    """Квадрати чисел, менших за максимум, у порядку спадання."""
    m = max(numbers)
    return m, sorted((x * x for x in numbers if x < m), reverse=True)


def task7(numbers):
    """Мінімальний за модулем елемент і список за зростанням."""
    return min(numbers, key=abs), sorted(numbers)


def task8(numbers):
    """10 списків по 3 елементи, відсортовані за сумою модулів елементів."""
    chunks = [numbers[i:i + 3] for i in range(0, len(numbers), 3)]
    return sorted(chunks, key=lambda chunk: sum(abs(x) for x in chunk))


def random_ints(n=30):
    return [random.randint(-100, 100) for _ in range(n)]


def random_mixed(n=30):
    """Випадкові цілі та дробові числа від -100 до 100 (навпіл)."""
    return [random.randint(-100, 100) if i % 2 == 0
            else round(random.uniform(-100, 100), 2) for i in range(n)]


def main():
    nums = read_int_list("Завдання 1. Введіть цілі числа через пробіл: ")
    m, rev = task1(nums)
    print(f"1) Максимум: {m}; у зворотному порядку: {rev}")

    nums = read_int_list("Завдання 2. Введіть цілі числа через пробіл: ")
    pos, other = task2(nums)
    print(f"2) Додатні: {pos}; решта: {other}")

    nums = [random.randint(-50, 50) for _ in range(20)]
    print(f"3) Список: {nums}\n   Сума елементів з непарними індексами: {task3(nums)}")

    nums = random_ints()
    m, position, odd = task4(nums)
    print(f"4) Список: {nums}\n   Максимум {m} на позиції {position}")
    print("   Непарні за спаданням:", odd if odd else "непарних чисел немає")

    nums = random_ints()
    pairs = task5(nums)
    print(f"5) Список: {nums}\n   Пари сусідніх від'ємних: {pairs if pairs else 'немає'}")

    nums = [random.randint(-20, 20) for _ in range(10)]
    m, squares = task6(nums)
    print(f"6) Список: {nums}\n   Максимум {m}; квадрати менших за спаданням: {squares}")

    nums = random_mixed()
    mn, ordered = task7(nums)
    print(f"7) Список: {nums}\n   Мінімальний за модулем: {mn}\n   За зростанням: {ordered}")

    nums = random_mixed()
    print(f"8) Список: {nums}")
    for chunk in task8(nums):
        print(f"   {chunk}  сума модулів = {sum(abs(x) for x in chunk):.2f}")


if __name__ == "__main__":
    main()
