class ConversationState:
    def __init__(self):
        self.username = None                # username
        self.dietary_pref = set()           # set of dietary preferences
        self.disliked_ingredients = set()   # set of dislikes ingredients 
        self.shopping_list = []             # list of shopping ingredients
        self.last_recipe = None             # most recently recommended recipe
        self.last_recipe_index = 0          # the index that the most recent recipe was in the recipe list
        self.last_recipe_list = None        # the list of recipes that the most recently recommended one came from
        self.last_intent = None             # last intent that was identified   


