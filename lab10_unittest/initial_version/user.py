"""Початкова (наївна) версія класу User - до покриття тестами."""


class User:
    def __init__(self, first_name, last_name, email, nickname, newsletter=False):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.nickname = nickname
        self.newsletter = newsletter
        self.login_attempts = 0

    def describe_user(self):
        print(f"Користувач: {self.first_name} {self.last_name}")

    def greeting_user(self):
        print(f"Вітаємо, {self.first_name}!")

    def increment_login_attempts(self):
        self.login_attempts += 1

    def reset_login_attempts(self):
        self.login_attempts = 0
