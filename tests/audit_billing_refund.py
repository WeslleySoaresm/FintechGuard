
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_PATH = BASE_DIR / "data" / "fintechguard_train_augmented.csv"

df = pd.read_csv(DATASET_PATH)

# Normaliza os textos apenas para facilitar a busca.
df["text_normalized"] = (
    df["text"]
    .astype(str)
    .str.lower()
    .str.strip()
)

terms = [
    "cobrado duas vezes",
    "cobrança duplicada",
    "dinheiro de volta",
    "quero meu dinheiro",
    "quero receber",
    "estorno",
    "reembolso",
    "charged twice",
    "money back",
    "duplicate charge",
]

print("===== DISTRIBUIÇÃO DAS CATEGORIAS =====")
print(df["intent"].value_counts())

for term in terms:
    matches = df[
        df["text_normalized"].str.contains(
            term,
            regex=False,
            na=False
        )
    ]

    if not matches.empty:
        print(f"\n===== TERMO: {term} =====")
        print(matches["intent"].value_counts())
        print(matches[["text", "intent"]].head(10).to_string(index=False))
    else:
        print(f"\nTermo não encontrado: {term}")
