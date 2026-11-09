
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
TRAIN_PATH = BASE_DIR / "data" / "fintechguard_train.csv"

TERMS = [
    "fee",
    "fees",
    "applied",
    "charge",
    "charges",
    "dashboard",
    "loading",
    "load",
    "refresh",
    "account",
    "not loading",
]

def main():
    df = pd.read_csv(TRAIN_PATH)
    df = df.dropna(subset=["text", "intent"]).copy()

    df["text"] = df["text"].astype(str).str.lower()
    df["intent"] = df["intent"].astype(str).str.lower()

    for term in TERMS:
        matches = df[df["text"].str.contains(term, regex=False)]

        print("\n" + "=" * 65)
        print(f"Termo: {term}")
        print(f"Ocorrências: {len(matches)}")

        if matches.empty:
            print("Nenhum exemplo encontrado.")
            continue

        print("\nDistribuição por categoria:")
        print(matches["intent"].value_counts().to_string())

        print("\nExemplos:")
        for _, row in matches.head(3).iterrows():
            print(f"[{row['intent']}] {row['text']}")

if __name__ == "__main__":
    main()
