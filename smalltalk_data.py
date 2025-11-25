# smalltalk_data.py

import pandas as pd

# Small talk templates used at response-time
SMALLTALK_TEMPLATES = {
    "greeting": [
        "Hello!",
        "Hi there!",
        "Hey! How can I help?",
        "Nice to see you, {name}!"
    ],
    "how_are_you": [
        "I'm just code, but I'm running great.",
        "I'm doing well! Ready to help.",
        "All good on my side, thanks for asking!"
    ],
    "thanks": [
        "You're welcome!",
        "Anytime!",
        "No problem at all."
    ],
    "what_can_you_do": [
        "Right now I can have small talk, and soon I’ll help you with meal planning and recipes.",
        "I support small talk for now, and I’ll later help with recipes and shopping lists.",
        "At the moment I just do chit-chat, but I’m being upgraded into a meal assistant."
    ],
    "what_is_my_name": [
        "Your name is {name}.",
        "You told me you are {name}.",
        "Of course, you’re {name}!"
    ],
    "what_is_your_name": [
        "I'm the skeleton chatbot!",
        "My name is Skeleton Chatbot.",
        "You can call me the skeleton chatbot."
    ],
}


def build_smalltalk_dataframe():
    """
    Build a small talk corpus as a DataFrame with:
    - Question: prototype user utterance
    - Answer: a default answer (used only as fallback)
    - Intent: intent label used for matching + templates
    """
    rows = [
        {
            "Question": "hello",
            "Answer": "Hello! How can I help you today?",
            "Intent": "greeting",
        },
        {
            "Question": "hi",
            "Answer": "Hi there!",
            "Intent": "greeting",
        },
        {
            "Question": "hey",
            "Answer": "Hey!",
            "Intent": "greeting",
        },
        {
            "Question": "how are you",
            "Answer": "I'm doing well, thanks!",
            "Intent": "how_are_you",
        },
        {
            "Question": "thank you",
            "Answer": "You're welcome!",
            "Intent": "thanks",
        },
        {
            "Question": "thanks",
            "Answer": "No worries!",
            "Intent": "thanks",
        },
        {
            "Question": "what can you do",
            "Answer": "I can do small talk.",
            "Intent": "what_can_you_do",
        },
        {
            "Question": "what is my name",
            "Answer": "You told me your name earlier.",
            "Intent": "what_is_my_name",
        },
        {
            "Question": "what is your name",
            "Answer": "I'm the skeleton chatbot!",
            "Intent": "what_is_your_name",
        },
    ]

    return pd.DataFrame(rows)


def load_corpus():
    """
    For now, our entire corpus is just the small talk dataset.
    (No external QA CSV.)
    """
    df = build_smalltalk_dataframe()
    return df
