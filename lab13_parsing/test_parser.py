"""Тести функцій парсингу (без звернення до мережі)."""
import pytest

from schedule_parser import find_bundle_url, js_string_literal_after, js_unescape, parse_rooms


@pytest.mark.parametrize("text, expected", [
    ("8-117", [(8, "117")]),
    ("8-224*", [(8, "224")]),
    ("Корпус 8, ауд. 117", [(8, "117")]),
    ("Корпус 8, лаб. 102Ц", [(8, "102Ц")]),
    ("к.8,а.117", [(8, "117")]),
    ("к.9, а.310", [(9, "310")]),
    ("Корпус 9,  ауд. 103Б", [(9, "103Б")]),
    ("8-116 // 8-106", [(8, "116"), (8, "106")]),
    ("онлайн", []),
    ("", []),
])
def test_parse_rooms(text, expected):
    assert parse_rooms(text) == expected


def test_find_bundle_url():
    html = '<html><head><script defer src="/app/static/js/main.8fdc9abb.js"></script></head></html>'
    assert find_bundle_url(html, "https://x.github.io/app/") == "https://x.github.io/app/static/js/main.8fdc9abb.js"


def test_js_string_and_unescape():
    code = r"""const i=JSON.parse('[{"day":"Пн","note":"it\'s"}]'),x=1;"""
    raw = js_string_literal_after(code, "JSON.parse('")
    assert js_unescape(raw) == '[{"day":"Пн","note":"it\'s"}]'
