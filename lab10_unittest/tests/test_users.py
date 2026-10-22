"""Тести для класів User, Admin, Privileges (завдання 9 з ЛР №8)."""
import pytest

import admin as admin_module
from admin import DEFAULT_PRIVILEGES, Admin, Privileges
from user import User


@pytest.fixture
def user():
    return User("Олена", "Коваленко", "olena@example.com", "olenka", True)


# --- a. атрибути та методи ---
def test_user_profile_attributes(user):
    assert (user.first_name, user.last_name) == ("Олена", "Коваленко")
    assert user.email == "olena@example.com"
    assert user.nickname == "olenka"
    assert user.newsletter is True


def test_newsletter_defaults_to_false():
    assert User("A", "B", "a@b.c", "ab").newsletter is False


def test_describe_user_contains_full_name(user, capsys):
    user.describe_user()
    assert "Олена Коваленко" in capsys.readouterr().out


def test_greeting_user_is_personal(user, capsys):
    text = user.greeting_user()
    assert "Олена" in text and text in capsys.readouterr().out


# --- b. login_attempts ---
def test_login_attempts_start_at_zero(user):
    assert user.login_attempts == 0


def test_increment_login_attempts(user):
    for _ in range(4):
        user.increment_login_attempts()
    assert user.login_attempts == 4


def test_reset_login_attempts(user):
    user.increment_login_attempts()
    user.increment_login_attempts()
    user.reset_login_attempts()
    assert user.login_attempts == 0


def test_login_attempts_independent_between_users(user):
    other = User("Андрій", "Мельник", "a@example.com", "andrew")
    user.increment_login_attempts()
    assert other.login_attempts == 0


# --- c, d. Admin і Privileges ---
def test_admin_is_user():
    a = Admin("Петро", "Іваненко", "admin@example.com", "root")
    assert isinstance(a, User)
    assert a.login_attempts == 0


def test_admin_has_privileges_object():
    a = Admin("Петро", "Іваненко", "admin@example.com", "root")
    assert isinstance(a.priv, Privileges)
    assert a.priv.privileges == DEFAULT_PRIVILEGES


def test_show_privileges_lists_all(capsys):
    Privileges().show_privileges()
    out = capsys.readouterr().out
    for p in DEFAULT_PRIVILEGES:
        assert p in out


def test_custom_privileges():
    a = Admin("П", "І", "a@b.c", "r", privileges=["Allowed to pin topics"])
    assert a.priv.privileges == ["Allowed to pin topics"]


def test_empty_privileges_list_is_respected():
    assert Privileges([]).privileges == []


def test_privileges_not_shared_between_admins():
    """Регресійний тест: зміна привілеїв одного адміна не впливає на інших."""
    a1 = Admin("A", "A", "a@a.a", "a")
    a2 = Admin("B", "B", "b@b.b", "b")
    a1.priv.privileges.append("Allowed to edit everything")
    assert "Allowed to edit everything" not in a2.priv.privileges
    assert "Allowed to edit everything" not in DEFAULT_PRIVILEGES


# --- e. класи у різних модулях ---
def test_classes_live_in_separate_modules():
    assert User.__module__ == "user"
    assert Admin.__module__ == "admin" and Privileges.__module__ == "admin"
    assert admin_module.User is User
