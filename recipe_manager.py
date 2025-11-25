# recipe_manager.py
import pandas as pd

class RecipeManager:
    def __init__(self, csv_path: str):
        self.df = pd.read_csv(csv_path)
        self._prepare_dataframe()
        self._build_ingredient_tokens()

    def _prepare_dataframe(self):
        df = self.df

        # Adjust these names if your CSV uses different headers
        df["ingredients_lower"] = df["ingredients"].str.lower()
        df["tags_lower"] = df["tags"].str.lower()
        df["cuisine_lower"] = df["cuisine"].str.lower()

        df["search_text"] = (
            df["recipe_name"].str.lower()
            + " "
            + df["ingredients_lower"]
            + " "
            + df["tags_lower"]
            + " "
            + df["cuisine_lower"]
        )

    def _build_ingredient_tokens(self):
        tokens = set()
        base_tokens = set()

        for row in self.df["ingredients_lower"]:
            for tok in row.split(";"):
                clean = tok.strip()
                if clean:
                    tokens.add(clean)
                    # break into words
                    for w in clean.split():
                        base_tokens.add(w)

        self.ingredient_tokens = tokens
        self.base_ingredient_tokens = base_tokens

    def extract_ingredient_keywords(self, user_text: str):
        text = user_text.lower()
        words = text.split()

        found = set()

        # 1. match exact base words like "beef", "pork", "chicken"
        for w in words:
            if w in self.base_ingredient_tokens:
                found.add(w)

        # 2. match full ingredient entries that contain those words
        expanded = set()
        for f in found:
            for ingredient in self.ingredient_tokens:
                if f in ingredient:
                    expanded.add(ingredient)

        return list(expanded)

    def search_by_ingredient(self, user_text: str, state):
        """
        Search recipes that contain any of the ingredient keywords
        mentioned by the user, then filter by:
        - state.dietary_pref    (e.g. {"vegan", "vegetarian"})
        - state.disliked_ingredients (list of strings)

        Returns: a list of recipe names.
        """
        keywords = self.extract_ingredient_keywords(user_text)

        # If no explicit ingredient word recognised, just give up
        if not keywords:
            return []

        df = self.df

        mask = pd.Series(False, index=df.index)
        for kw in keywords:
            mask |= df["ingredients_lower"].str.contains(kw, na=False) # only keep rows where an ingredient appears

        filtered = df[mask]

        # --- Filter by dietary preference, if set ---
        prefs = getattr(state, "dietary_pref", set()) or set()
        if prefs:
            # require all selected diet keywords to appear in tags_lower
            for pref in prefs:
                filtered = filtered[
                    filtered["tags_lower"].str.contains(pref.lower(), na=False)
                ]

        # --- Filter out disliked ingredients, if any ---
        dislikes = getattr(state, "disliked_ingredients", []) or []
        for bad in dislikes:
            bad = bad.lower()
            filtered = filtered[
                ~filtered["ingredients_lower"].str.contains(bad, na=False, regex=False)
            ]

        # Return just recipe names as a simple list
        return filtered["recipe_name"].tolist()


# For quick manual testing
# if __name__ == "__main__":
#     from state import ConversationState

#     state = ConversationState()
#     state.dietary_prefs = None
#     state.disliked_ingredients = ["mushrooms"]

#     manager = RecipeManager("recipes.csv")
#     recipes = manager.search_by_ingredient("I want a pasta dinner", state)
#     print(recipes)
