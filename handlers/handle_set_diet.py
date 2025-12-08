# handlers/handle_set_diet.py

def handle_set_diet(user_text, state):
    """
    Extract dietary preferences from the user's message and store them in state.dietary_pref.

    Looks for phrases like:
    - vegan
    - vegetarian / veggie / vege
    - gluten free
    - dairy free
    - high protein
    - low carb
    """

    text = user_text.lower()
    found = set()

    # --- basic keyword detection ---

    # vegan
    if "vegan" in text:
        found.add("vegan")

    # vegetarian / veggie / vege
    if "vegetarian" in text or "veggie" in text or "vege" in text:
        found.add("vegetarian")

    # gluten free
    if "gluten free" in text or "gluten-free" in text:
        found.add("gluten free")

    # dairy free
    if "dairy free" in text or "dairy-free" in text or "lactose free" in text:
        found.add("dairy free")

    # high protein
    if "high protein" in text:
        found.add("high protein")

    # low carb / keto
    if "low carb" in text or "keto" in text:
        found.add("low carb")

    # --- no recognised prefs ---
    if not found:
        return (
            "I couldn't see a clear dietary preference in that.\n"
            "You can say things like:\n"
            "• \"I'm vegan\"\n"
            "• \"I'm vegetarian\"\n"
            "• \"I need gluten free recipes from now on\"\n"
            "• \"I'm trying to eat high protein meals\""
        )

    # ensure state has a set
    if state.dietary_pref is None:
        state.dietary_pref = set()

    # update preferences
    before = set(state.dietary_pref)
    state.dietary_pref.update(found)
    after = state.dietary_pref

    # build confirmation message
    new_prefs = after
    prefs_list = ", ".join(sorted(new_prefs))

    # Work out what changed (for a bit nicer feedback)
    added = after - before
    if added:
        added_text = ", ".join(sorted(added))
        prefix = f"Got it, I'll remember that you're {added_text}."
    else:
        prefix = "Your dietary preferences are already set like that."

    return (
        f"{prefix}\n"
        f"From now on, I'll try to show recipes that match: {prefs_list}."
    )