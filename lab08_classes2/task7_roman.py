"""Завдання 7. Перетворення десяткових чисел у римські й навпаки."""

ROMAN_TABLE = [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"),
               (90, "XC"), (50, "L"), (40, "XL"), (10, "X"), (9, "IX"),
               (5, "V"), (4, "IV"), (1, "I")]


class DecimalToRoman:
    @staticmethod
    def convert(number):
        if not isinstance(number, int) or not 1 <= number <= 3999:
            raise ValueError("Римськими цифрами записуються цілі числа від 1 до 3999")
        result = []
        for value, symbol in ROMAN_TABLE:
            count, number = divmod(number, value)
            result.append(symbol * count)
        return "".join(result)


class RomanToDecimal:
    VALUES = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}

    @classmethod
    def convert(cls, roman):
        roman = roman.strip().upper()
        if not roman or any(ch not in cls.VALUES for ch in roman):
            raise ValueError(f"'{roman}' - некоректне римське число")
        total = 0
        for i, ch in enumerate(roman):
            value = cls.VALUES[ch]
            # Менша цифра перед більшою віднімається (IV = 5 - 1).
            if i + 1 < len(roman) and value < cls.VALUES[roman[i + 1]]:
                total -= value
            else:
                total += value
        # Перевірка канонічності запису (відкидає, наприклад, IIII чи IC).
        if DecimalToRoman.convert(total) != roman:
            raise ValueError(f"'{roman}' - некоректне римське число")
        return total


if __name__ == "__main__":
    for n in (4, 9, 14, 40, 90, 400, 1994, 2024, 3999):
        r = DecimalToRoman.convert(n)
        print(f"{n:>4} -> {r:<12} -> {RomanToDecimal.convert(r)}")
    for bad in ("IIII", "ABC"):
        try:
            RomanToDecimal.convert(bad)
        except ValueError as e:
            print("Помилка:", e)
