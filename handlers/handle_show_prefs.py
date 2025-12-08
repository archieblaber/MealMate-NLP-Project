# handlers/handle_show_prefs.py

def handle_show_prefs(state):
    """
    Summarise the user's stored dietary preferences and disliked ingredients.
    """

    has_diet = bool(state.dietary_pref)
    has_dislikes = bool(state.disliked_ingredients)

    if not has_diet and not has_dislikes:
        return (
            "I don’t have any dietary preferences or dislikes saved yet.\n"
            "You can tell me things like:\n"
            "• \"I am vegetarian\"\n"
            "• \"I am vegan\"\n"
            "• \"I need gluten free recipes from now on\"\n"
            "• \"I do not like mushrooms\"\n"
            "• \"please avoid peppers in my recipes\""
        )

    lines = []
    lines.append("Here’s what I know about your preferences:")

    if has_diet:
        diet_list = ", ".join(sorted(state.dietary_pref))
        lines.append(f"• Dietary preferences: {diet_list}")
    else:
        lines.append("• Dietary preferences: (none set)")

    if has_dislikes:
        dislikes_list = ", ".join(sorted(state.disliked_ingredients))
        lines.append(f"• Ingredients to avoid: {dislikes_list}")
    else:
        lines.append("• Ingredients to avoid: (none set)")

    lines.append("")
    lines.append("I use these to:")
    lines.append("• filter recipe suggestions so they match your diet, and")
    lines.append("• avoid recipes containing ingredients you don’t like.")
    lines.append("")
    lines.append("You can update them by saying things like:")
    lines.append("• \"I am vegan\"")
    lines.append("• \"I don’t like olives\"")

    return "\n".join(lines)