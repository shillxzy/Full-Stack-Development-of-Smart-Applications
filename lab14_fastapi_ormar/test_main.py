"""Перевірка API.

База береться зі змінної DATABASE_URL (локальний PostgreSQL, див. run_local.ps1);
якщо змінна не задана - тимчасова SQLite. Перед тестом таблиці створюються заново.

Запуск: python -m pytest -v test_main.py
"""
import os
from pathlib import Path

os.environ.setdefault("DATABASE_URL", f"sqlite:///{(Path(__file__).parent / 'test_books.db').as_posix()}")

from fastapi.testclient import TestClient  # noqa: E402

import main  # noqa: E402
from main import app  # noqa: E402


def test_books_api():
    print("База даних:", main.engine.url.render_as_string(hide_password=True))
    main.metadata.drop_all(main.engine)      # чистий старт
    with TestClient(app) as client:          # with запускає події startup/shutdown
        r = client.get("/books/")
        assert r.status_code == 200
        books = r.json()
        assert [b["title"] for b in books] == ["1984", "To Kill a Mockingbird", "The Great Gatsby"]

        r = client.get("/books/2")
        assert r.status_code == 200
        assert r.json() == {"id": 2, "title": "To Kill a Mockingbird",
                            "description": "Classic novel", "published_year": 1960}

        r = client.get("/books/999")
        assert r.status_code == 404
        assert r.json() == {"detail": "Книга не знайдена"}

        assert client.get("/books/abc").status_code == 422   # валідація типу параметра

    # Повторний старт не дублює початкові дані.
    with TestClient(app) as client:
        assert len(client.get("/books/").json()) == 3
