class ConversationState:
    def __init__(self):
        self.username = None
        self.dietary_pref = set()             # "vegan", "vegetarian", "gluten free", etc
        self.disliked_ingredients = set()    # list of strings
        self.shopping_list = []           # ingredients
        self.last_recipe = None              # recipe name
        self.last_intent = None              # useful for follow-up responses
        self.last_recipe_index = 0
