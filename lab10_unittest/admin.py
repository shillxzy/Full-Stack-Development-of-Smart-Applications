"""Завдання 9 d-e. Модуль з класами Privileges і Admin."""
from user import User

DEFAULT_PRIVILEGES = ["Allowed to add message", "Allowed to delete users", "Allowed to ban users"]


class Privileges:
    def __init__(self, privileges=None):
        self.privileges = list(privileges) if privileges is not None else DEFAULT_PRIVILEGES.copy()

    def show_privileges(self):
        text = "Привілеї адміністратора:\n" + "\n".join(f"- {p}" for p in self.privileges)
        print(text)
        return text


class Admin(User):
    """Адміністратор: користувач, привілеї якого зберігає об'єкт Privileges."""

    def __init__(self, first_name, last_name, email, nickname, newsletter=False, privileges=None):
        super().__init__(first_name, last_name, email, nickname, newsletter)
        self.priv = Privileges(privileges)
