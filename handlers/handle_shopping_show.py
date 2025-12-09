# handlers/handle_shopping_show.py

from state import ConversationState


def handle_shopping_show(state):
    if not state.shopping_list:
        return (
            "Your shopping list is currently empty.\n"
            'You can add things by saying, for example:\n'
            '- "add chicken and pasta to my shopping list"\n'
            '- "add apples"\n'
            '- "add that recipe to my shopping list" (after I suggest a recipe)'
        )

    lines = []
    lines.append("Here's what is currently on your shopping list:")
    lines.append("")

    for i, item in enumerate(state.shopping_list, start=1):
        lines.append(f"{i}. {item}")

    lines.append("")
    lines.append(
        'You can say things like:\n'
        '- "remove milk from my shopping list"\n'
        '- "clear my shopping list"'
    )

    return "\n".join(lines)