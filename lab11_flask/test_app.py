"""Автоматична перевірка сайту через тестовий клієнт Flask (pytest)."""
import os

import pytest

os.environ["DATABASE_URL"] = "sqlite://"     # окрема база в пам'яті для тестів

from app import Album, User, app, db, seed   # noqa: E402

TEST_LOGIN = "tester"
TEST_PASSWORD = "test-password-123"


@pytest.fixture
def client():
    app.config.update(TESTING=True)
    with app.app_context():
        db.drop_all()
        seed()
        user = User(username=TEST_LOGIN)
        user.set_password(TEST_PASSWORD)
        db.session.add(user)
        db.session.commit()
    with app.test_client() as c:
        yield c


def login(client, password=TEST_PASSWORD):
    return client.post("/login", data={"username": TEST_LOGIN, "password": password},
                       follow_redirects=True)


@pytest.mark.parametrize("url, text", [
    ("/", "Останні релізи"), ("/about", "Про проект"),
    ("/history", "Історія гурту"), ("/albums", "Дискографія"), ("/albums/1", "Трек-лист"),
])
def test_public_pages(client, url, text):
    r = client.get(url)
    assert r.status_code == 200
    assert text in r.get_data(as_text=True)


def test_unknown_album_404(client):
    assert client.get("/albums/999").status_code == 404


def test_guest_cannot_manage_albums(client):
    assert client.get("/albums/new").status_code == 302          # редірект на вхід
    assert client.post("/albums/1/delete").status_code == 302
    with app.app_context():
        assert Album.query.count() == 3


def test_wrong_password(client):
    assert "Невірний логін або пароль" in login(client, "bad").get_data(as_text=True)


def test_create_edit_delete_album(client):
    assert "Ви увійшли" in login(client).get_data(as_text=True)

    r = client.post("/albums/new", data={"title": "Тестовий", "year": "2024",
                                         "tracks": "Пісня 1\nПісня 2"}, follow_redirects=True)
    assert "Альбом «Тестовий» додано" in r.get_data(as_text=True)
    with app.app_context():
        album = Album.query.filter_by(title="Тестовий").one()
        assert album.track_list == ["Пісня 1", "Пісня 2"]
        album_id = album.id

    r = client.post(f"/albums/{album_id}/edit", data={"title": "Оновлений", "year": "2025"},
                    follow_redirects=True)
    assert "Зміни збережено" in r.get_data(as_text=True)
    with app.app_context():
        assert db.session.get(Album, album_id).year == 2025

    r = client.post(f"/albums/{album_id}/delete", follow_redirects=True)
    assert "видалено" in r.get_data(as_text=True)
    with app.app_context():
        assert db.session.get(Album, album_id) is None


def test_validation(client):
    login(client)
    r = client.post("/albums/new", data={"title": "", "year": "abc"})
    text = r.get_data(as_text=True)
    assert "Назва альбому обов" in text and "Рік має бути" in text
    with app.app_context():
        assert Album.query.count() == 3
