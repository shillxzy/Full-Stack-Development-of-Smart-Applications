"""Веб-додаток: аналіз тональності рецензій на фільми (IMDB).

Перед запуском навчіть модель: python train_model.py
Запуск: python app.py  ->  http://127.0.0.1:5000
"""
import pickle

from flask import Flask, render_template, request

from text_utils import clean_text

app = Flask(__name__)

with open("model.pkl", "rb") as f:
    model = pickle.load(f)
with open("vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)


def classify(text):
    """Повертає ('POSITIVE' | 'NEGATIVE', ймовірність позитиву у %)."""
    vector = vectorizer.transform([clean_text(text)])
    probability = float(model.predict_proba(vector)[0][1])
    label = "POSITIVE" if probability >= 0.5 else "NEGATIVE"
    return label, round(probability * 100, 1)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    text = request.form.get("message", "").strip()
    if not text:
        return render_template("index.html", error="Введіть текст рецензії англійською мовою.")
    result, positive = classify(text)
    confidence = positive if result == "POSITIVE" else round(100 - positive, 1)
    return render_template("index.html", message=text, result=result, confidence=confidence)


if __name__ == "__main__":
    app.run(debug=True)
