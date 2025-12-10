# handlers/handle_shopping_place_order.py

def handle_shopping_place_order(state):

    if not state.shopping_list:
        return (
            "You don't have anything on your shopping list yet.\n"
            "First add some ingredients, then you can ask me to place your order."
        )

    seen = set()
    unique_items = []
    for item in state.shopping_list:
        if item not in seen:
            seen.add(item)
            unique_items.append(item)

    # builds items_text with shopping list values to confirm with user
    if len(unique_items) == 1:
        items_text = f"- {unique_items[0]}"
    else:
        items_text_lines = [f"- {item}" for item in unique_items]
        items_text = "\n".join(items_text_lines)

    lines = []
    print("MealMate: Okay, here's the order I'm about to place:")
    print()
    print(items_text)
    print()
    
    while True:
        confirm = input("MealMate: Do you want me to place this order now? (y/n) ").strip().lower() # confirmation with user before ordering
        if confirm in ("y", "yes"):
            state.shopping_list = []
            return (
                "Great, your order has been placed and "
                "I've cleared your shopping list."
            )
        elif confirm in ("n", "no"):
            return "Okay, I won't place the order yet."
        else:
            print('MealMate: Please answer with "y" or "n".')

    return "\n".join(lines)