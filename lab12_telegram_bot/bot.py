"""Лабораторна робота №12. Telegram-бот: тест з 10 питань про Python.

Токен бота (отримати у @BotFather) передається через змінну середовища
BOT_TOKEN або файл .env поруч зі скриптом з рядком BOT_TOKEN=...
Запуск: python bot.py
"""
import os
from pathlib import Path

import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from quiz import QuizSession


def load_env_file(path=Path(__file__).parent / ".env"):
    """Читає пари KEY=VALUE з .env, не перезаписуючи вже задані змінні середовища."""
    if path.exists():
        for line in path.read_text(encoding="utf-8-sig").splitlines():
            key, sep, value = line.partition("=")
            if sep and not line.lstrip().startswith("#"):
                os.environ.setdefault(key.strip(), value.strip().strip('"'))


load_env_file()
TOKEN = os.environ.get("BOT_TOKEN")
if not TOKEN:
    raise SystemExit("Задайте змінну середовища BOT_TOKEN з токеном від @BotFather")

bot = telebot.TeleBot(TOKEN)
sessions = {}   # chat_id -> QuizSession; кожен користувач проходить свій тест


def question_keyboard(question, number):
    """Кнопки з варіантами; у callback_data - номер питання і варіанта."""
    markup = InlineKeyboardMarkup(row_width=1)
    for i, option in enumerate(question.options):
        markup.add(InlineKeyboardButton(option, callback_data=f"{number}:{i}"))
    return markup


def send_question(chat_id):
    session = sessions[chat_id]
    q = session.current_question()
    number = session.current
    bot.send_message(chat_id, f"Питання {number + 1}/{len(session.questions)}\n\n{q.text}",
                     reply_markup=question_keyboard(q, number))


@bot.message_handler(commands=["start"])
def start(message):
    sessions[message.chat.id] = QuizSession.create()
    bot.send_message(message.chat.id,
                     "Привіт! Це тест з Python: 10 питань, по 4 варіанти відповіді.\n"
                     "Питання й варіанти щоразу перемішуються. Почнемо!")
    send_question(message.chat.id)


@bot.message_handler(commands=["help"])
def help_command(message):
    bot.send_message(message.chat.id, "/start - почати тест заново")


@bot.callback_query_handler(func=lambda call: True)
def handle_answer(call):
    chat_id = call.message.chat.id
    session = sessions.get(chat_id)
    number, option = map(int, call.data.split(":"))
    # Ігноруємо натискання на кнопки старих питань або завершеного тесту.
    if session is None or session.finished or number != session.current:
        bot.answer_callback_query(call.id, "Це питання вже неактуальне. /start - новий тест")
        return

    is_correct, question = session.answer(option)
    verdict = "✅ Правильно!" if is_correct else (
        f"❌ Неправильно. Правильна відповідь: {question.options[question.correct_index]}")
    bot.answer_callback_query(call.id, "Правильно!" if is_correct else "Неправильно")
    # Прибираємо кнопки і дописуємо вибір та вердикт під питанням.
    bot.edit_message_text(f"{call.message.text}\n\nВаша відповідь: {question.options[option]}\n{verdict}",
                          chat_id, call.message.message_id)

    if session.finished:
        bot.send_message(chat_id, session.report())
        bot.send_message(chat_id, "Щоб пройти тест ще раз, надішліть /start")
    else:
        send_question(chat_id)


if __name__ == "__main__":
    print("Бот запущено. Натисніть Ctrl+C для зупинки.")
    bot.infinity_polling()
