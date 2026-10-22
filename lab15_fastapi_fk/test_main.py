"""Функціональні тести API.

База береться зі змінної DATABASE_URL (локальний PostgreSQL, див. run_local.ps1);
якщо змінна не задана - тимчасова SQLite. Перед кожним тестом таблиці
створюються заново і заповнюються початковими даними.

Запуск: python -m pytest -v test_main.py
"""
import os
from pathlib import Path

import pytest

os.environ.setdefault("DATABASE_URL", f"sqlite:///{(Path(__file__).parent / 'test_lab15.db').as_posix()}")

from fastapi.testclient import TestClient  # noqa: E402

from database import engine, metadata  # noqa: E402
from main import app  # noqa: E402


def test_database_backend():
    print("База даних:", engine.url.render_as_string(hide_password=True))


@pytest.fixture
def client():
    metadata.drop_all(engine)
    with TestClient(app) as c:
        yield c


def test_seed_and_relations(client):
    books = client.get("/books/").json()
    assert len(books) == 4
    assert books[0]["author"]["surname"] == "Orwell"          # select_related підтягує автора
    book = client.get("/books/1").json()
    assert book["reviews"][0]["reviewer"] == "Olena"           # зворотний зв'язок book.reviews
    author = client.get("/authors/1").json()
    assert sorted(b["title"] for b in author["books"]) == ["1984", "Animal Farm"]
    assert len(client.get("/books/?author_id=1").json()) == 2


def test_author_crud(client):
    r = client.post("/authors/", json={"name": "Lina", "surname": "Kostenko", "birth_year": 1930})
    assert r.status_code == 201
    aid = r.json()["id"]
    r = client.patch(f"/authors/{aid}", json={"birth_year": 1931})
    assert r.json()["birth_year"] == 1931 and r.json()["name"] == "Lina"   # PATCH змінює лише передане
    assert client.delete(f"/authors/{aid}").status_code == 204
    assert client.get(f"/authors/{aid}").status_code == 404


def test_book_crud_with_foreign_key(client):
    r = client.post("/books/", json={"title": "Marusia Churai", "published_year": 1979, "author": 2})
    assert r.status_code == 201
    bid = r.json()["id"]
    assert client.get(f"/books/{bid}").json()["author"]["surname"] == "Lee"
    r = client.patch(f"/books/{bid}", json={"author": None})
    assert r.status_code == 200
    assert client.get(f"/books/{bid}").json()["author"] is None
    assert client.delete(f"/books/{bid}").status_code == 204


def test_review_crud(client):
    r = client.post("/reviews/", json={"reviewer": "Ira", "rating": 3, "book": 4})
    assert r.status_code == 201
    rid = r.json()["id"]
    assert client.patch(f"/reviews/{rid}", json={"rating": 5}).json()["rating"] == 5
    assert len(client.get("/reviews/?book_id=4").json()) == 1
    assert client.delete(f"/reviews/{rid}").status_code == 204


@pytest.mark.parametrize("url, payload", [
    ("/books/", {"title": "X", "published_year": 2000, "author": 999}),
    ("/reviews/", {"reviewer": "A", "rating": 4, "book": 999}),
    ("/dog/", {"name": "Max", "age": 1, "is_male": True, "owner": 999}),
])
def test_foreign_key_must_exist(client, url, payload):
    r = client.post(url, json=payload)
    assert r.status_code == 422 and "does not exist" in r.json()["detail"]


@pytest.mark.parametrize("url, payload", [
    ("/reviews/", {"reviewer": "A", "rating": 6, "book": 1}),          # рейтинг 1..5
    ("/books/", {"title": "   ", "published_year": 2000}),             # порожня назва
    ("/human/", {"name": "A", "surname": "B", "age": -1}),             # вік >= 0
    ("/authors/", {"name": "A" * 51, "surname": "B"}),                 # max_length
])
def test_validation_errors(client, url, payload):
    assert client.post(url, json=payload).status_code == 422


def test_integrity_on_delete(client):
    assert client.delete("/authors/1").status_code == 409     # у автора є книги
    assert client.delete("/human/1").status_code == 409       # у людини є собака
    assert client.delete("/books/1").status_code == 204       # книга видаляється разом з відгуками
    assert client.get("/reviews/?book_id=1").json() == []


def test_dog_and_human_endpoints(client):
    hid = client.post("/human/", json={"name": "Oksana", "surname": "Melnyk", "age": 25}).json()["id"]
    did = client.post("/dog/", json={"name": "Max", "age": 1, "is_male": True, "owner": hid}).json()["id"]
    assert client.get(f"/dog/{did}").json()["owner"]["name"] == "Oksana"
    assert client.patch(f"/dog/{did}", json={"age": 2}).json()["age"] == 2
    assert client.patch("/dog/999", json={"age": 2}).status_code == 404
    assert client.delete(f"/dog/{did}").status_code == 204
    assert client.delete(f"/human/{hid}").status_code == 204
    assert client.get("/human/999").status_code == 404
