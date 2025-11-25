from smalltalk_intents import build_smalltalk_dataframe
from task_intents import build_task_intents_dataframe
import pandas as pd

def load_full_corpus():
    st_df = build_smalltalk_dataframe()
    task_df = build_task_intents_dataframe()
    df_all = pd.concat([st_df, task_df], ignore_index=True)
    return df_all
