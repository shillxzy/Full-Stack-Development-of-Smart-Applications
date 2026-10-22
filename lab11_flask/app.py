"""Лабораторна робота №11. Сайт музичного гурту на Flask.

Сторінки: Головна, Про проект, Історія гурту, список і сторінки альбомів.
Авторизовані користувачі можуть додавати, редагувати й видаляти альбоми.

Локальний запуск:   flask --app app run   (або python app.py)
Створити адміністратора:  flask --app app create-user <логін>
"""
import os

import click
from flask import Flask, abort, flash, redirect, render_template, request, url_for
from flask_login import (LoginManager, UserMixin, current_user, login_required,
                         login_user, logout_user)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")

# Heroku Postgres видає адресу з префіксом postgres://, а SQLAlchemy 1.4+
# очікує postgresql:// - виправляємо. Локально використовується SQLite.
db_url = os.environ.get("DATABASE_URL", "sqlite:///band.db")
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = db_url

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message = "Увійдіть, щоб керувати альбомами."


# ---------------------------- Моделі ----------------------------
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    cover_url = db.Column(db.String(500))
    description = db.Column(db.Text, default="")
    tracks = db.Column(db.Text, default="")   # одна пісня на рядок

    @property
    def track_list(self):
        return [t.strip() for t in self.tracks.splitlines() if t.strip()]


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


# ---------------------------- Сторінки ----------------------------
@app.route("/")
def index():
    latest = Album.query.order_by(Album.year.desc()).limit(3).all()
    return render_template("index.html", latest=latest)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/history")
def history():
    return render_template("history.html")


@app.route("/albums")
def albums():
    return render_template("albums.html", albums=Album.query.order_by(Album.year).all())


@app.route("/albums/<int:album_id>")
def album_detail(album_id):
    return render_template("album.html", album=db.get_or_404(Album, album_id))


# ---------------------------- CRUD альбомів ----------------------------
def album_from_form(album):
    """Заповнює альбом даними форми; повертає список помилок валідації."""
    errors = []
    title = request.form.get("title", "").strip()
    year = request.form.get("year", "").strip()
    if not title:
        errors.append("Назва альбому обов'язкова.")
    if not year.isdigit() or not 1950 <= int(year) <= 2100:
        errors.append("Рік має бути числом від 1950 до 2100.")
    if errors:
        return errors
    album.title = title
    album.year = int(year)
    album.cover_url = request.form.get("cover_url", "").strip() or None
    album.description = request.form.get("description", "").strip()
    album.tracks = request.form.get("tracks", "").strip()
    return []


@app.route("/albums/new", methods=["GET", "POST"])
@login_required
def album_create():
    album = Album()
    if request.method == "POST":
        errors = album_from_form(album)
        if not errors:
            db.session.add(album)
            db.session.commit()
            flash(f"Альбом «{album.title}» додано.", "success")
            return redirect(url_for("album_detail", album_id=album.id))
        for e in errors:
            flash(e, "danger")
    return render_template("album_form.html", album=album, form=request.form, is_new=True)


@app.route("/albums/<int:album_id>/edit", methods=["GET", "POST"])
@login_required
def album_edit(album_id):
    album = db.get_or_404(Album, album_id)
    if request.method == "POST":
        errors = album_from_form(album)
        if not errors:
            db.session.commit()
            flash("Зміни збережено.", "success")
            return redirect(url_for("album_detail", album_id=album.id))
        db.session.rollback()
        for e in errors:
            flash(e, "danger")
    return render_template("album_form.html", album=album, form=request.form, is_new=False)


@app.route("/albums/<int:album_id>/delete", methods=["POST"])
@login_required
def album_delete(album_id):
    album = db.get_or_404(Album, album_id)
    db.session.delete(album)
    db.session.commit()
    flash(f"Альбом «{album.title}» видалено.", "info")
    return redirect(url_for("albums"))


# ---------------------------- Авторизація ----------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(username=request.form.get("username", "")).first()
        if user and user.check_password(request.form.get("password", "")):
            login_user(user)
            flash("Ви увійшли.", "success")
            next_url = request.args.get("next", "")
            # Дозволяємо перенаправлення лише на внутрішні сторінки сайту.
            return redirect(next_url if next_url.startswith("/") and not next_url.startswith("//")
                            else url_for("index"))
        flash("Невірний логін або пароль.", "danger")
    return render_template("login.html")


@app.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    flash("Ви вийшли.", "info")
    return redirect(url_for("index"))


@app.errorhandler(404)
def not_found(_):
    return render_template("404.html"), 404


# ---------------------------- Ініціалізація ----------------------------
SEED_ALBUMS = [
    dict(title="Перший сніг", year=2016,
         description="Дебютна платівка, записана у репетиційній кімнаті на Подолі.",
         tracks="Перший сніг\nНічний трамвай\nДовгі листи\nПісля дощу\nДім"),
    dict(title="Світло на воді", year=2019,
         description="Другий альбом: більше синтезаторів і мелодій, натхненних Дніпром.",
         tracks="Світло на воді\nВідлуння\nЛіхтарі\nНе відпускай\nОстанній паром\nТиша"),
    dict(title="Дорога додому", year=2023,
         description="Найособистіший альбом гурту про повернення та підтримку.",
         tracks="Дорога додому\nЗоряний пил\nМи разом\nПтахи\nСвітанок"),
]


def seed():
    """Створює таблиці й початкові альбоми, якщо база порожня."""
    db.create_all()
    if Album.query.count() == 0:
        db.session.add_all(Album(**a) for a in SEED_ALBUMS)
        db.session.commit()


@app.cli.command("create-user")
@click.argument("username")
@click.password_option()
def create_user(username, password):
    """Створити користувача, що може керувати альбомами."""
    seed()
    if User.query.filter_by(username=username).first():
        raise click.ClickException("Такий користувач уже існує")
    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    click.echo(f"Користувача {username} створено.")


with app.app_context():
    seed()

if __name__ == "__main__":
    app.run(debug=True)
