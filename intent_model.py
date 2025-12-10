# intent_model.py

import os

from joblib import dump, load
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.metrics.pairwise import cosine_similarity

from config import VECTORIZER_PATH, TFIDF_TRANSFORMER_PATH
from nlp_utils import preprocess_text, create_stemmer_and_stopwords


def build_vectorizer_and_transformer(df):
    stemmer, stop_words = create_stemmer_and_stopwords()

    processed_questions = [
        preprocess_text(q, stemmer, stop_words) # stems and removes stopwords
        for q in df["Question"].astype(str)
    ]

    vectorizer = CountVectorizer()
    counts = vectorizer.fit_transform(processed_questions) # creates count vector

    transformer = TfidfTransformer(use_idf=True, sublinear_tf=True)
    corpus_tfidf = transformer.fit_transform(counts) # creates tf-idf vector

    dump(vectorizer, VECTORIZER_PATH)
    dump(transformer, TFIDF_TRANSFORMER_PATH)

    return vectorizer, transformer, corpus_tfidf


def load_vectorizer_and_transformer():
    if not (os.path.exists(VECTORIZER_PATH) and os.path.exists(TFIDF_TRANSFORMER_PATH)):
        return None, None
    vectorizer = load(VECTORIZER_PATH)
    transformer = load(TFIDF_TRANSFORMER_PATH)
    return vectorizer, transformer


def match_intent(user_input, vectorizer, transformer, corpus_tfidf, intents, stemmer, stop_words, threshold=0.15):

    processed = preprocess_text(user_input, stemmer, stop_words)
    counts = vectorizer.transform([processed])
    tfidf = transformer.transform(counts)

    sims = cosine_similarity(tfidf, corpus_tfidf)[0] # computes cosine similarity between user input and each row of corpus
    best_idx = sims.argmax() # index of best match
    best_score = sims[best_idx] # highest similarity score

    if best_score < threshold:
        return "unknown", best_idx, float(best_score)

    return intents[best_idx], best_idx, float(best_score)


# testing function
if __name__ == "__main__":

    from corpus import load_full_corpus
    from nlp_utils import create_stemmer_and_stopwords
    import pandas as pd

    df = load_full_corpus()

    vectorizer, transformer = load_vectorizer_and_transformer()
    if vectorizer is None or transformer is None:
        vectorizer, transformer, corpus_tfidf = build_vectorizer_and_transformer(df)
    else:
        stemmer, stop_words = create_stemmer_and_stopwords()
        processed_questions = [
            preprocess_text(q, stemmer, stop_words)
            for q in df["Question"].astype(str)
        ]
        counts = vectorizer.transform(processed_questions)
        corpus_tfidf = transformer.transform(counts)

    questions = df["Question"].astype(str).tolist()
    answers = df["Answer"].astype(str).tolist()
    intents = df["Intent"].tolist()

    stemmer, stop_words = create_stemmer_and_stopwords()

    while True:
        user_input = input("Test input: ").strip()
        if not user_input:
            continue

        intent, idx, score = match_intent(user_input,vectorizer,transformer,corpus_tfidf,intents,stemmer,stop_words,threshold=0.15)

        print(f"\nPredicted intent: {intent}")
        print(f"Matched example: \"{questions[idx]}\"")
        print(f"Similarity score: {score:.4f}\n")