"""Ormar-моделі.

Приклад з методички: Human -> Dog (Dog.owner - зовнішній ключ на Human).
Самостійна частина: розширення Books API з ЛР №14 -
    Author -> Book   (Book.author - зовнішній ключ, у книги може не бути автора);
    Book   -> Review (Review.book - обов'язковий зовнішній ключ на книгу).
"""
from typing import Optional

import ormar

from database import database, metadata


class BaseMeta(ormar.ModelMeta):
    database = database
    metadata = metadata


# ---------------- Приклад з методички ----------------
class Human(ormar.Model):
    class Meta(BaseMeta):
        tablename = "human"

    # У методичці BigInteger; Integer обрано, бо в SQLite (локальні тести)
    # автоінкремент працює лише для INTEGER PRIMARY KEY. У PostgreSQL - SERIAL.
    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=50)
    surname: str = ormar.String(max_length=50)
    age: int = ormar.Integer(minimum=0)


class Dog(ormar.Model):
    class Meta(BaseMeta):
        tablename = "dog"

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=50)
    age: int = ormar.Integer(minimum=0)
    is_male: bool = ormar.Boolean()
    owner: Optional[Human] = ormar.ForeignKey(Human, nullable=True, related_name="dogs")


# ---------------- Розширення Books API ----------------
class Author(ormar.Model):
    class Meta(BaseMeta):
        tablename = "authors"

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=50)
    surname: str = ormar.String(max_length=50)
    birth_year: Optional[int] = ormar.Integer(nullable=True)


class Book(ormar.Model):
    class Meta(BaseMeta):
        tablename = "books"

    id: int = ormar.Integer(primary_key=True)
    title: str = ormar.String(max_length=100)
    description: str = ormar.Text()
    published_year: int = ormar.Integer()
    # Зовнішній ключ: багато книг -> один автор. related_name дає зворотний
    # доступ author.books.
    author: Optional[Author] = ormar.ForeignKey(Author, nullable=True, related_name="books")


class Review(ormar.Model):
    class Meta(BaseMeta):
        tablename = "reviews"

    id: int = ormar.Integer(primary_key=True)
    reviewer: str = ormar.String(max_length=50)
    rating: int = ormar.Integer(minimum=1, maximum=5)
    text: str = ormar.Text(default="")
    book: Book = ormar.ForeignKey(Book, nullable=False, related_name="reviews")
