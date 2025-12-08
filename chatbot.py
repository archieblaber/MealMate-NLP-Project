# chatbot.py

import random

from state import ConversationState
from corpus import load_full_corpus
from handlers.handle_recipe_search_ingredient import handle_recipe_search_ingredient
from handlers.handle_recipe_details import handle_recipe_details
from handlers.handle_recipe_more import handle_recipe_more
from handlers.handle_shopping_add import handle_shopping_add
from handlers.handle_shopping_show import handle_shopping_show
from handlers.handle_shopping_clear import handle_shopping_clear
from handlers.handle_shopping_remove import handle_shopping_remove
from handlers.handle_help import handle_help
from handlers.handle_shopping_place_order import handle_shopping_place_order
from recipe_manager import RecipeManager
from smalltalk_intents import SMALLTALK_TEMPLATES
from nlp_utils import create_stemmer_and_stopwords, ensure_nltk, preprocess_text
from intent_model import (
    build_vectorizer_and_transformer,
    load_vectorizer_and_transformer,
    match_intent,
)


def main():
    # Load small talk corpus
    df = load_full_corpus()
    state = ConversationState()
    recipe_manager = RecipeManager("recipes.csv")

    # Build or load vectoriser/transformer
    vectorizer, transformer = load_vectorizer_and_transformer()
    if vectorizer is None or transformer is None:
        vectorizer, transformer, corpus_tfidf = build_vectorizer_and_transformer(df)
    else:
        # Need to rebuild corpus_tfidf from the current corpus
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

    # NLP tools for runtime
    stemmer, stop_words = create_stemmer_and_stopwords()

    # Username handshake
    print("Hi, I'm the skeleton small talk chatbot.")

    while state.username is None:
        name_try = input("What should I call you? ").strip()
        if not name_try:
            print("I didn't catch that, try again.")
            continue
        confirm = input(f"Did you say '{name_try}'? (y/n) ").strip().lower()
        if confirm in ("y", "yes"):
            state.username = name_try
        else:
            print("Okay, let's try again.")

    print(f"Nice to meet you, {state.username}!")
    print("Right now I can have small talk. Ask me something (type 'quit' to exit).")

    # Main chat loop
    while True:
        user_input = input(f"{state.username}: ").strip()
        if not user_input:
            continue

        if user_input.lower() in {"quit", "exit", "bye"}:
            print("MealMate: Goodbye!")
            break

        intent, idx, score = match_intent(
            user_input,
            vectorizer,
            transformer,
            corpus_tfidf,
            intents,
            stemmer,
            stop_words,
        )

        # proto_q = questions[idx]
        # print(f"[DEBUG] intent={intent}  score={score:.3f}")
        # print(f"[DEBUG] matched prototype: \"{proto_q}\"")

        if intent == "unknown":
            print("MealMate: I'm not confident I understand that yet.")
            continue

        state.last_intent = intent

        # Use templates if we have them
        if intent in SMALLTALK_TEMPLATES:
            template = random.choice(SMALLTALK_TEMPLATES[intent])
            response = template.replace("{name}", state.username)
            print("MealMate:", response)
            continue
        
        if intent == "recipe_search_ingredient":
            response = handle_recipe_search_ingredient(user_input, state, recipe_manager)
            print("MealMate:", response)
            continue

        if intent == "recipe_details":
            response = handle_recipe_details(state, recipe_manager)
            print("MealMate:", response)
            continue

        if intent == "recipe_more":
            response = handle_recipe_more(state, recipe_manager)
            print("MealMate:", response)
            continue
        
        if intent == "shopping_add":
            response = handle_shopping_add(user_input, state, recipe_manager)
            print("MealMate:", response)
            continue
        if intent == "shopping_remove":
            response = handle_shopping_remove(user_input, state)
            print("MealMate:", response)
            continue
        if intent == "shopping_show":
            response = handle_shopping_show(state)
            print("MealMate:", response)
            continue
        if intent == "shopping_clear":
            response = handle_shopping_clear(state)
            print("MealMate:", response)
            continue
        if intent == "shopping_place_order":
            response = handle_shopping_place_order(state)
            print("MealMate:", response)
            continue
        if intent == "help":
            response = handle_help(state)
            print("MealMate:", response)
            continue

        # Fallback to default answer from datasety
        print("MealMate:", answers[idx])


if __name__ == "__main__":
    main()
