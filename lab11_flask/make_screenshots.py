"""Робить скриншоти сторінок запущеного сайту для звіту (Playwright + Edge).

Запуск (сайт має працювати на http://localhost:5011):
    python make_screenshots.py <логін> <пароль>
"""
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE_URL = "http://localhost:5011"
OUT = Path(__file__).parent / "screenshots"
OUT.mkdir(exist_ok=True)
login, password = sys.argv[1], sys.argv[2]

with sync_playwright() as p:
    browser = p.chromium.launch(channel="msedge")
    page = browser.new_page(viewport={"width": 1280, "height": 800})

    def shot(name, url=None, full=True):
        if url:
            page.goto(BASE_URL + url)
        page.screenshot(path=OUT / f"{name}.png", full_page=full)
        print("saved", name)

    shot("01_home", "/")
    shot("02_history", "/history")
    shot("03_about", "/about")
    shot("04_albums_guest", "/albums")
    shot("05_album_page", "/albums/1")
    page.goto(BASE_URL + "/albums/new")            # гостя перенаправляє на вхід
    shot("06_login_redirect")

    page.fill("#username", login)
    page.fill("#password", password)
    page.click("button:has-text('Увійти')")
    shot("07_albums_admin", "/albums")

    page.goto(BASE_URL + "/albums/new")
    page.fill("#title", "Акустика")
    page.fill("#year", "2025")
    page.fill("#description", "Акустичні версії улюблених пісень.")
    page.fill("#tracks", "Перший сніг (acoustic)\nТиша (acoustic)\nПтахи (acoustic)")
    shot("08_album_form")
    page.click("button:has-text('Зберегти')")
    shot("09_album_created")

    page.click("a:has-text('Редагувати')")
    page.fill("#year", "2026")
    page.click("button:has-text('Зберегти')")
    shot("10_album_edited")

    page.once("dialog", lambda d: d.accept())
    page.click("button:has-text('Видалити')")
    shot("11_album_deleted")
    browser.close()
