"""Перевірка веб-додатку та навченої моделі на нових (не з датасету) рецензіях."""
import pytest

from app import app, classify

REVIEWS = [
    ("An absolute masterpiece. The acting is superb and the story is moving.", "POSITIVE"),
    ("I loved every minute of it, wonderful soundtrack and great characters!", "POSITIVE"),
    ("Funny, warm and smart. Best comedy I've seen this year.", "POSITIVE"),
    ("Worst movie ever. Boring plot, terrible acting, a complete waste of time.", "NEGATIVE"),
    ("The film was dull and predictable; I almost fell asleep.", "NEGATIVE"),
    ("Awful script and poorly directed. Very disappointing.", "NEGATIVE"),
]


@pytest.mark.parametrize("text, expected", REVIEWS)
def test_model_on_new_reviews(text, expected):
    label, _ = classify(text)
    assert label == expected


def test_home_page():
    r = app.test_client().get("/")
    assert r.status_code == 200 and "Movie Review Sentiment" in r.get_data(as_text=True)


def test_predict_endpoint():
    r = app.test_client().post("/predict", data={"message": REVIEWS[0][0]})
    html = r.get_data(as_text=True)
    assert "POSITIVE" in html and "Впевненість моделі" in html


def test_empty_input():
    r = app.test_client().post("/predict", data={"message": "   "})
    assert "Введіть текст рецензії" in r.get_data(as_text=True)
