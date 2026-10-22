"""Завдання 9 e. Імпорт Admin з окремого модуля і виклик show_privileges()."""
from admin import Admin

admin = Admin("Петро", "Іваненко", "admin@example.com", "root")
admin.describe_user()
admin.priv.show_privileges()
