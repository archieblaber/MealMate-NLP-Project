# handlers/handle_recipe_more.py

from random import randint
from state import ConversationState
from recipe_manager import RecipeManager
from recipe_summary_templates import RECIPE_SUMMARY_TEMPLATES


def handle_recipe_more(state, recipe_manager):

    if not state.last_recipe_list or len(state.last_recipe_list) == 0:
        return (
            "I don't have any recipes in mind yet.\n"
            "First ask me something like 'what can I cook with chicken?'."
        )

    recipes = state.last_recipe_list

    current_idx = state.last_recipe_index or 0 # wraps round if needed
    next_idx = (current_idx + 1) % len(recipes) # selects a new random recipe

    # updates convo state
    state.last_recipe_index = next_idx
    state.last_recipe = recipes[next_idx]
    recipe_name = state.last_recipe

    row = recipe_manager.get_recipe_by_name(recipe_name) # gets recipe row
    if row is None:
        return (
            "I couldn't load the details for the next recipe.\n"
            "Try asking me for a new recipe search."
        )
    
    # extracts details from recipe row
    difficulty = row["difficulty"]
    cuisine = row["cuisine"]
    time_min = row["time_to_cook_min"]

    # builds return response
    template = RECIPE_SUMMARY_TEMPLATES[
        randint(0, len(RECIPE_SUMMARY_TEMPLATES) - 1)
    ]
    summary_text = template.format(
        name=recipe_name,
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