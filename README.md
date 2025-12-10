# **MealMate - NLP Meal Recommendation & Shopping Chatbot**

MealMate is an interactive, rule-based NLP chatbot that helps users discover recipes, store food preferences, manage dietary requirements, and build a grocery shopping list through natural conversation. It uses TF-IDF intent matching, cosine similarity, context tracking and modular intent handlers to create a smooth conversational experience.

---

## **Features**

* 🍽️ **Recipe search** by ingredient, cuisine, or quick meals
* 🚫 **Preference management** (dietary requirements + disliked ingredients)
* 🛒 **Shopping list creation**, editing, and virtual ordering
* 💬 **Small talk** and sentiment-aware responses
* 🧠 **Context tracking** to interpret follow-up commands
* 🔍 **Intent classification** using TF-IDF + cosine similarity

---

# **Installation Guide**

MealMate runs on **Python 3.10+**.

Below are instructions for **Windows** and **macOS** to create a virtual environment, install the required packages, and run the chatbot.

---

# 🛠️ **1. Create a Virtual Environment**

### **macOS / Linux**

```bash
python3 -m venv venv
source venv/bin/activate
```

### **Windows (PowerShell)**

```powershell
python -m venv venv
venv\Scripts\activate
```

You should now see `(venv)` in your terminal, indicating the environment is active.

---

# 📦 **2. Install Required Libraries**

Run the following command **after activating your venv**:

```bash
pip install joblib nltk numpy pandas python-dateutil pytz regex scikit-learn scipy six threadpoolctl tqdm tzdata
```

Or install from a `requirements.txt` if you prefer.

---

# ▶️ **3. Run MealMate**

Make sure you're in the project folder (same directory as `chatbot.py`), then run:

### macOS/Linux

```bash
python3 chatbot.py
```

### Windows

```powershell
python chatbot.py
```

MealMate will greet you, ask for your name, and show you what it can do.

---

# 📁 **Project Structure**

```
chatbot.py                # Main entry point
handlers/                 # All intent handlers
intent_model.py           # TF-IDF + cosine similarity model
corpus.py                 # Builds training corpus
recipe_manager.py         # Recipe dataset loading and filtering
state.py                  # ConversationState class
nlp_utils.py              # Tokenisation, stemming, preprocessing
recipe_summary_templates.py
smalltalk_data.py
tasks_intents.py
recipes.csv               # Dataset used for search
```

---
