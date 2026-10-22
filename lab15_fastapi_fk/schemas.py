"""Pydantic-схеми для валідації вхідних даних.

У *Create усі обов'язкові поля мають бути передані; у *Update всі поля
необов'язкові (None) - так реалізуються PATCH-запити: оновлюються лише ті
поля, які клієнт явно передав (dict(exclude_unset=True)).
"""
from typing import Optional

from pydantic import BaseModel, Field, validator


class HumanCreate(BaseModel):
    name: str = Field(max_length=50)
    surname: str = Field(max_length=50)
    age: int = Field(ge=0)


class HumanUpdate(BaseModel):
    name: str = Field(None, max_length=50)
    surname: str = Field(None, max_length=50)
    age: int = Field(None, ge=0)


class DogCreate(BaseModel):
    name: str = Field(max_length=50)
    age: int = Field(ge=0)
    is_male: bool
    owner: Optional[int] = None


class DogUpdate(BaseModel):
    name: str = Field(None, max_length=50)
    age: int = Field(None, ge=0)
    is_male: bool = None
    owner: Optional[int] = None


class AuthorCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    surname: str = Field(min_length=1, max_length=50)
    birth_year: Optional[int] = Field(None, ge=0, le=2100)


class AuthorUpdate(BaseModel):
    name: str = Field(None, min_length=1, max_length=50)
    surname: str = Field(None, min_length=1, max_length=50)
    birth_year: Optional[int] = Field(None, ge=0, le=2100)


class BookCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: str = ""
    published_year: int = Field(ge=0, le=2100)
    author: Optional[int] = None

    @validator("title")
    def title_not_blank(cls, value):
        if not value.strip():
            raise ValueError("Назва не може складатися лише з пробілів")
        return value.strip()


class BookUpdate(BaseModel):
    title: str = Field(None, min_length=1, max_length=100)
    description: str = None
    published_year: int = Field(None, ge=0, le=2100)
    author: Optional[int] = None


class ReviewCreate(BaseModel):
    reviewer: str = Field(min_length=1, max_length=50)
    rating: int = Field(ge=1, le=5)
    text: str = ""
    book: int


class ReviewUpdate(BaseModel):
    reviewer: str = Field(None, min_length=1, max_length=50)
    rating: int = Field(None, ge=1, le=5)
    text: str = None
