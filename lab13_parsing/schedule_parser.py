"""Лабораторна робота №13. Парсинг сайту розкладу занять ЧНУ (денна форма).

Джерело: розклад ННІ фізико-технічних та комп'ютерних наук (ІФТКН) ЧНУ, на
який посилається сайт інституту (ptcsi.chnu.edu.ua -> «Розклад занять»):
    https://shpatar26121974.github.io/nniftcn_schedule/

Сайт - односторінковий React-застосунок: HTML містить лише посилання на
JS-бандл, а сам розклад вшитий у бандл як JSON.parse('[...]'). Тому парсинг
виконується у три кроки:
    1) завантажуємо HTML і знаходимо (BeautifulSoup) адресу JS-бандла;
    2) завантажуємо бандл і вирізаємо рядок-аргумент JSON.parse(...);
    3) розкодовуємо екранування JavaScript і розбираємо JSON.

Кожен запис розкладу: day, period (номер пари), week (1 - непарний,
2 - парний тиждень), group, subject, teacher, room, type, source.
"""
import json
import re
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

SITE_URL = "https://shpatar26121974.github.io/nniftcn_schedule/"
CACHE = Path(__file__).parent / "schedule_cache.json"
HEADERS = {"User-Agent": "Mozilla/5.0 (lab13 schedule parser; educational use)"}

JS_ESCAPES = {"n": "\n", "t": "\t", "r": "\r", "b": "\b", "f": "\f", "0": "\0"}


def find_bundle_url(html, base_url):
    """Шукає в HTML тег <script src=".../main.*.js">."""
    soup = BeautifulSoup(html, "html.parser")
    for script in soup.find_all("script", src=True):
        if re.search(r"/main\.[0-9a-f]+\.js$", script["src"]):
            return urljoin(base_url, script["src"])
    raise ValueError("На сторінці не знайдено JS-бандл з розкладом")


def js_string_literal_after(code, marker):
    """Повертає вміст рядка в одинарних лапках, що йде після marker."""
    start = code.index(marker) + len(marker)
    end = start
    while True:
        end = code.index("'", end)
        # лапка екранована, якщо перед нею непарна кількість зворотних слешів
        slashes = len(code[:end]) - len(code[:end].rstrip("\\"))
        if slashes % 2 == 0:
            return code[start:end]
        end += 1


def js_unescape(text):
    """Розкодовує \\uXXXX, \\xXX, \\', \\\\ тощо з JavaScript-рядка."""
    def repl(match):
        esc = match.group(1)
        if esc[0] in "ux" and len(esc) > 1:
            return chr(int(esc[1:], 16))
        return JS_ESCAPES.get(esc, esc)
    return re.sub(r"\\(u[0-9a-fA-F]{4}|x[0-9a-fA-F]{2}|.)", repl, text)


def download_schedule(url=SITE_URL):
    """Завантажує й розбирає розклад із сайту; повертає список записів."""
    html = requests.get(url, headers=HEADERS, timeout=30)
    html.raise_for_status()
    bundle_url = find_bundle_url(html.text, url)
    bundle = requests.get(bundle_url, headers=HEADERS, timeout=60)
    bundle.raise_for_status()
    bundle.encoding = "utf-8"
    raw = js_string_literal_after(bundle.text, "JSON.parse('")
    records = json.loads(js_unescape(raw))
    print(f"Завантажено {len(records)} записів розкладу з {bundle_url}")
    return records


def load_schedule(refresh=False):
    """Бере розклад з кешу або завантажує з сайту (і зберігає кеш)."""
    if CACHE.exists() and not refresh:
        return json.loads(CACHE.read_text(encoding="utf-8"))
    records = download_schedule()
    CACHE.write_text(json.dumps(records, ensure_ascii=False, indent=0), encoding="utf-8")
    return records


# ---------- Нормалізація назв аудиторій ----------
# На сайті одна й та сама аудиторія записана по-різному:
# "8-117", "8-117*", "Корпус 8, ауд. 117", "к.8,а.117", "8-116 // 8-106".
ROOM_PATTERNS = [
    re.compile(r"^(\d+)\s*-\s*([\wА-ЯІЇЄҐа-яіїєґ]+)\*?$"),                      # 8-117, 8-117*
    re.compile(r"^корпус\s*(\d+)\s*,\s*(?:ауд|лаб)\.?\s*([\wА-ЯІЇЄҐа-яіїєґ]+)$", re.I),  # Корпус 8, ауд. 117
    re.compile(r"^к\.?\s*(\d+)\s*[,.]?\s*а\.?\s*([\wА-ЯІЇЄҐа-яіїєґ]+)$", re.I),     # к.8,а.117
]


def parse_rooms(room_text):
    """Перетворює текст аудиторії на список (корпус, номер). Онлайн/порожні -> []."""
    rooms = []
    for part in re.split(r"\s*//\s*", room_text.strip()):
        part = re.sub(r"\s+", " ", part.strip())
        for pattern in ROOM_PATTERNS:
            match = pattern.match(part)
            if match:
                rooms.append((int(match.group(1)), match.group(2).upper()))
                break
    return rooms


def room_label(building, number):
    return f"{building}-{number}"
