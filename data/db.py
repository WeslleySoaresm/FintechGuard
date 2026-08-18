# data/db.py
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / "customer_support_tickets.csv"

def load_data():
    if not CSV_PATH.exists():
        return pd.DataFrame()
    
    # Carrega e substitui qualquer NaN por string vazia ("")
    data = pd.read_csv(CSV_PATH)
    data = data.loc[:, ~data.columns.str.contains('^Unnamed')]
    return data.fillna("")

df = load_data()