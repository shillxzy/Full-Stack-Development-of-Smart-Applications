"""Підключення до бази даних (PostgreSQL у Docker або будь-яка інша через DATABASE_URL)."""
import os

import databases
import sqlalchemy

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/booksdb")

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()
engine = sqlalchemy.create_engine(DATABASE_URL)
