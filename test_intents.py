import csv
from collections import Counter

from corpus import load_full_corpus
from intent_model import (
    build_vectorizer_and_transformer,
    load_vectorizer_and_transformer,
    match_intent,
)
from nlp_utils import create_stemmer_and_stopwords, preprocess_text


def load_model_and_corpus():
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
    return vectorizer, transformer, corpus_tfidf, intents, stemmer, stop_words


def load_test_cases(path="intent_test_500.csv"):
    cases = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cases.append((row["utterance"], row["expected_intent"]))
    return cases


def main():
    vectorizer, transformer, corpus_tfidf, intents, stemmer, stop_words = (
        load_model_and_corpus()
    )
    cases = load_test_cases()

    correct = 0
    per_intent = Counter()
    per_intent_correct = Counter()

    print("Running intent classification tests on 155 utterances...\n")

    for utterance, expected in cases:
        predicted, idx, score = match_intent(
            utterance,
            vectorizer,
            transformer,
            corpus_tfidf,
            intents,
            stemmer,
            stop_words,
        )

        ok = predicted == expected
        if ok:
            correct += 1
            per_intent_correct[expected] += 1
        per_intent[expected] += 1

        # Optional: comment this out if too spammy
        # status = "OK " if ok else "ERR"
        # print(f"[{status}] '{utterance}' -> predicted={predicted}, "
        #       f"expected={expected}, score={score:.3f}")

    total = len(cases)
    overall_acc = correct / total if total else 0.0
    print("\nSummary")
    print("-------")
    print(f"Total test cases: {total}")
    print(f"Correct predictions: {correct}")
    print(f"Overall accuracy: {overall_acc:.2%}\n")

    print("Per-intent accuracy:")
    for intent in sorted(per_intent.keys()):
        n = per_intent[intent]
        c = per_intent_correct[intent]
        acc = c / n if n else 0.0
        print(f"- {intent:25s}: {c:3d}/{n:3d} = {acc:.2%}")


if __name__ == "__main__":
    main()
