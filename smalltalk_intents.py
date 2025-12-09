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
    "what_is_my_name": [
        "Your name is {name}.",
        "You told me you are {name}.",
        "Of course, you're {name}!"
    ],
    "what_is_your_name": [
        "I'm the skeleton chatbot!",
        "My name is Skeleton Chatbot.",
        "You can call me the skeleton chatbot."
    ],
    "my_name_is": [
        "Alright, I will call you {name}!"
    ]
}


def build_smalltalk_dataframe():
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
            "Question": "what is my name",
            "Answer": "You told me your name earlier.",
            "Intent": "what_is_my_name",
        },
        {
            "Question": "what is your name",
            "Answer": "I'm the skeleton chatbot!",
            "Intent": "what_is_your_name",
        },
        {
            "Question": "call me ",
            "Answer": "",
            "Intent": "my_name_is",
        },
    ]

    return pd.DataFrame(rows)


def load_corpus():
    df = build_smalltalk_dataframe()
    return df
