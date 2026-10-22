"""Логіка тесту, незалежна від Telegram (її легко перевірити тестами)."""
import random
from dataclasses import dataclass, field
from datetime import datetime

from questions import QUESTIONS

QUESTIONS_PER_TEST = 10


@dataclass
class Question:
    text: str
    options: list          # варіанти в перемішаному порядку
    correct_index: int


@dataclass
class QuizSession:
    questions: list
    started_at: datetime = field(default_factory=datetime.now)
    current: int = 0
    answers: list = field(default_factory=list)   # (питання, обраний індекс, чи правильно)
    finished_at: datetime | None = None

    @classmethod
    def create(cls, rng=random):
        """Випадкові 10 питань у випадковому порядку з перемішаними варіантами."""
        questions = []
        for text, options in rng.sample(QUESTIONS, QUESTIONS_PER_TEST):
            shuffled = options[:]
            rng.shuffle(shuffled)
            questions.append(Question(text, shuffled, shuffled.index(options[0])))
        return cls(questions)

    @property
    def finished(self):
        return self.current >= len(self.questions)

    def current_question(self):
        return None if self.finished else self.questions[self.current]

    def answer(self, option_index):
        """Фіксує відповідь на поточне питання; повертає (правильно?, питання)."""
        question = self.current_question()
        if question is None:
            raise RuntimeError("Тест уже завершено")
        is_correct = option_index == question.correct_index
        self.answers.append((question, option_index, is_correct))
        self.current += 1
        if self.finished:
            self.finished_at = datetime.now()
        return is_correct, question

    @property
    def score(self):
        return sum(1 for *_, ok in self.answers if ok)

    def duration_text(self):
        seconds = int(((self.finished_at or datetime.now()) - self.started_at).total_seconds())
        minutes, seconds = divmod(seconds, 60)
        return f"{minutes} хв {seconds} с"

    def report(self):
        lines = [
            "📋 Результати тесту з Python",
            f"Бали: {self.score} з {len(self.questions)}",
            f"Дата: {self.started_at:%d.%m.%Y %H:%M}",
            f"Тривалість: {self.duration_text()}",
            "",
        ]
        for i, (q, chosen, ok) in enumerate(self.answers, 1):
            mark = "✅" if ok else "❌"
            line = f"{i}. {mark} {q.text}\n   Ваша відповідь: {q.options[chosen]}"
            if not ok:
                line += f"\n   Правильна: {q.options[q.correct_index]}"
            lines.append(line)
        return "\n".join(lines)
