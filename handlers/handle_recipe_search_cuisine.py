# handlers/handle_recipe_search_cuisine.py

from random import randint
from recipe_manager import RecipeManager
from state import ConversationState
from recipe_summary_templates import RECIPE_SUMMARY_TEMPLATES


def handle_recipe_search_cuisine(user_text, state, recipe_manager):

    recipes = recipe_manager.search_by_cuisine(user_text, state)

    if not recipes:
        return (
            "I couldn't find any recipes for that cuisine, given your preferences.\n"
            "Try mentioning a cuisine like 'Italian', 'Indian', or 'Mexican'."
        )

    recipe_index = randint(0, len(recipes) - 1)

    state.last_recipe_list = recipes
    state.last_recipe_index = recipe_index
    top_recipe = state.last_recipe = recipes[recipe_index]

    row = recipe_manager.get_recipe_by_name(top_recipe)
    difficulty = row["difficulty"]
    cuisine = row["cuisine"]
    time_min = row["time_to_cook_min"]

    template = RECIPE_SUMMARY_TEMPLATES[randint(0, len(RECIPE_SUMMARY_TEMPLATES) - 1)]
    summary_text = template.format(
        name=top_recipe,
        difficulty=difficulty,
        cuisine=cuisine,
        time=time_min,
    )

    lines = []
    lines.append(summary_text)

    if state.dietary_pref or state.disliked_ingredients:
        filter_bits = []
        if state.dietary_pref:
            filter_bits.append(f"diet: {', '.join(state.dietary_pref)}")
        if state.disliked_ingredients:
            filter_bits.append("avoiding: " + ", ".join(state.disliked_ingredients))
        lines.append(f"(Filtered based on your preferences: {', '.join(filter_bits)})")

    lines.append("")
    lines.append("You can ask me:")
    lines.append("- \"tell me more about that recipe\"")
    lines.append("- \"show me another recipe\"")
    lines.append("- \"add that recipe to my shopping list\"")

    return "\n".join(lines)