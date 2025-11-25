# intent_model.py

import os

from joblib import dump, load
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.metrics.pairwise import cosine_similarity

from config import VECTORIZER_PATH, TFIDF_TRANSFORMER_PATH
from nlp_utils import preprocess_text, create_stemmer_and_stopwords


def build_vectorizer_and_transformer(df):
    """
    Build CountVectorizer + TfidfTransformer on the smalltalk corpus.
    Save them via joblib.
    Returns:
        vectorizer, transformer, corpus_tfidf
    """
    stemmer, stop_words = create_stemmer_and_stopwords()

    processed_questions = [
        preprocess_text(q, stemmer, stop_words)
        for q in df["Question"].astype(str)
    ]

    vectorizer = CountVectorizer()
    counts = vectorizer.fit_transform(processed_questions)

    transformer = TfidfTransformer(use_idf=True, sublinear_tf=True)
    corpus_tfidf = transformer.fit_transform(counts)

    dump(vectorizer, VECTORIZER_PATH)
    dump(transformer, TFIDF_TRANSFORMER_PATH)

    return vectorizer, transformer, corpus_tfidf


def load_vectorizer_and_transformer():
    """
    Load previously saved vectoriser and transformer.
    Returns (vectorizer, transformer) or (None, None) if missing.
    """
    if not (os.path.exists(VECTORIZER_PATH) and os.path.exists(TFIDF_TRANSFORMER_PATH)):
        return None, None
    vectorizer = load(VECTORIZER_PATH)
    transformer = load(TFIDF_TRANSFORMER_PATH)
    return vectorizer, transformer


def match_intent(
    user_input,
    vectorizer,
    transformer,
    corpus_tfidf,
    intents,
    stemmer,
    stop_words,
    threshold=0.15,
):
    """
    Vectorise user input with existing vectoriser + transformer
    and compute cosine similarity against the full corpus.
    Returns (intent, best_index, score) or ("unknown", ...)
    """
    processed = preprocess_text(user_input, stemmer, stop_words)
    counts = vectorizer.transform([processed])
    tfidf = transformer.transform(counts)

    sims = cosine_similarity(tfidf, corpus_tfidf)[0]
    best_idx = sims.argmax()
    best_score = sims[best_idx]

    if best_score < threshold:
        return "unknown", best_idx, float(best_score)

    return intents[best_idx], best_idx, float(best_score)
