# recipe_manager.py
import pandas as pd

class RecipeManager:
    def __init__(self, csv_path):
        self.df = pd.read_csv(csv_path)
        self._prepare_dataframe()
        self._build_ingredient_tokens()

    def _prepare_dataframe(self):
        df = self.df

        # lower case versions of columns
        df["ingredients_lower"] = df["ingredients"].str.lower()
        df["tags_lower"] = df["tags"].str.lower()
        df["cuisine_lower"] = df["cuisine"].str.lower()

        # combined search_text might come in useful?
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
        # get the row of a recipe based on its name
        mask = self.df["recipe_name"].str.lower() == recipe_name.lower()
        matches = self.df[mask]
        if matches.empty:
            return None
        return matches.iloc[0]

    def _build_ingredient_tokens(self):
        # builds a set of full ingredients and a set of individual words from the ingredients
        tokens = set()
        base_tokens = set()

        for row in self.df["ingredients_lower"]:
            for tok in row.split(";"):
                clean = tok.strip()
                if clean:
                    tokens.add(clean) # add full ingredients
                    # break into words
                    for w in clean.split():
                        base_tokens.add(w) # add each word

        self.ingredient_tokens = tokens
        self.base_ingredient_tokens = base_tokens

    def extract_ingredient_keywords(self, user_text):
        # match individual words against base tokens set
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
                    expanded.add(ingredient) # contains full ingredient names for matching

        return list(expanded)

    def extract_cuisine_keywords(self, user_text):
        text = user_text.lower()
        cuisines = set(self.df["cuisine_lower"].dropna().unique()) # gets set of all different cuisines

        found = []
        for c in cuisines:
            if c and c in text:
                found.append(c) # scans user text for cuisines

        return found

    def search_by_cuisine(self, user_text, state):
        keywords = self.extract_cuisine_keywords(user_text)

        if not keywords:
            return []

        df = self.df

        # builds boolean mask, any recipe whos cuisine contains one of the keywords from the user text is True
        mask = pd.Series(False, index=df.index)
        for kw in keywords:
            mask |= df["cuisine_lower"].str.contains(kw, na=False)

        filtered = df[mask] # filters for only where the mask is True so only keeps where cuisine matches

        # filters based on preferences
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

        limit = 20 # 20 minutes is the longest we can return

        df = self.df

        # make sure value in time to cook is numeric and drop invalid values
        time_col = pd.to_numeric(df["time_to_cook_min"], errors="coerce")

        mask = time_col <= limit # make another boolean mask only where time is lower then 20
        filtered = df[mask] 

        # filters by preferences
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

    def search_by_ingredient(self, user_text, state):
        keywords = self.extract_ingredient_keywords(user_text)

        if not keywords:
            return []

        df = self.df

        mask = pd.Series(False, index=df.index)
        for kw in keywords:
            mask |= df["ingredients_lower"].str.contains(kw, na=False) # builds mask where ingredient doesnt appear

        filtered = df[mask] # filters dataframe

        # filters by preference
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