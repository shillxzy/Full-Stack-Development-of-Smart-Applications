"""Навчання моделі класифікації рецензій IMDB (позитивна / негативна).

Результат: model.pkl, vectorizer.pkl, metrics.txt, confusion_matrix.png.
"""
import pickle

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import ConfusionMatrixDisplay, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

from text_utils import clean_text

# 1. Завантаження датасету: review - текст, sentiment - positive/negative.
df = pd.read_csv("IMDB Dataset.csv")
df.columns = ["message", "label"]
df["label"] = (df["label"] == "positive").astype(int)    # 1 - позитивна, 0 - негативна
print("Розмір датасету:", df.shape)
print("Розподіл класів:", df["label"].value_counts().to_dict())

df["message"] = df["message"].apply(clean_text)

# 2. Розбиття на train/test (80/20); stratify зберігає пропорцію класів.
X_train, X_test, y_train, y_test = train_test_split(
    df["message"], df["label"], test_size=0.2, random_state=42, stratify=df["label"]
)

# 3. Векторизація TF-IDF (слова та біграми, щоб враховувати "not good").
vectorizer = TfidfVectorizer(stop_words=None, ngram_range=(1, 2), min_df=5, max_features=200_000,
                             sublinear_tf=True)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)
print("Кількість ознак (слів і біграм):", X_train_vec.shape[1])

# 4. Навчання логістичної регресії та оцінка якості.
model = LogisticRegression(max_iter=1000, C=4)
model.fit(X_train_vec, y_train)
y_pred = model.predict(X_test_vec)

accuracy = model.score(X_test_vec, y_test)
report = classification_report(y_test, y_pred, target_names=["negative", "positive"], digits=4)
print("Accuracy:", round(accuracy, 4))
print(report)

# Найвагоміші слова для кожного класу - щоб пояснити, як "думає" модель.
names = vectorizer.get_feature_names_out()
order = model.coef_[0].argsort()
top_neg = ", ".join(names[order[:15]])
top_pos = ", ".join(names[order[-15:][::-1]])
print("Найсильніші ознаки негативу:", top_neg)
print("Найсильніші ознаки позитиву:", top_pos)

with open("metrics.txt", "w", encoding="utf-8") as f:
    f.write(f"Train: {len(X_train)}, test: {len(X_test)}, ознак: {X_train_vec.shape[1]}\n")
    f.write(f"Accuracy: {accuracy:.4f}\n\n{report}\n")
    f.write(f"Ознаки негативу: {top_neg}\nОзнаки позитиву: {top_pos}\n")

cm = confusion_matrix(y_test, y_pred)
ConfusionMatrixDisplay(cm, display_labels=["negative", "positive"]).plot(cmap="Blues", values_format="d")
plt.title(f"Матриця помилок (accuracy = {accuracy:.4f})")
plt.tight_layout()
plt.savefig("confusion_matrix.png", dpi=110)

# 5. Збереження моделі та векторизатора.
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)
with open("vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)
print("Модель і векторизатор збережено!")
