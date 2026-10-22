"""Консольна демонстрація тієї ж логіки тесту, що й у боті (без Telegram).

Корисно для перевірки й звіту, коли немає токена: питання виводяться
в консоль, номер варіанта вводиться з клавіатури (1-4).
"""
from quiz import QuizSession

session = QuizSession.create()
while not session.finished:
    q = session.current_question()
    print(f"\nПитання {session.current + 1}/{len(session.questions)}: {q.text}")
    for i, option in enumerate(q.options, 1):
        print(f"  {i}) {option}")
    choice = int(input("Ваша відповідь (1-4): ")) - 1
    ok, _ = session.answer(choice)
    print("✅ Правильно!" if ok else f"❌ Неправильно. Правильна: {q.options[q.correct_index]}")

print("\n" + session.report())
