"""Завдання 9 a-d. Демонстрація класів User, Admin, Privileges.

Пункт c (Admin з власним атрибутом privileges і методом show_privileges)
показано класом AdminV1 нижче; у пункті d список і метод перенесено в
клас Privileges (модуль admin.py).
"""
from admin import Admin
from user import User

print("--- a ---")
users = [
    User("Олена", "Коваленко", "olena@example.com", "olenka", True),
    User("Андрій", "Мельник", "andrii@example.com", "andrew_m"),
    User("Ірина", "Бондаренко", "iryna@example.com", "irka", True),
]
for u in users:
    u.describe_user()
    u.greeting_user()

print("\n--- b ---")
user = users[0]
for _ in range(3):
    user.increment_login_attempts()
print("login_attempts після 3 спроб:", user.login_attempts)
user.reset_login_attempts()
print("login_attempts після скидання:", user.login_attempts)

print("\n--- c ---")


class AdminV1(User):
    """Перша версія адміністратора: привілеї зберігаються в самому класі."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.privileges = ["Allowed to add message", "Allowed to delete users", "Allowed to ban users"]

    def show_privileges(self):
        print("Привілеї адміністратора:", *self.privileges, sep="\n- ")


AdminV1("Петро", "Іваненко", "admin@example.com", "root").show_privileges()

print("\n--- d ---")
admin = Admin("Петро", "Іваненко", "admin@example.com", "root")
admin.priv.show_privileges()
