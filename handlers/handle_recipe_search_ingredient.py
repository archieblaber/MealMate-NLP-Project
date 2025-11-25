# handlers/handle_recipe_search_ingredient.py

from recipe_manager import RecipeManager
from state import ConversationState
from random import randint


def handle_recipe_search_ingredient(user_text, state: ConversationState, recipe_manager: RecipeManager):

    recipes = recipe_manager.search_by_ingredient(user_text, state)

    if not recipes:
        return (
            "I couldn't find any recipes matching that ingredient, given your preferences.\n"
            "Try mentioning a clearer ingredient, like 'beef', 'pasta', or 'tofu'."
        )
    
    recipe_index = randint(0, len(recipes) - 1)

    # store context for follow-ups
    state.last_recipe = recipes
    state.last_recipe_index = recipe_index

    top_recipe = recipes[recipe_index]

    # build response lines
    lines = []
    lines.append(f"Here's a recipe you could try:\n• {top_recipe}")

    # explain filtering (good for the report)
    if state.dietary_pref or state.disliked_ingredients:
        filter_bits = []
        if state.dietary_pref:
            filter_bits.append(f"diet: {', '.join(state.dietary_pref)}")
        if state.disliked_ingredients:
            filter_bits.append("avoiding: " + ", ".join(state.disliked_ingredients))
        lines.append(f"(Filtered based on your preferences: {', '.join(filter_bits)})")

    # suggest what they can say next
    lines.append("")
    lines.append("You can ask me:")
    lines.append("• \"tell me more about that recipe\"")
    lines.append("• \"show me another recipe\"")
    lines.append("• \"add that recipe to my shopping list\"")

    return "\n".join(lines)
