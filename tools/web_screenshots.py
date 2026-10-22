"""Скриншоти веб-лаб для звітів: запускає сервер, знімає сторінки, зупиняє сервер.

Запуск з кореня репозиторію: .venv\\Scripts\\python tools\\web_screenshots.py
"""
import os
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
FASTAPI_PY = ROOT / ".venv-fastapi" / "Scripts" / "python.exe"
MAIN_PY = ROOT / ".venv" / "Scripts" / "python.exe"


def wait_for(url, timeout=60):
    start = time.time()
    while time.time() - start < timeout:
        try:
            urllib.request.urlopen(url, timeout=2)
            return
        except Exception:
            time.sleep(0.5)
    raise RuntimeError(f"Сервер {url} не відповів")


def serve(folder, cmd, url, env=None):
    proc = subprocess.Popen(cmd, cwd=ROOT / folder, env={**os.environ, **(env or {})},
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    wait_for(url)
    return proc


def fastapi_lab(page, folder, port, db_name, actions):
    """Сервер працює з локальним PostgreSQL (start_postgres.ps1); таблиці очищаються,
    щоб на скриншотах були лише початкові дані."""
    env = {"DATABASE_URL": f"postgresql://user:password@localhost:5433/{db_name}"}
    subprocess.run([str(FASTAPI_PY), "-c", "from main import metadata, engine; metadata.drop_all(engine)"],
                   cwd=ROOT / folder, env={**os.environ, **env}, check=True)
    proc = serve(folder, [str(FASTAPI_PY), "-m", "uvicorn", "main:app", "--port", str(port)],
                 f"http://127.0.0.1:{port}/docs", env)
    out = ROOT / folder / "screenshots"
    out.mkdir(exist_ok=True)
    try:
        actions(page, f"http://127.0.0.1:{port}", out)
    finally:
        proc.terminate()
        proc.wait()


def swagger_try(page, out, name, tag_path, params=None, body=None):
    """Розгортає операцію у Swagger UI, виконує 'Try it out' і знімає відповідь."""
    op = page.locator(f"#{tag_path}")
    op.locator(".opblock-summary").click()
    op.locator("button.try-out__btn").click()
    for key, value in (params or {}).items():
        op.locator(f"tr[data-param-name='{key}'] input").fill(str(value))
    if body is not None:
        op.locator("textarea.body-param__text").fill(body)
    op.locator("button.execute").click()
    live = op.locator(".responses-wrapper .live-responses-table")
    live.wait_for()
    page.wait_for_timeout(400)
    # Знімаємо операцію лише до кінця фактичної відповіді сервера (без схем-прикладів нижче).
    # bounding_box() дає координати відносно вікна, а clip при full_page - відносно сторінки.
    scroll_y = page.evaluate("window.scrollY")
    top, bottom = op.bounding_box(), live.bounding_box()
    page.screenshot(path=out / f"{name}.png", full_page=True, clip={
        "x": top["x"], "y": top["y"] + scroll_y, "width": top["width"],
        "height": bottom["y"] + bottom["height"] - top["y"] + 10})
    print("saved", out.parent.name, name)


def lab14(page, base, out):
    page.goto(base + "/docs")
    page.wait_for_selector(".opblock")
    page.screenshot(path=out / "01_swagger.png", full_page=True)
    swagger_try(page, out, "02_get_books", "operations-Books-get_all_books_books__get")
    swagger_try(page, out, "03_get_book_by_id", "operations-Books-get_book_by_id_books__book_id__get", {"book_id": 2})
    page.goto(base + "/docs")
    page.wait_for_selector(".opblock")
    swagger_try(page, out, "04_get_book_404", "operations-Books-get_book_by_id_books__book_id__get", {"book_id": 99})


def lab15(page, base, out):
    page.goto(base + "/docs")
    page.wait_for_selector(".opblock")
    page.screenshot(path=out / "01_swagger.png", full_page=True)
    swagger_try(page, out, "02_get_book_with_relations", "operations-Books-get_book_books__id__get", {"id": 1})
    swagger_try(page, out, "03_create_book", "operations-Books-create_book_books__post",
                body='{\n  "title": "Animal Farm (2nd ed.)",\n  "description": "Satire",\n  "published_year": 1946,\n  "author": 1\n}')
    swagger_try(page, out, "04_create_review_bad_fk", "operations-Reviews-create_review_reviews__post",
                body='{\n  "reviewer": "Ira",\n  "rating": 5,\n  "text": "Top",\n  "book": 999\n}')
    swagger_try(page, out, "05_delete_author_conflict", "operations-Authors-delete_author_authors__id__delete", {"id": 1})


def ml_app(page):
    folder = "lab16_ml_web"
    proc = serve(folder, [str(MAIN_PY), "-m", "flask", "--app", "app", "run", "--port", "5016"],
                 "http://127.0.0.1:5016/")
    out = ROOT / folder / "screenshots"
    out.mkdir(exist_ok=True)
    samples = [
        ("01_empty", None),
        ("02_positive", "I loved this film. The cast is brilliant and the ending made me cry happy tears."),
        ("03_negative", "What a waste of two hours. The plot makes no sense and the acting is wooden."),
    ]
    try:
        for name, text in samples:
            page.goto("http://127.0.0.1:5016/")
            if text:
                page.fill("textarea", text)
                page.click("button")
                page.wait_for_selector(".result")
            page.screenshot(path=out / f"{name}.png", full_page=True)
            print("saved", folder, name)
    finally:
        proc.terminate()
        proc.wait()


if __name__ == "__main__":
    targets = sys.argv[1:] or ["lab14", "lab15", "lab16"]
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge")
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        if "lab14" in targets:
            fastapi_lab(page, "lab14_fastapi_ormar", 8014, "booksdb", lab14)
        if "lab15" in targets:
            fastapi_lab(page, "lab15_fastapi_fk", 8015, "booksdb_fk", lab15)
        if "lab16" in targets:
            page.set_viewport_size({"width": 800, "height": 650})
            ml_app(page)
        browser.close()
