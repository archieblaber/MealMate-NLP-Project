# handlers/handle_shopping_add.py

from state import ConversationState


# Words that are not ingredients
FILLER_WORDS = {
    "add", "put", "to", "my", "the", "on", "in", "into", "and",
    "shopping", "list", "that", "this", "recipe", "for", "of",
    "please", "can", "you"
}


def _extract_freeform_ingredients(user_text):
    """
    Extract ingredients from the user's text by:
    - converting to lowercase,
    - replacing ' and ' with commas,
    - splitting on commas,
    - removing filler words and very short tokens,
    - returning a list of cleaned ingredient phrases.
    """
    text = user_text.lower().replace(" and ", ",")
    raw_segments = text.split(",")
    freeform = []

    for segment in raw_segments:
        tokens = segment.strip().split()
        filtered_tokens = [t for t in tokens if t not in FILLER_WORDS and len(t) > 2]
        phrase = " ".join(filtered_tokens)
        if phrase and phrase not in freeform:
            freeform.append(phrase)

    return freeform


def _add_items_to_shopping_list(items, state):
    """
    Add a list of item strings to the state's shopping_list, avoiding duplicates.
    Returns (added_count, preview_string).
    """
    if state.shopping_list is None:
        state.shopping_list = []

    added_count = 0
    for ing in items:
        if ing not in state.shopping_list:
            state.shopping_list.append(ing)
            added_count += 1

    # Short preview: last up to 5 items on the list
    preview = ", ".join(state.shopping_list[-min(5, len(state.shopping_list)):])
    return added_count, preview


def _add_full_recipe_to_list(state, recipe_manager):
    """
    Fallback: add all ingredients for state.last_recipe to the shopping list.
    Used when user doesn't specify ingredients explicitly.
    """
    if not state.last_recipe:
        return (
            "I don't have a specific recipe in mind yet.\n"
            "First ask me for something to cook (e.g. \"what can I cook with pasta?\"), "
            "then say \"add that recipe to my shopping list\"."
        )

    row = recipe_manager.get_recipe_by_name(state.last_recipe)
    if row is None:
        return (
            "Sorry, I couldn't find that recipe's details in my data.\n"
            "Try asking me for another recipe first."
        )

    raw_ingredients = row["ingredients"]
    ingredients = [ing.strip() for ing in raw_ingredients.split(";") if ing.strip()]

    added_count, preview = _add_items_to_shopping_list(ingredients, state)

    if added_count == 0:
        return (
            f"I've already added all the ingredients for {state.last_recipe} "
            "to your shopping list."
        )

    return (
        f"I've added the ingredients for **{state.last_recipe}** to your shopping list "
        f"({added_count} new item{'s' if added_count != 1 else ''}).\n"
        f"Recent items on your list: {preview}\n"
        'You can say "show me my shopping list" to see everything.'
    )


def handle_shopping_add(user_text, state, recipe_manager):
    """
    Handle things like:
      - "add chicken breast, lemons and olive oil"
      - "add apples"
      - "add that recipe to my shopping list"

    Logic:
      1) Try to extract free-form ingredients from the user's text
         (e.g. "chicken breast", "lemons", "olive oil", "apples")
      2) If we found any ingredients:
         - add them directly to the shopping list
      3) Otherwise, if there's a last_recipe:
         - add the whole recipe's ingredients
      4) If nothing to add and no recipe:
         - tell the user how to phrase things.
    """

    # 1. Extract free-form ingredients (e.g. "apples")
    freeform_ings = _extract_freeform_ingredients(user_text)

    # CASE A: user explicitly named ingredients (free-form only)
    if freeform_ings:
        items_to_add = freeform_ings

        added_count, preview = _add_items_to_shopping_list(items_to_add, state)

        if added_count == 0:
            return (
                "Those items are already on your shopping list.\n"
                f"Recent items on your list: {preview}"
            )

        return (
            f"I've added {added_count} new item"
            f"{'s' if added_count != 1 else ''} to your shopping list "
            f"({', '.join(items_to_add)}).\n"
            f"Recent items on your list: {preview}\n"
            'You can say "show me my shopping list" to see everything.'
        )

    # CASE B: no explicit ingredients – fall back to adding the whole last recipe
    if state.last_recipe:
        return _add_full_recipe_to_list(state, recipe_manager)

    # CASE C: nothing to add and no recipe context
    return (
        "I'm not sure what you want me to add.\n"
        "You can say things like:\n"
        '• "add apples"\n'
        '• "add chicken and pasta to my shopping list"\n'
        '• "add that recipe to my shopping list" (after I suggest a recipe)'
    )