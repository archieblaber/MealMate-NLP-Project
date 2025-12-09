# nlp_utils.py

import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer


def ensure_nltk():
    try:
        stopwords.words("english")
    except LookupError:
        nltk.download("stopwords")


def create_stemmer_and_stopwords():
    ensure_nltk()
    stemmer = PorterStemmer()
    stop_words = set(stopwords.words("english"))
    stop_words.discard("your")
    return stemmer, stop_words


def preprocess_text(text, stemmer, stop_words):
    text = text.lower()
    tokens = re.findall(r"[a-z]+", text)

    processed = [stemmer.stem(t) for t in tokens if t not in stop_words]

    if not processed and tokens:
        processed = [stemmer.stem(t) for t in tokens]

    return " ".join(processed)
