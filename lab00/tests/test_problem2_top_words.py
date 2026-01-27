import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

import pathlib
from src.problem2_top_words import top_k_words

DATA = pathlib.Path(__file__).resolve().parents[1] / "data"

def load_stopwords() -> set[str]:
    return set((DATA / "stopwords.txt").read_text().split())

def test_top_k_words_basic():
    stop = load_stopwords()
    text = "Python, python, PYTHON! Data moves the world; data-driven models are everywhere."
    assert top_k_words(text, stop, k=3) == [("python", 3), ("data", 2), ("driven", 1)]

def test_top_k_words_tie_break_alpha():
    stop = load_stopwords()
    text = "alpha beta beta gamma gamma"
    assert top_k_words(text, stop, k=2) == [("beta", 2), ("gamma", 2)]

def test_top_k_words_stopwords_removed():
    stop = load_stopwords()
    text = "The the the data in the world"
    assert top_k_words(text, stop, k=3) == [("data", 1), ("world", 1)]
