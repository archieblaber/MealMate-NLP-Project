# handlers/handle_shopping_clear.py

from state import ConversationState

def handle_shopping_clear(state):

    if not state.shopping_list:
        return (
            "Your shopping list is already empty.\n"
            "You can add items by saying things like:\n"
            "- \"add chicken\"\n"
            "- \"add that recipe to my shopping list\""
        )

    state.shopping_list.clear()

    return (
        "I've cleared your shopping list.\n"
        "You can start fresh by adding items again."
    )