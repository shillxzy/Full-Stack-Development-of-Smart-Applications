"""Завдання 9. Модуль з класом User (облік користувачів на сайті)."""


class User:
    def __init__(self, first_name, last_name, email, nickname, newsletter=False):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email                # поштова адреса
        self.nickname = nickname          # нікнейм, що показується на сайті
        self.newsletter = newsletter      # згода на розсилку новин форуму
        self.login_attempts = 0

    def describe_user(self):
        text = (f"Користувач: {self.first_name} {self.last_name} (@{self.nickname}), "
                f"email: {self.email}, розсилка: {'так' if self.newsletter else 'ні'}")
        print(text)
        return text

    def greeting_user(self):
        text = f"Вітаємо, {self.first_name}! Раді бачити вас знову на форумі."
        print(text)
        return text

    def increment_login_attempts(self):
        self.login_attempts += 1

    def reset_login_attempts(self):
        self.login_attempts = 0
