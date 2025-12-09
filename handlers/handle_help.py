# handlers/handle_help.py

from state import ConversationState


def handle_help(state):
    name = state.username or "there"

    lines = []
    lines.append(f"I'm MealMate, a meal-planning and shopping-list assistant, {name}.")
    lines.append("")
    lines.append("Here's what I can do:")

    # Small talk
    lines.append("")
    lines.append("- Small talk")
    lines.append("  Say things like \"hi\", \"how are you\", or \"what is your name\".")

    # Recipe search
    lines.append("")
    lines.append("- Find recipes for you")
    lines.append("  - By ingredient: e.g. \"I want a chicken pasta dinner\", \"what can I cook with tofu\"")
    lines.append("  - By diet: e.g. \"show me vegetarian recipes\", \"show me some vegan recipes\"")
    lines.append("  - By time: e.g. \"I need a quick dinner under 20 minutes\"")
    lines.append("  - By cuisine: e.g. \"show me Italian recipes\", \"I fancy something Indian\"")

    # Personalisation
    lines.append("")
    lines.append("- Remember your preferences")
    lines.append("  - Tell me your diet: \"I am vegetarian\", \"I am vegan\"")
    lines.append("  - Tell me dislikes: \"I do not like mushrooms\", \"please avoid peppers\"")
    lines.append("  I'll use this to filter future recipe suggestions.")

    # Shopping list
    lines.append("")
    lines.append("- Manage a shopping list")
    lines.append("  - \"add that recipe to my shopping list\"")
    lines.append("  - \"add chicken and rice to my shopping list\"")
    lines.append("  - \"show me my shopping list\"")
    lines.append("  - \"clear my shopping list\"")

    #  Follow-ups
    lines.append("")
    lines.append("- Follow up on a recipe")
    lines.append("  After I suggest something, you can say:")
    lines.append("  - \"tell me more about that recipe\"")
    lines.append("  - \"show me another recipe\"")

    # Show current stored prefs if any
    if state.dietary_pref or state.disliked_ingredients:
        lines.append("")
        lines.append("Right now I remember:")
        if state.dietary_pref:
            lines.append(f"  - Your diet: {', '.join(state.dietary_pref)}")
        if state.disliked_ingredients:
            lines.append(f"  - Ingredients you dislike: {', '.join(state.disliked_ingredients)}")

    lines.append("")
    lines.append("You can just talk to me in natural language and I'll try to match what you say to one of these actions.")

    return "\n".join(lines)