# recipe_detail_notes.py

import random

# varied notes for responses for lexical variation

TAG_NOTE_OPTIONS = {
    "high protein": [
        "It's a great choice if you're looking to boost protein.",
        "Perfect if you want something protein-rich.",
        "A strong option for keeping your protein intake high."
    ],
    "low carb": [
        "Ideal if you're keeping your carb intake low.",
        "A fitting option for low-carb eating.",
        "Good pick if you're reducing carbohydrates."
    ],
    "vegetarian": [
        "A solid vegetarian-friendly dish.",
        "Perfect if you're avoiding meat.",
        "A nice option for plant-focused eating."
    ],
    "vegan": [
        "Completely plant-based and vegan-friendly.",
        "Suitable if you avoid all animal products.",
        "A strong vegan option to consider."
    ],
    "gluten free": [
        "Suitable if you need to avoid gluten.",
        "A dependable choice for gluten-free eating.",
        "Ideal if you're steering clear of gluten."
    ],
    "default": [
        "A flexible dish that suits many preferences.",
        "A general-purpose meal most people enjoy.",
        "A versatile recipe that fits a range of diets."
    ]
}

DIFFICULTY_NOTE_OPTIONS = {
    "easy": [
        "Straightforward and beginner-friendly.",
        "Simple to prepare with minimal hassle.",
        "Great for someone who wants an easy cook."
    ],
    "medium": [
        "Requires some attention but nothing challenging.",
        "A balanced recipe that takes a bit of focus.",
        "Good for cooks comfortable with a little prep."
    ],
    "hard": [
        "Best suited for confident cooks.",
        "More involved and rewarding if you enjoy a challenge.",
        "Ideal for someone who likes a more technical recipe."
    ],
    "default": [
        "Manageable for most home cooks.",
        "Accessible regardless of skill level.",
        "Comfortable for a wide range of cooking ability."
    ]
}

TIME_NOTE_OPTIONS = [
    (20, [
        "Perfect when you want something fast.",
        "Ideal for a quick meal with little waiting.",
        "Great if you don't have much time to cook."
    ]),
    (40, [
        "A comfortable cooking time for most evenings.",
        "Great for a relaxed weekday dinner.",
        "Good when you don't want to rush or take too long."
    ]),
    (9999, [
        "Ideal for when you prefer an unhurried cook.",
        "Perfect for a slower weekend meal.",
        "Great if you enjoy spending more time in the kitchen."
    ])
]


def build_recipe_notes(row):
    notes = []

    tags = str(row["tags"]).lower()
    difficulty = str(row["difficulty"]).lower()
    time_min = int(row["time_to_cook_min"])

    tag_key = "default"
    for key in TAG_NOTE_OPTIONS.keys():
        if key != "default" and key in tags:
            tag_key = key
            break
    notes.append(random.choice(TAG_NOTE_OPTIONS[tag_key]))

    diff_key = difficulty if difficulty in DIFFICULTY_NOTE_OPTIONS else "default"
    notes.append(random.choice(DIFFICULTY_NOTE_OPTIONS[diff_key]))

    for threshold, options in TIME_NOTE_OPTIONS:
        if time_min <= threshold:
            notes.append(random.choice(options))
            break

    return notes