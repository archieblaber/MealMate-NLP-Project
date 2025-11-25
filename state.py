class ConversationState:
    def __init__(self):
        self.username = None
        self.dietary_pref = None             # "vegan", "vegetarian", "gluten free", etc
        self.disliked_ingredients = []       # list of strings
        self.shopping_list = []              # ingredients
        self.last_recipe = None              # recipe name
        self.last_intent = None              # useful for follow-up responses
