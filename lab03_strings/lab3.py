"""Лабораторна робота №3. Рядки.

Кожне завдання - окрема функція, що приймає рядок і повертає результат.
Якщо при введенні тексту натиснути Enter, використовується приклад тексту.
"""
import re

UA_SAMPLE = ("Python - мова програмування: проста, але потужна. "
             "Програми на Python пишуть швидко. Пайтон популярний: його "
             "вивчають у школах, а також в університетах. Текст для перевірки.")
EN_SAMPLE = ("Python was created by Guido van Rossum in the Netherlands. "
             "Today python is used at Google, NASA and Netflix. "
             "People love Python because it is simple. Pandas and NumPy help "
             "with data, while Django and Flask help with web development. "
             "Many developers in Ukraine and Poland use it daily. Keep it up.")

WORD_RE = r"[A-Za-zА-Яа-яЇїІіЄєҐґ'’]+"


def words(text):
    """Список слів без розділових знаків."""
    return re.findall(WORD_RE, text)


def task1(text, letter):
    """Кількість слів, що починаються з заданої літери (без врахування регістру)."""
    return sum(1 for w in words(text) if w.lower().startswith(letter.lower()))


def task2(text):
    """Замінити ':' на '%' і підрахувати кількість замін."""
    return text.replace(":", "%"), text.count(":")


def task3(text):
    """Видалити крапки і підрахувати кількість видалених символів."""
    return text.replace(".", ""), text.count(".")


def task4(text):
    """Замінити 'а' на 'о', порахувати заміни та довжину рядка."""
    # Текст український, тому замінюємо кириличну малу літеру "а".
    return text.replace("а", "о"), text.count("а"), len(text)


def task5(text):
    """Замінити всі великі літери малими."""
    return text.lower()


def task6(text):
    """Видалити всі літери 'о' і підрахувати їх кількість."""
    return text.replace("о", ""), text.count("о")


def task7(text):
    """Замінити '*' літери 'п' серед перших n/2 символів (n - довжина рядка)."""
    half = len(text) // 2
    return text[:half].replace("п", "*").replace("П", "*") + text[half:]


def task8(text, word):
    """Скільки разів у тексті трапляється задане слово (ціле слово, без регістру)."""
    return sum(1 for w in words(text) if w.lower() == word.lower())


def task9(text):
    """Кожне слово з великої літери."""
    # str.title() зіпсувало б слова з апострофом (don't -> Don'T),
    # тому робимо великою лише першу літеру кожного слова.
    return re.sub(WORD_RE, lambda m: m.group(0)[0].upper() + m.group(0)[1:], text)


def task10(text, first, last):
    """Слова, що починаються на first, і слова, що закінчуються на last."""
    ws = words(text)
    starts = [w for w in ws if w.lower().startswith(first.lower())]
    ends = [w for w in ws if w.lower().endswith(last.lower())]
    return starts, ends


VOWELS = set("aeiou")


def task11(text):
    """Кількість голосних англійських літер (нечутливо до регістру)."""
    return sum(1 for ch in text.lower() if ch in VOWELS)


def task12(text):
    """Кількість приголосних англійських літер (нечутливо до регістру)."""
    return sum(1 for ch in text.lower() if "a" <= ch <= "z" and ch not in VOWELS)


def task13(text):
    """Імена та власні назви всередині речень (слова з великої літери не на початку речення)."""
    result = []
    for sentence in re.split(r"(?<=[.!?])\s+", text):
        ws = words(sentence)
        result.extend(w for w in ws[1:] if w[0].isupper())
    return result


def ask_text(prompt, default):
    text = input(prompt + " (Enter - приклад): ")
    return text if text.strip() else default


def main():
    ua = ask_text("Введіть текст українською", UA_SAMPLE)
    print("Текст:", ua)
    letter = input("Завдання 1. Літера: ")
    print("1) Слів на літеру", repr(letter), "-", task1(ua, letter))
    t, n = task2(ua)
    print(f"2) {t}\n   Кількість замін ':' -> '%': {n}")
    t, n = task3(ua)
    print(f"3) {t}\n   Видалено крапок: {n}")
    t, n, length = task4(ua)
    print(f"4) {t}\n   Замін 'а' -> 'о': {n}, символів у рядку: {length}")
    print("5)", task5(ua))
    t, n = task6(ua)
    print(f"6) {t}\n   Видалено літер 'о': {n}")
    print("7)", task7(ua))
    word = input("Завдання 8. Слово для пошуку: ")
    print(f"8) Слово {word!r} трапляється {task8(ua, word)} раз(и)")

    en = ask_text("Введіть текст англійською", EN_SAMPLE)
    print("Text:", en)
    print("9)", task9(en))
    first = input("Завдання 10. Літера N (початок слова): ")
    last = input("Завдання 10. Літера P (кінець слова): ")
    starts, ends = task10(en, first, last)
    print(f"10) Починаються на {first!r}: {starts}\n    Закінчуються на {last!r}: {ends}")
    print("11) Голосних літер:", task11(en))
    print("12) Приголосних літер:", task12(en))
    print("13) Імена та власні назви:", task13(en))


if __name__ == "__main__":
    main()
