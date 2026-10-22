"""Завдання 1. Класи Alphabet та EngAlphabet."""
import string


class Alphabet:
    # Статичні атрибути - значення за замовчуванням для української мови.
    UA_LANG = "Uk"
    UA_LETTERS = list("абвгґдеєжзиіїйклмнопрстуфхцчшщьюя")

    def __init__(self, lang=UA_LANG, letters=None):
        self.lang = lang
        self.letters = list(letters) if letters is not None else Alphabet.UA_LETTERS.copy()

    def print_alphabet(self):
        print(" ".join(self.letters))

    def letters_num(self):
        return len(self.letters)

    @classmethod
    def is_ua_lang(cls, text):
        """True, якщо всі літери тексту - з українського алфавіту (регістр не важливий).

        Апостроф і неалфавітні символи (пробіли, цифри, розділові знаки) ігноруються.
        """
        letters = [ch for ch in text.lower() if ch.isalpha()]
        return bool(letters) and all(ch in cls.UA_LETTERS for ch in letters)


class EngAlphabet(Alphabet):
    __en_letters_num = 26     # приватний статичний атрибут

    def __init__(self):
        super().__init__("En", string.ascii_uppercase)

    def is_en_letter(self, text):
        """True, якщо рядок складається лише з літер англійського алфавіту."""
        return bool(text) and all(ch.upper() in self.letters for ch in text)

    def letters_num(self):
        return EngAlphabet.__en_letters_num

    @staticmethod
    def example():
        return "The quick brown fox jumps over the lazy dog."


if __name__ == "__main__":
    eng = EngAlphabet()
    print("Літери англійського алфавіту:")
    eng.print_alphabet()
    print("Кількість літер:", eng.letters_num())
    print("Чи J належить до англійського алфавіту?", eng.is_en_letter("J"))
    print("Чи Щ належить до українського алфавіту?", eng.is_ua_lang("Щ"))
    print("Приклад тексту англійською:", EngAlphabet.example())
    ua = Alphabet()
    print("\nУкраїнський алфавіт:")
    ua.print_alphabet()
    print("Кількість літер:", ua.letters_num())
    print("'Привіт, світе!' українською?", ua.is_ua_lang("Привіт, світе!"))
    print("'Hello' українською?", ua.is_ua_lang("Hello"))
