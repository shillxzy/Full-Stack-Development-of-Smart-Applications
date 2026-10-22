"""Лабораторна робота №15. FastAPI + Ormar: моделі із зовнішніми ключами, CRUD.

Запуск у Docker:  docker-compose up --build   ->  http://localhost:8000/docs
"""
from typing import Type

import nest_asyncio
import ormar
from fastapi import FastAPI, HTTPException, Response
from ormar.exceptions import NoMatch

from database import database, engine, metadata
from models import Author, Book, Dog, Human, Review
from schemas import (AuthorCreate, AuthorUpdate, BookCreate, BookUpdate, DogCreate, DogUpdate,
                     HumanCreate, HumanUpdate, ReviewCreate, ReviewUpdate)

app = FastAPI(title="Books API з зовнішніми ключами")
app.state.database = database
nest_asyncio.apply()


# ---------------- Допоміжні функції ----------------
async def get_or_404(model: Type[ormar.Model], pk: int, *related):
    """Повертає об'єкт за id (з пов'язаними моделями) або 404."""
    query = model.objects.select_related(list(related)) if related else model.objects
    try:
        return await query.get(pk=pk)
    except NoMatch:
        raise HTTPException(status_code=404, detail=f"{model.__name__} with id {pk} not found!")


async def apply_update(instance: ormar.Model, data: dict):
    """PATCH: оновлює в базі лише передані поля й повертає свіжий запис.

    Оновлення робимо через QuerySet, а не instance.update(): в Ormar 0.11
    присвоєння None зв'язку на екземплярі ігнорується, тож запит
    {"author": null} не відв'язав би автора.
    """
    model = type(instance)
    if data:
        await model.objects.filter(pk=instance.pk).update(**data)
    return await model.objects.get(pk=instance.pk)


async def ensure_exists(model: Type[ormar.Model], pk, field: str):
    """Перевірка цілісності: зовнішній ключ має вказувати на існуючий запис."""
    if pk is not None and not await model.objects.filter(pk=pk).exists():
        raise HTTPException(status_code=422,
                            detail=f"{field}: {model.__name__} with id {pk} does not exist")


# ---------------- Події ----------------
async def seed_data():
    if await Author.objects.count() == 0:
        orwell = await Author.objects.create(name="George", surname="Orwell", birth_year=1903)
        lee = await Author.objects.create(name="Harper", surname="Lee", birth_year=1926)
        fitz = await Author.objects.create(name="F. Scott", surname="Fitzgerald", birth_year=1896)
        b1 = await Book.objects.create(title="1984", description="Dystopian novel",
                                       published_year=1949, author=orwell)
        await Book.objects.create(title="Animal Farm", description="Political satire",
                                  published_year=1945, author=orwell)
        b3 = await Book.objects.create(title="To Kill a Mockingbird", description="Classic novel",
                                       published_year=1960, author=lee)
        await Book.objects.create(title="The Great Gatsby", description="Novel by F. Scott Fitzgerald",
                                  published_year=1925, author=fitz)
        await Review.objects.create(reviewer="Olena", rating=5, text="Актуально як ніколи", book=b1)
        await Review.objects.create(reviewer="Andrii", rating=4, text="Сильна книга", book=b3)
    if await Human.objects.count() == 0:
        ivan = await Human.objects.create(name="Ivan", surname="Petrenko", age=30)
        await Dog.objects.create(name="Rex", age=3, is_male=True, owner=ivan)
        await Dog.objects.create(name="Bella", age=2, is_male=False, owner=None)


@app.on_event("startup")
async def startup():
    database_ = app.state.database
    if not database_.is_connected:
        await database_.connect()
    metadata.create_all(engine)
    await seed_data()


@app.on_event("shutdown")
async def shutdown():
    database_ = app.state.database
    if database_.is_connected:
        await database_.disconnect()


# ---------------- Human (приклад з методички) ----------------
@app.get("/human/", tags=["Human"])
async def get_humans():
    return await Human.objects.all()


@app.get("/human/{id}", tags=["Human"])
async def get_human_by_id(id: int):
    return await get_or_404(Human, id, "dogs")


@app.post("/human/", tags=["Human"], status_code=201)
async def create_human(human: HumanCreate):
    return await Human(**human.dict()).save()


@app.patch("/human/{id}", tags=["Human"])
async def update_human(id: int, human: HumanUpdate):
    db_human = await get_or_404(Human, id)
    return await apply_update(db_human, human.dict(exclude_unset=True))


