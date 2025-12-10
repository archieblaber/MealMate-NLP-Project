# handlers/handle_how_are_you.py

from nltk.sentiment import SentimentIntensityAnalyzer

def handle_how_are_you(state):

    print("MealMate: I'm doing great, thanks for asking! How are you feeling today?")

    user_reply = input(f"{state.username}: ").strip()

    sia = SentimentIntensityAnalyzer()
    sentiment = sia.polarity_scores(user_reply)

    compound = sentiment["compound"] # takes the compound score from the sentiment hashmap and uses it to assess sentiment

    # case that user sounds happy
    if compound >= 0.35:
        return f"That's great to hear {state.username}! If you want help finding a recipe or building your shopping list, I'm here!"
    
    # case that user sounds unhappy
    elif compound <= -0.35:
        return f"I'm really sorry you're feeling that way {state.username}. Hopefully I can make you feel better with some nice food!"

    # case that user sounds neutral
    else:
        return f"Thanks for sharing {state.username}. I'm here if you need anything, whether it's a recipe, a meal idea, or just a distraction."
