"""Тести логіки тесту (без звернень до Telegram)."""
import random

from questions import QUESTIONS
from quiz import QUESTIONS_PER_TEST, QuizSession


def test_bank_is_valid():
    assert len(QUESTIONS) >= QUESTIONS_PER_TEST
    for text, options in QUESTIONS:
        assert len(options) == 4 and len(set(options)) == 4, text


def test_session_has_10_unique_questions():
    s = QuizSession.create()
    assert len(s.questions) == 10
    assert len({q.text for q in s.questions}) == 10


def test_correct_option_tracked_after_shuffle():
    correct = dict(QUESTIONS)
    s = QuizSession.create()
    for q in s.questions:
        assert q.options[q.correct_index] == correct[q.text][0]
        assert sorted(q.options) == sorted(correct[q.text])


def test_order_is_random_between_runs():
    orders = {tuple(q.text for q in QuizSession.create(random.Random(seed)).questions) for seed in range(5)}
    assert len(orders) > 1


def test_full_run_scoring_and_report():
    s = QuizSession.create(random.Random(1))
    for i, q in enumerate(s.questions):
        # перші 7 - правильно, решта - неправильно
        s.answer(q.correct_index if i < 7 else (q.correct_index + 1) % 4)
    assert s.finished and s.score == 7
    report = s.report()
    assert "Бали: 7 з 10" in report and "Дата:" in report and "Тривалість:" in report
    assert report.count("✅") == 7 and report.count("❌") == 3
