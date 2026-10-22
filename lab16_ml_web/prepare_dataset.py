"""Готує файл IMDB Dataset.csv (50 000 рецензій) у форматі датасету з Kaggle
(lakshmi25npathi/imdb-dataset-of-50k-movie-reviews): стовпці review, sentiment.

Джерело - оригінальний набір Large Movie Review Dataset (Maas et al., 2011),
опублікований на Hugging Face як stanfordnlp/imdb. Скрипт потрібен, лише якщо
немає доступу до Kaggle; інакше просто покладіть завантажений CSV поруч.
"""
import pandas as pd
from datasets import load_dataset

ds = load_dataset("stanfordnlp/imdb")
frames = [ds[split].to_pandas() for split in ("train", "test")]
df = pd.concat(frames, ignore_index=True)
df["sentiment"] = df["label"].map({0: "negative", 1: "positive"})
df = df[["text", "sentiment"]].rename(columns={"text": "review"})
df = df.sample(frac=1, random_state=42).reset_index(drop=True)   # перемішуємо
df.to_csv("IMDB Dataset.csv", index=False)
print(df.shape, df["sentiment"].value_counts().to_dict())
