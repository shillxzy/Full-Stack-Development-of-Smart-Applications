# Додає до sys.path каталог з кодом, що тестується: за замовчуванням - поточна
# (виправлена) версія; LAB10_SRC=initial_version - початкова версія класів.
import os
import sys
from pathlib import Path

BASE = Path(__file__).parent
sys.path.insert(0, str(BASE / os.environ.get("LAB10_SRC", ".")))