@app.delete("/human/{id}", tags=["Human"], status_code=204)
async def delete_human(id: int):
    human = await get_or_404(Human, id)
    if await Dog.objects.filter(owner__id=id).exists():
        raise HTTPException(status_code=409, detail=f"Human with id {id} still owns dogs")
    await human.delete()
    return Response(status_code=204)


# ---------------- Dog (приклад з методички) ----------------
@app.get("/dog/", tags=["Dog"])
async def get_dogs():
    return await Dog.objects.select_related("owner").all()


@app.get("/dog/{id}", tags=["Dog"])
async def get_dog_by_id(id: int):
    return await get_or_404(Dog, id, "owner")


@app.post("/dog/", tags=["Dog"], status_code=201)
async def create_dog(dog: DogCreate):
    await ensure_exists(Human, dog.owner, "owner")
    return await Dog(**dog.dict()).save()


@app.patch("/dog/{id}", tags=["Dog"])
async def update_dog(id: int, dog: DogUpdate):
    db_dog = await get_or_404(Dog, id)
    data = dog.dict(exclude_unset=True)
    await ensure_exists(Human, data.get("owner"), "owner")
    return await apply_update(db_dog, data)


@app.delete("/dog/{id}", tags=["Dog"], status_code=204)
async def delete_dog(id: int):
    await (await get_or_404(Dog, id)).delete()
    return Response(status_code=204)


# ---------------- Author ----------------
@app.get("/authors/", tags=["Authors"])
async def get_authors():
    return await Author.objects.all()


@app.get("/authors/{id}", tags=["Authors"])
async def get_author(id: int):
    return await get_or_404(Author, id, "books")


@app.post("/authors/", tags=["Authors"], status_code=201)
async def create_author(author: AuthorCreate):
    return await Author(**author.dict()).save()


@app.patch("/authors/{id}", tags=["Authors"])
async def update_author(id: int, author: AuthorUpdate):
    db_author = await get_or_404(Author, id)
    return await apply_update(db_author, author.dict(exclude_unset=True))


@app.delete("/authors/{id}", tags=["Authors"], status_code=204)
async def delete_author(id: int):
    author = await get_or_404(Author, id)
    if await Book.objects.filter(author__id=id).exists():
        raise HTTPException(status_code=409,
                            detail=f"Author with id {id} has books; delete or reassign them first")
    await author.delete()
    return Response(status_code=204)


# ---------------- Book ----------------
@app.get("/books/", tags=["Books"])
async def get_books(author_id: int = None):
    query = Book.objects.select_related("author")
    if author_id is not None:
        query = query.filter(author__id=author_id)
    return await query.all()


@app.get("/books/{id}", tags=["Books"])
async def get_book(id: int):
    return await get_or_404(Book, id, "author", "reviews")


@app.post("/books/", tags=["Books"], status_code=201)
async def create_book(book: BookCreate):
    await ensure_exists(Author, book.author, "author")
    return await Book(**book.dict()).save()


@app.patch("/books/{id}", tags=["Books"])
async def update_book(id: int, book: BookUpdate):
    db_book = await get_or_404(Book, id)
    data = book.dict(exclude_unset=True)
    await ensure_exists(Author, data.get("author"), "author")
    return await apply_update(db_book, data)


@app.delete("/books/{id}", tags=["Books"], status_code=204)
async def delete_book(id: int):
    """Видаляє книгу разом з її відгуками (каскадне видалення вручну)."""
    book = await get_or_404(Book, id)
    async with database.transaction():
        # Фільтр за самим стовпцем зовнішнього ключа (без JOIN) - так DELETE
        # працює і в PostgreSQL, і в SQLite.
        await Review.objects.filter(book=id).delete()
        await book.delete()
    return Response(status_code=204)


# ---------------- Review ----------------
@app.get("/reviews/", tags=["Reviews"])
async def get_reviews(book_id: int = None):
    query = Review.objects.select_related("book")
    if book_id is not None:
        query = query.filter(book__id=book_id)
    return await query.all()


@app.get("/reviews/{id}", tags=["Reviews"])
async def get_review(id: int):
    return await get_or_404(Review, id, "book")


@app.post("/reviews/", tags=["Reviews"], status_code=201)
async def create_review(review: ReviewCreate):
    await ensure_exists(Book, review.book, "book")
    return await Review(**review.dict()).save()


@app.patch("/reviews/{id}", tags=["Reviews"])
async def update_review(id: int, review: ReviewUpdate):
    db_review = await get_or_404(Review, id)
    return await apply_update(db_review, review.dict(exclude_unset=True))


@app.delete("/reviews/{id}", tags=["Reviews"], status_code=204)
async def delete_review(id: int):
    await (await get_or_404(Review, id)).delete()
    return Response(status_code=204)
