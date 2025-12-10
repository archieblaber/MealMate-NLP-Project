# handlers/handle_add_dislike.py

from state import ConversationState

# words to ignore when looking for ingredients in user text
FILLER_WORDS = {
    "add", "put", "to", "my", "the", "on", "in", "into", "and",
    "shopping", "list", "that", "this", "recipe", "for", "of",
    "please", "can", "you", "dont", "don't", "dislike", "hate",
    "no", "not", "i", "like", "prefer", "avoid", "avoidance"
}

# replaces and with , then splits the input on ,
# makes a new list of tokens from the user input only if they are not in the filler words set and their length > 2
# returns ingredients found as a list
def _extract_dislike_phrases(user_text):
    text = user_text.lower().replace(" and ", ",")
    segments = text.split(",")
    found = []

    for seg in segments:
        tokens = seg.strip().split()
        cleaned = [t for t in tokens if t not in FILLER_WORDS and len(t) > 2]
        phrase = " ".join(cleaned)
        if phrase and phrase not in found:
            found.append(phrase)

    return found


def handle_add_dislike(user_text, state):

    dislikes = _extract_dislike_phrases(user_text)

    if not dislikes:
        return (
            "I'm not sure what ingredient you want to avoid.\n"
            "You can say things like:\n"
            "- \"I don't like mushrooms\"\n"
            "- \"avoid peanuts and prawns\"\n"
            "- \"no beef please\""
        )

    added = []
    already = []

    for ing in dislikes:
        if ing in state.disliked_ingredients:
            already.append(ing) # build list of ingredients that were already disliked for output
        else:
            state.disliked_ingredients.add(ing)
            added.append(ing) # builds list of newly disliked ingredients for output

    response_lines = []

    if added:
        response_lines.append(
            f"Okay, I'll avoid these ingredients from now on: {', '.join(added)}."
        )

    if already:
        response_lines.append(
            f"I was already avoiding: {', '.join(already)}."
        )

    response_lines.append(
        "I will filter recipe suggestions based on your dislikes."
    )

    return "\n".join(response_lines)