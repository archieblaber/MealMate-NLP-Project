# recipe_manager.py
import pandas as pd

class RecipeManager:
    def __init__(self, csv_path):
        self.df = pd.read_csv(csv_path)
        self._prepare_dataframe()
        self._build_ingredient_tokens()

    def _prepare_dataframe(self):
        df = self.df

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

    def get_recipe_by_name(self, recipe_name):
        mask = self.df["recipe_name"].str.lower() == recipe_name.lower()
        matches = self.df[mask]
        if matches.empty:
            return None
        return matches.iloc[0]

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

        for w in words:
            if w in self.base_ingredient_tokens:
                found.add(w)

        expanded = set()
        for f in found:
            for ingredient in self.ingredient_tokens:
                if f in ingredient:
                    expanded.add(ingredient)

        return list(expanded)

    def extract_cuisine_keywords(self, user_text):
        text = user_text.lower()
        cuisines = set(self.df["cuisine_lower"].dropna().unique())

        found = []
        for c in cuisines:
            if c and c in text:
                found.append(c)

        return found

    def search_by_cuisine(self, user_text, state):
        """
        Search recipes that match cuisine keywords mentioned by the user,
        then filter by:
        - state.dietary_pref (e.g. {"vegan", "vegetarian"})
        - state.disliked_ingredients (list of strings)

        Returns: a list of recipe names.
        """
        keywords = self.extract_cuisine_keywords(user_text)

        if not keywords:
            return []

        df = self.df

        mask = pd.Series(False, index=df.index)
        for kw in keywords:
            mask |= df["cuisine_lower"].str.contains(kw, na=False)

        filtered = df[mask]

        prefs = getattr(state, "dietary_pref", set()) or set()
        if prefs:
            for pref in prefs:
                filtered = filtered[
                    filtered["tags_lower"].str.contains(pref.lower(), na=False)
                ]

        dislikes = getattr(state, "disliked_ingredients", []) or []
        for bad in dislikes:
            bad = bad.lower()
            filtered = filtered[
                ~filtered["ingredients_lower"].str.contains(bad, na=False, regex=False)
            ]

        return filtered["recipe_name"].tolist()
    
    def search_quick(self, user_text, state):
        text = user_text.lower()

        limit = 20

        df = self.df

        time_col = pd.to_numeric(df["time_to_cook_min"], errors="coerce")

        mask = time_col <= limit
        filtered = df[mask]

        prefs = getattr(state, "dietary_pref", set()) or set()
        if prefs:
            for pref in prefs:
                filtered = filtered[
                    filtered["tags_lower"].str.contains(pref.lower(), na=False)
                ]

        dislikes = getattr(state, "disliked_ingredients", []) or []
        for bad in dislikes:
            bad = bad.lower()
            filtered = filtered[
                ~filtered["ingredients_lower"].str.contains(bad, na=False, regex=False)
            ]

        return filtered["recipe_name"].tolist()

    def search_by_ingredient(self, user_text: str, state):
        keywords = self.extract_ingredient_keywords(user_text)

        if not keywords:
            return []

        df = self.df

        mask = pd.Series(False, index=df.index)
        for kw in keywords:
            mask |= df["ingredients_lower"].str.contains(kw, na=False)

        filtered = df[mask]

        prefs = getattr(state, "dietary_pref", set()) or set()
        if prefs:
            for pref in prefs:
                filtered = filtered[
                    filtered["tags_lower"].str.contains(pref.lower(), na=False)
                ]

        dislikes = getattr(state, "disliked_ingredients", []) or []
        for bad in dislikes:
            bad = bad.lower()
            filtered = filtered[
                ~filtered["ingredients_lower"].str.contains(bad, na=False, regex=False)
            ]

        return filtered["recipe_name"].tolist()