"""Лабораторна робота №14. FastAPI + Ormar (модель без зовнішніх ключів) + PostgreSQL.

Запуск у Docker:  docker-compose up --build   ->  http://localhost:8000/docs
"""
import os

import databases
import nest_asyncio
import ormar
import sqlalchemy
from fastapi import FastAPI, HTTPException
from ormar.exceptions import NoMatch

# ---------- Підключення до бази даних ----------
# Адреса бази береться зі змінної середовища (її задає docker-compose.yml).
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://user:password@localhost:5432/booksdb"
)
database = databases.Database(DATABASE_URL)        # асинхронна робота з БД (запити)
metadata = sqlalchemy.MetaData()                   # опис таблиць
engine = sqlalchemy.create_engine(DATABASE_URL)    # синхронний рушій для create_all


# ---------- Модель даних ----------
class Book(ormar.Model):
    class Meta:
        tablename = "books"
        metadata = metadata
        database = database

    id: int = ormar.Integer(primary_key=True)
    title: str = ormar.String(max_length=100)
    description: str = ormar.Text()
    published_year: int = ormar.Integer()


# ---------- Додаток ----------
app = FastAPI(title="Books API")
nest_asyncio.apply()


async def seed_data():
    """Додає три книги, якщо таблиця порожня."""
    if await Book.objects.count() == 0:
        books_data = [
            {"title": "1984", "description": "Dystopian novel", "published_year": 1949},
            {"title": "To Kill a Mockingbird", "description": "Classic novel", "published_year": 1960},
            {"title": "The Great Gatsby", "description": "Novel by F. Scott Fitzgerald", "published_year": 1925},
        ]
        for b in books_data:
            await Book.objects.create(**b)
        print("Дані додані в базу!")


@app.on_event("startup")
async def startup():
    metadata.create_all(engine)          # створює таблиці, якщо їх ще немає
    if not database.is_connected:
        await database.connect()
    await seed_data()


@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()


# ---------- Ендпоїнти ----------
@app.get("/books/", tags=["Books"])
async def get_all_books():
    return await Book.objects.all()


@app.get("/books/{book_id}", tags=["Books"])
async def get_book_by_id(book_id: int):
    try:
        book = await Book.objects.get(id=book_id)
        return book
    except NoMatch:
        raise HTTPException(status_code=404, detail="Книга не знайдена")
