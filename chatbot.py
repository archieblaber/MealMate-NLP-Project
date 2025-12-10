# chatbot.py

import random
import nltk


from state import ConversationState
from corpus import load_full_corpus
from handlers.handle_recipe_search_ingredient import handle_recipe_search_ingredient
from handlers.handle_recipe_details import handle_recipe_details
from handlers.handle_recipe_more import handle_recipe_more
from handlers.handle_shopping_add import handle_shopping_add
from handlers.handle_shopping_show import handle_shopping_show
from handlers.handle_shopping_clear import handle_shopping_clear
from handlers.handle_shopping_remove import handle_shopping_remove
from handlers.handle_how_are_you import handle_how_are_you
from handlers.handle_add_dislike import handle_add_dislike
from handlers.handle_set_diet import handle_set_diet
from handlers.handle_recipe_search_cuisine import handle_recipe_search_cuisine
from handlers.handle_recipe_search_quick import handle_recipe_search_quick
from handlers.handle_help import handle_help
from handlers.handle_shopping_place_order import handle_shopping_place_order
from handlers.handle_show_prefs import handle_show_prefs
from recipe_manager import RecipeManager
from smalltalk_intents import SMALLTALK_TEMPLATES
from nlp_utils import create_stemmer_and_stopwords, ensure_nltk, preprocess_text
from intent_model import (
    build_vectorizer_and_transformer,
    load_vectorizer_and_transformer,
    match_intent,
)

nltk.download("vader_lexicon")


def main():
    df = load_full_corpus()
    LOW_CONF_THRESHOLD = 0.6 # threshold under which clarification will be needed
    state = ConversationState()
    recipe_manager = RecipeManager("recipes.csv")

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

    print("Hi, I'm MealMate - your recipe and shopping assistant.")

    while state.username is None:
        name_try = input("MealMate: What should I call you? ").strip()
        if not name_try:
            print("MealMate: I didn't catch that, try again.")
            continue
        confirm = input(f"MealMate: Did you say '{name_try}'? (y/n) ").strip().lower()
        if confirm in ("y", "yes"):
            state.username = name_try
        else:
            print("MealMate: Okay, let's try again.")

    print(f"MealMate: Nice to meet you, {state.username}!")
    print(
        "MealMate: Here's what I can help you with:\n"
        "- Find recipes based on ingredients, cuisine, diet, or cooking time.\n"
        "- Show more details for a recipe and give you personalised notes.\n"
        "- Remember your dietary preferences (e.g. vegan, gluten free).\n"
        "- Remember ingredients you dislike and avoid them in suggestions.\n"
        "- Build, show, update, and clear a shopping list from recipes or free-form items.\n"
        "- Do a bit of small talk (hello, how are you, etc.).\n"
        "\nYou can try asking things like:\n"
        '  - "show me some quick recipes"\n'
        '  - "what can I cook with chicken"\n'
        '  - "add that recipe to my shopping list"\n'
        '  - "what are my dietary preferences"\n'
        "\nType \"help\" at any time to see this again, or \"quit\" to exit."
    )

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

        if intent == "unknown":
            print("MealMate: I'm not confident I understand that yet.\n"
                  "\nYou can try asking things like:\n"
        '  - "show me some quick recipes"\n'
        '  - "what can I cook with chicken"\n'
        '  - "add that recipe to my shopping list"\n'
        '  - "what are my dietary preferences"\n'
            )
            continue

        # clarify what the user meant, score value is between 0.15 and 0.6
        if score < LOW_CONF_THRESHOLD:
            guess_text = questions[idx]
            print(
                f"MealMate: I'm not completely sure what you meant.\n"
                f"My best guess is something like: \"{guess_text}\" "
            )
            confirm = input("MealMate: Should I go ahead with this? (y/n) ").strip().lower()
            if confirm not in ("y", "yes"):
                print("MealMate: Okay, please rephrase your request or try a different wording.")
                continue

        state.last_intent = intent

        # match intents with handlers:
        if intent in SMALLTALK_TEMPLATES:
            if intent == "my_name_is":
                state.username = user_input.split()[-1]
            if intent == "how_are_you":
                response = handle_how_are_you(state)
                print("MealMate:", response)
                continue
            template = random.choice(SMALLTALK_TEMPLATES[intent])
            response = template.replace("{name}", state.username)
            print("MealMate:", response)
            continue
        
        if intent == "recipe_search_ingredient":
            response = handle_recipe_search_ingredient(user_input, state, recipe_manager)
            print("MealMate:", response)
            continue
        if intent == "recipe_search_cuisine":
            response = handle_recipe_search_cuisine(user_input, state, recipe_manager)
            print("MealMate:", response)
            continue
        if intent == "recipe_search_quick":
            response = handle_recipe_search_quick(user_input, state, recipe_manager)
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
        if intent == "add_dislike":
            response = handle_add_dislike(user_input, state)
            print("MealMate:", response)
            continue
        if intent == "show_prefs":
            response = handle_show_prefs(state)
            print("MealMate:", response)
            continue
        if intent == "set_diet":
            response = handle_set_diet(user_input, state)
            print("MealMate:", response)
            continue
        if intent == "change_name":
            response = handle_change_name(user_input, state)
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
