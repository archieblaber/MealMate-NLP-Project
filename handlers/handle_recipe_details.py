# handlers/handle_recipe_details.py

from recipe_manager import RecipeManager
from state import ConversationState
from recipe_detail_notes import build_recipe_notes


def handle_recipe_details(state: ConversationState, recipe_manager: RecipeManager):
    """
    Respond to intents like: 'tell me more about that recipe'
    Uses the last recipe stored in state (from a previous search).
    """

    if not state.last_recipe:
        return (
            "I don't have a recipe in mind yet.\n"
            "First ask me to find you something to cook, "
            "then you can say 'tell me more about that recipe'."
        )

    row = recipe_manager.get_recipe_by_name(state.last_recipe)
    notes = build_recipe_notes(row)
    if row is None:
        return (
            "Sorry, I couldn't find the full details for that recipe.\n"
            "Try asking me for another recipe."
        )

    name = row["recipe_name"]
    ingredients = row["ingredients"]
    instructions = row["instructions"]
    time_min = row["time_to_cook_min"]
    difficulty = row["difficulty"]
    cuisine = row["cuisine"]
    tags = row["tags"]

    lines = []
    lines.append("")
    lines.append("--------------------------------------------------------------")
    lines.append(f"Here are more details for: {name}")
    lines.append("")
    lines.append(f"• Cuisine: {cuisine}")
    lines.append(f"• Difficulty: {difficulty}")
    lines.append(f"• Time to cook: {time_min} minutes")
    lines.append(f"• Tags: {tags}")
    lines.append("")
    lines.append("Notes about this recipe:")
    for i, note in enumerate(notes):
        lines.append(f"{i+1}. {note}")
    lines.append("")
    lines.append("Ingredients:")
    lines.append(','.join(ingredients.split(";")))
    lines.append("")
    lines.append("Instructions:")
    lines.append(instructions)
    lines.append("")
    lines.append("If you like this one, you can say:")
    lines.append("• \"add that recipe to my shopping list\"")
    lines.append("• \"show me another recipe\"")
    lines.append("--------------------------------------------------------------")

    return "\n".join(lines)
