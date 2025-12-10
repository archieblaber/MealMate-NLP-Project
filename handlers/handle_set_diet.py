# handlers/handle_set_diet.py

def handle_set_diet(user_text, state):

    text = user_text.lower()
    found = set()

    # looks for dietary keywords in user input since there are limited options, matches them and builds a list of requirements it found
    if "vegan" in text:
        found.add("vegan")

    if "vegetarian" in text or "veggie" in text or "vege" in text:
        found.add("vegetarian")

    if "gluten free" in text or "gluten-free" in text:
        found.add("gluten free")

    if "dairy free" in text or "dairy-free" in text or "lactose free" in text:
        found.add("dairy free")

    if "high protein" in text:
        found.add("high protein")

    if "low carb" in text or "keto" in text:
        found.add("low carb")

    if not found: # didn't find any keywords
        return (
            "I couldn't see a clear dietary preference in that.\n"
            "You can say things like:\n"
            "- \"I'm vegan\"\n"
            "- \"I'm vegetarian\"\n"
            "- \"I need gluten free recipes from now on\"\n"
            "- \"I'm trying to eat high protein meals\""
        )

    if state.dietary_pref is None:
        state.dietary_pref = set()

    # saves state before to compare to after to see if any changes have occured and respond accordingly
    before = set(state.dietary_pref) 
    state.dietary_pref.update(found)
    after = state.dietary_pref

    new_prefs = after
    prefs_list = ", ".join(sorted(new_prefs))


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