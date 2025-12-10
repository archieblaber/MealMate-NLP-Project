# handlers/handle_shopping_add.py

from state import ConversationState

# words to ignore when looking for ingredients in user text
FILLER_WORDS = {
    "add", "put", "to", "my", "the", "on", "in", "into", "and",
    "shopping", "list", "that", "this", "recipe", "for", "of",
    "please", "can", "you"
}

# replaces and with , then splits the input on ,
# makes a new list of tokens from the user input only if they are not in the filler words set and their length > 2
# returns ingredients found as a list
def _extract_freeform_ingredients(user_text):
    text = user_text.lower().replace(" and ", ",")
    segments = text.split(",")
    freeform = []

    for seg in segments:
        tokens = seg.strip().split()
        filtered_tokens = [t for t in tokens if t not in FILLER_WORDS and len(t) > 2]
        phrase = " ".join(filtered_tokens)
        if phrase and phrase not in freeform:
            freeform.append(phrase)

    return freeform


def _add_items_to_shopping_list(items, state):
    if state.shopping_list is None:
        state.shopping_list = []

    added_count = 0
    for ing in items:
        if ing not in state.shopping_list:
            state.shopping_list.append(ing) # add to shopping list
            added_count += 1

    preview = ", ".join(state.shopping_list[-min(5, len(state.shopping_list)):]) #preview at most 5 items after adding
    return added_count, preview


def _add_full_recipe_to_list(state, recipe_manager):
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
    ingredients = [ing.strip() for ing in raw_ingredients.split(";") if ing.strip()] # makes a new list by splitting on semi-colons and stripping output

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
        'You can say "show me my shopping list" to see everything or "place my shopping order" if you are ready to order.'
    )


def handle_shopping_add(user_text, state, recipe_manager):
    freeform_ings = _extract_freeform_ingredients(user_text)

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
            'You can say "show me my shopping list" to see everything or "place my shopping order" if you are ready to order.'
        )

    if state.last_recipe:
        return _add_full_recipe_to_list(state, recipe_manager)

    return (
        "I'm not sure what you want me to add.\n"
        "You can say things like:\n"
        '- "add apples"\n'
        '- "add chicken and pasta to my shopping list"\n'
        '- "add that recipe to my shopping list" (after I suggest a recipe)'
    )