# task_intents.py

import pandas as pd


def build_task_intents_dataframe():
    rows = [
        # =========================
        # RECIPE SEARCH BY INGREDIENT
        # =========================
        {
            "Question": "what can I cook with ",
            "Answer": "",
            "Intent": "recipe_search_ingredient",
        },
        {
            "Question": "give me recipes using ",
            "Answer": "",
            "Intent": "recipe_search_ingredient",
        },
        {
            "Question": "I have some what can I make",
            "Answer": "",
            "Intent": "recipe_search_ingredient",
        },
        {
            "Question": "any ideas with for dinner",
            "Answer": "",
            "Intent": "recipe_search_ingredient",
        },
        {
            "Question": "show me dishes with ",
            "Answer": "",
            "Intent": "recipe_search_ingredient",
        },
        {
            "Question": "I only have what can I cook",
            "Answer": "",
            "Intent": "recipe_search_ingredient",
        },
        {
            "Question": "Show me recipes with",
            "Answer": "",
            "Intent": "recipe_search_ingredient",
        },

        # =========================
        # RECIPE SEARCH BY DIET / TAGS
        # =========================
        {
            "Question": "show me vegetarian recipes",
            "Answer": "",
            "Intent": "recipe_search_diet",
        },
        {
            "Question": "show me some vegan recipes",
            "Answer": "",
            "Intent": "recipe_search_diet",
        },
        {
            "Question": "find me gluten free recipes",
            "Answer": "",
            "Intent": "recipe_search_diet",
        },
        {
            "Question": "have you got any high protein meals",
            "Answer": "",
            "Intent": "recipe_search_diet",
        },
        {
            "Question": "suggest some low carb recipes",
            "Answer": "",
            "Intent": "recipe_search_diet",
        },
        {
            "Question": "I want a vegetarian high protein meal",
            "Answer": "",
            "Intent": "recipe_search_diet",
        },


        # =========================
        # RECIPE SEARCH BY TIME (QUICK / SLOW)
        # =========================
        {
            "Question": "I need a quick dinner under 20 minutes",
            "Answer": "",
            "Intent": "recipe_search_quick",
        },
        {
            "Question": "show me easy meals I can cook fast",
            "Answer": "",
            "Intent": "recipe_search_quick",
        },
        {
            "Question": "what can I make in 15 minutes",
            "Answer": "",
            "Intent": "recipe_search_quick",
        },
        {
            "Question": "I have more time give me a slow cook recipe",
            "Answer": "",
            "Intent": "recipe_search_quick",
        },

        # =========================
        # RECIPE SEARCH BY CUISINE
        # =========================
        {
            "Question": "show me Italian recipes",
            "Answer": "",
            "Intent": "recipe_search_cuisine",
        },
        {
            "Question": "I fancy something Indian",
            "Answer": "",
            "Intent": "recipe_search_cuisine",
        },
        {
            "Question": "have you got any Mexican dishes",
            "Answer": "",
            "Intent": "recipe_search_cuisine",
        },
        {
            "Question": "recommend a Japanese dinner",
            "Answer": "",
            "Intent": "recipe_search_cuisine",
        },
        {
            "Question": "give me some Thai recipes",
            "Answer": "",
            "Intent": "recipe_search_cuisine",
        },

        # =========================
        # SHOPPING LIST – ADD
        # =========================
        {
            "Question": "add the ingredients for that recipe to my shopping list",
            "Answer": "",
            "Intent": "shopping_add",
        },
        {
            "Question": "put on my shopping list",
            "Answer": "",
            "Intent": "shopping_add",
        },
        {
            "Question": "add to my list",
            "Answer": "",
            "Intent": "shopping_add",
        },
        {
            "Question": "can you add to my shopping list",
            "Answer": "",
            "Intent": "shopping_add",
        },

        # =========================
        # SHOPPING LIST – SHOW
        # =========================
        {
            "Question": "show me my shopping list",
            "Answer": "",
            "Intent": "shopping_show",
        },
        {
            "Question": "what is on my shopping list",
            "Answer": "",
            "Intent": "shopping_show",
        },
        {
            "Question": "list my ingredients to buy",
            "Answer": "",
            "Intent": "shopping_show",
        },

        # =========================
        # SHOPPING LIST – CLEAR / REMOVE
        # =========================
        {
            "Question": "clear my shopping list",
            "Answer": "",
            "Intent": "shopping_clear",
        },
        {
            "Question": "empty my shopping list",
            "Answer": "",
            "Intent": "shopping_clear",
        },
        {
            "Question": "remove from my shopping list",
            "Answer": "",
            "Intent": "shopping_remove",
        },
        {
            "Question": "take off my list",
            "Answer": "",
            "Intent": "shopping_remove",
        },

        # =========================
        # SHOPPING LIST – PLACE ORDER (SIMULATED)
        # =========================
        {
            "Question": "place my grocery order",
            "Answer": "",
            "Intent": "shopping_place_order",
        },
        {
            "Question": "I am ready to order my shopping",
            "Answer": "",
            "Intent": "shopping_place_order",
        },
        {
            "Question": "checkout my shopping list",
            "Answer": "",
            "Intent": "shopping_place_order",
        },

        # =========================
        # USER PROFILE – DIETARY PREFERENCES
        # =========================
        {
            "Question": "I am vegetarian",
            "Answer": "",
            "Intent": "set_diet",
        },
        {
            "Question": "I am vegan",
            "Answer": "",
            "Intent": "set_diet",
        },
        {
            "Question": "from now on I need gluten free food",
            "Answer": "",
            "Intent": "set_diet",
        },
        {
            "Question": "my diet is high protein",
            "Answer": "",
            "Intent": "set_diet",
        },
        {
            "Question": "remember that I am vegetarian",
            "Answer": "",
            "Intent": "set_diet",
        },
        {
            "Question": "remember that I am vegan",
            "Answer": "",
            "Intent": "set_diet",
        },


        # =========================
        # USER PROFILE – DISLIKED INGREDIENTS
        # =========================
        {
            "Question": "I do not like ",
            "Answer": "",
            "Intent": "add_dislike",
        },
        {
            "Question": "please avoid in my recipes",
            "Answer": "",
            "Intent": "add_dislike",
        },
        {
            "Question": "I hate ",
            "Answer": "",
            "Intent": "add_dislike",
        },
        {
            "Question": "do not show me recipes with",
            "Answer": "",
            "Intent": "add_dislike",
        },

        # =========================
        # USER PROFILE – SHOW PREFERENCES
        # =========================
        {
            "Question": "what are my dietary preferences",
            "Answer": "",
            "Intent": "show_prefs",
        },
        {
            "Question": "what diet did I tell you I follow",
            "Answer": "",
            "Intent": "show_prefs",
        },
        {
            "Question": "what ingredients do you know I do not like",
            "Answer": "",
            "Intent": "show_prefs",
        },

        # =========================
        # CONTEXTUAL FOLLOW UPS – MORE / DETAILS
        # =========================
        {
            "Question": "show me another recipe like that",
            "Answer": "",
            "Intent": "recipe_more",
        },
        {
            "Question": "give me a different option",
            "Answer": "",
            "Intent": "recipe_more",
        },
        {
            "Question": "another",
            "Answer": "",
            "Intent": "recipe_more",
        },
        {
            "Question": "give me another one",
            "Answer": "",
            "Intent": "recipe_more",
        },
        {
            "Question": "next recipe",
            "Answer": "",
            "Intent": "recipe_more",
        },
        {
            "Question": "can I have more ideas",
            "Answer": "",
            "Intent": "recipe_more",
        },
        {
            "Question": "tell me more about that recipe",
            "Answer": "",
            "Intent": "recipe_details",
        },
        {
            "Question": "show me the details again",
            "Answer": "",
            "Intent": "recipe_details",
        },

        # =========================
        # HELP / DISCOVERABILITY
        # =========================
        {
            "Question": "how do I use this chatbot",
            "Answer": "",
            "Intent": "help",
        },
        {
            "Question": "what can you do for me",
            "Answer": "",
            "Intent": "help",
        },
        {
            "Question": "explain your features",
            "Answer": "",
            "Intent": "help",
        },
    ]

    return pd.DataFrame(rows)
