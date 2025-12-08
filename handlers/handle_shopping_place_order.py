# handlers/handle_shopping_place_order.py

def handle_shopping_place_order(state):
    """
    Placing a shopping order based on the current shopping_list.
    Does NOT clear the list automatically (so we don't surprise the user).
    """

    if not state.shopping_list:
        return (
            "You don't have anything on your shopping list yet.\n"
            "First add some ingredients, then you can ask me to place your order."
        )

    # Deduplicate while preserving order
    seen = set()
    unique_items = []
    for item in state.shopping_list:
        if item not in seen:
            seen.add(item)
            unique_items.append(item)

    # Build a readable bullet list
    if len(unique_items) == 1:
        items_text = f"- {unique_items[0]}"
    else:
        items_text_lines = [f"- {item}" for item in unique_items]
        items_text = "\n".join(items_text_lines)

    lines = []
    lines.append("Okay, I'll place this order for you:")
    lines.append("")
    lines.append(items_text)
    lines.append("")
    lines.append("If you want, you can now say:")
    lines.append("• \"clear my shopping list\"")
    lines.append("• \"show me my shopping list\"")
    lines.append("• \"find me another recipe\"")

    return "\n".join(lines)