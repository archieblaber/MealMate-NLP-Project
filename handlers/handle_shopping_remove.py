# handlers/handle_shopping_remove.py

def handle_shopping_remove(user_text, state):
    """
    Remove one or more items from the shopping list based on the user's message.

    Strategy:
    - If the shopping list is empty -> explain and suggest next steps.
    - Try to match words in the user_text to items currently on the list.
      e.g. "remove chicken and rice" will remove any items whose words
      overlap with "chicken" or "rice" (like "chicken breast", "basmati rice").
    - If nothing matches -> show the list and ask the user to be more specific.
    """

    if not state.shopping_list:
        return (
            "Your shopping list is currently empty, so there’s nothing to remove.\n"
            "You can say things like:\n"
            "• \"add that recipe to my shopping list\"\n"
            "• \"add chicken and rice to my shopping list\""
        )

    # Normalise user text
    text = user_text.lower()
    text_words = set(text.split())

    # Try to find which items the user might mean
    items_to_remove = set()

    for item in state.shopping_list:
        item_lower = item.lower()
        item_tokens = [t for t in item_lower.split() if len(t) > 2]  # ignore tiny words like "of", "to"

        # If any meaningful token from the item appears in the user's text,
        # we assume this is what they want to remove.
        if any(tok in text_words for tok in item_tokens):
            items_to_remove.add(item)

    if not items_to_remove:
        # Nothing matched – help the user out.
        # Show the current list so they can copy wording if they want.
        if len(state.shopping_list) == 1:
            current = f"- {state.shopping_list[0]}"
        else:
            current = "\n".join(f"- {it}" for it in state.shopping_list)

        return (
            "I couldn't work out which item you wanted to remove.\n"
            "Right now your shopping list has:\n"
            f"{current}\n\n"
            "Try saying something like:\n"
            "• \"remove chicken from my shopping list\"\n"
            "• \"take rice off my list\""
        )

    # Actually remove them
    new_list = [it for it in state.shopping_list if it not in items_to_remove]
    state.shopping_list = new_list

    # Build response
    removed_lines = "\n".join(f"- {it}" for it in sorted(items_to_remove))

    if not new_list:
        # List is now empty
        return (
            "Okay, I’ve removed these from your shopping list:\n"
            f"{removed_lines}\n\n"
            "Your shopping list is now empty.\n"
            "You can say things like:\n"
            "• \"add that recipe to my shopping list\"\n"
            "• \"add tomatoes and onions to my shopping list\""
        )

    # List still has items
    remaining_lines = "\n".join(f"- {it}" for it in new_list)

    return (
        "Okay, I’ve removed these from your shopping list:\n"
        f"{removed_lines}\n\n"
        "You still have these items on your list:\n"
        f"{remaining_lines}\n\n"
        "You can also say:\n"
        "• \"show me my shopping list\"\n"
        "• \"clear my shopping list\""
    )