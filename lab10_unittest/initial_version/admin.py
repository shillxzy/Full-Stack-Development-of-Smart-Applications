"""Початкова (наївна) версія класів Privileges і Admin - до покриття тестами."""
from user import User

DEFAULT_PRIVILEGES = ["Allowed to add message", "Allowed to delete users", "Allowed to ban users"]


class Privileges:
    def __init__(self, privileges=None):
        self.privileges = privileges or DEFAULT_PRIVILEGES

    def show_privileges(self):
        print("Привілеї адміністратора:")
        for p in self.privileges:
            print("-", p)


class Admin(User):
    def __init__(self, first_name, last_name, email, nickname, newsletter=False, privileges=None):
        super().__init__(first_name, last_name, email, nickname, newsletter)
        self.priv = Privileges(privileges)
