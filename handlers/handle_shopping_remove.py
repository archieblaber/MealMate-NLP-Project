# handlers/handle_shopping_remove.py

def handle_shopping_remove(user_text, state):

    if not state.shopping_list:
        return (
            "Your shopping list is currently empty, so there's nothing to remove.\n"
            "You can say things like:\n"
            "- \"add that recipe to my shopping list\"\n"
            "- \"add chicken and rice to my shopping list\""
        )

    text = user_text.lower()
    text_words = set(text.split()) # splits user input into a set

    items_to_remove = set()

    for item in state.shopping_list:
        item_lower = item.lower()
        item_tokens = [t for t in item_lower.split() if len(t) > 2] 

        if any(tok in text_words for tok in item_tokens): # if even one word in the input text is in a shopping list item remove it
            items_to_remove.add(item) # builds a list of items to remove if a 

    if not items_to_remove:

        # builds user response
        if len(state.shopping_list) == 1:
            current = f"- {state.shopping_list[0]}"
        else:
            current = "\n".join(f"- {it}" for it in state.shopping_list)

        return (
            "I couldn't work out which item you wanted to remove.\n"
            "Right now your shopping list has:\n"
            f"{current}\n\n"
            "Try saying something like:\n"
            "- \"remove chicken from my shopping list\"\n"
            "- \"take rice off my list\""
        )

    new_list = [it for it in state.shopping_list if it not in items_to_remove]
    state.shopping_list = new_list

    removed_lines = "\n".join(f"- {it}" for it in sorted(items_to_remove))

    if not new_list:
        return (
            "Okay, I've removed these from your shopping list:\n"
            f"{removed_lines}\n\n"
            "Your shopping list is now empty.\n"
            "You can say things like:\n"
            "- \"add that recipe to my shopping list\"\n"
            "- \"add tomatoes and onions to my shopping list\""
        )

    remaining_lines = "\n".join(f"- {it}" for it in new_list)

    return (
        "Okay, I've removed these from your shopping list:\n"
        f"{removed_lines}\n\n"
        "You still have these items on your list:\n"
        f"{remaining_lines}\n\n"
        "You can also say:\n"
        "- \"show me my shopping list\"\n"
        "- \"clear my shopping list\""
    )