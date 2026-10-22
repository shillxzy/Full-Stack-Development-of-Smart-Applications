"""Тести для класів Shop і Discount (завдання 8 з ЛР №8)."""
import os
import subprocess
import sys
from pathlib import Path

import pytest

from shop import Discount, Shop


@pytest.fixture
def store():
    return Shop("Rozetka", "електроніка")


# --- a. атрибути та методи describe_shop / open_shop ---
def test_attributes(store):
    assert store.shop_name == "Rozetka"
    assert store.store_type == "електроніка"


def test_describe_shop_prints_both_attributes(store, capsys):
    result = store.describe_shop()
    out = capsys.readouterr().out
    assert "Rozetka" in out and "електроніка" in out
    assert result == out.strip()


def test_open_shop_message(store, capsys):
    store.open_shop()
    out = capsys.readouterr().out
    assert "Rozetka" in out and "відкритий" in out


# --- b. різні екземпляри незалежні ---
def test_three_instances_are_independent(capsys):
    shops = [Shop("A", "книги"), Shop("B", "одяг"), Shop("C", "іграшки")]
    for s in shops:
        s.describe_shop()
    lines = capsys.readouterr().out.strip().splitlines()
    assert len(lines) == 3
    assert ["книги" in lines[0], "одяг" in lines[1], "іграшки" in lines[2]] == [True] * 3


# --- c. number_of_units ---
def test_number_of_units_default_zero(store):
    assert store.number_of_units == 0


def test_number_of_units_can_be_changed_directly(store):
    store.number_of_units = 15
    assert store.number_of_units == 15


# --- d. set_number_of_units / increment_number_of_units ---
def test_set_number_of_units(store):
    store.set_number_of_units(250)
    assert store.number_of_units == 250


def test_increment_number_of_units(store):
    store.set_number_of_units(10)
    store.increment_number_of_units(5)
    store.increment_number_of_units(0)
    assert store.number_of_units == 15


@pytest.mark.parametrize("method", ["set_number_of_units", "increment_number_of_units"])
def test_negative_units_rejected(store, method):
    with pytest.raises(ValueError):
        getattr(store, method)(-1)
    assert store.number_of_units == 0


# --- e. Discount ---
def test_discount_is_shop_subclass():
    d = Discount("Outlet", "електроніка", ["мишка"])
    assert isinstance(d, Shop)
    assert d.shop_name == "Outlet" and d.number_of_units == 0


def test_get_discounts_products(capsys):
    d = Discount("Outlet", "електроніка", ["навушники", "мишка"])
    d.get_discounts_ptoducts()
    out = capsys.readouterr().out
    assert "навушники" in out and "мишка" in out


def test_discount_without_products(capsys):
    Discount("Outlet", "електроніка").get_discounts_ptoducts()
    assert "немає" in capsys.readouterr().out


def test_discount_lists_are_not_shared():
    """Регресійний тест: список товарів не має бути спільним для екземплярів."""
    products = ["мишка"]
    d1 = Discount("A", "x", products)
    d2 = Discount("B", "y")
    d1.discount_products.append("клавіатура")
    assert d2.discount_products == []
    assert products == ["мишка"]          # вхідний список не змінено


# --- f. імпорт модуля з окремого файлу ---
def test_import_from_separate_file(tmp_path):
    script = tmp_path / "import_shop.py"
    script.write_text("from shop import Shop\nall_store = Shop('All', 'різне')\nall_store.open_shop()\n",
                      encoding="utf-8")
    module_dir = Path(__file__).resolve().parent.parent
    proc = subprocess.run([sys.executable, str(script)], capture_output=True, text=True,
                          encoding="utf-8",
                          env=dict(os.environ, PYTHONPATH=str(module_dir), PYTHONIOENCODING="utf-8"))
    assert proc.returncode == 0, proc.stderr
    assert "All" in proc.stdout and "відкритий" in proc.stdout
