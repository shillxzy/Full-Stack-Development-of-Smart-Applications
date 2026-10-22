"""Очищення тексту. Винесено в окремий модуль, щоб навчання і веб-додаток
обробляли текст однаково (інакше модель бачила б у додатку "інші" дані)."""
import re


def clean_text(text):
    text = text.lower()
    text = re.sub(r"<br\s*/?>", " ", text)           # у рецензіях IMDB є HTML-переноси
    text = re.sub(r"http\S+", " url ", text)
    text = re.sub(r"\S+@\S+", " email ", text)
    text = re.sub(r"[^a-z' ]", " ", text)             # апостроф лишаємо: don't, isn't
    text = re.sub(r"\s+", " ", text).strip()
    return text
