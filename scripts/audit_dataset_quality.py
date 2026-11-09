
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd

df = pd.read_csv("data/fintechguard_train.csv")

df = df.loc[:, ~df.columns.str.startswith("Unnamed")]
df = df.dropna(subset=["text", "intent"])

# Normaliza apenas para identificar textos repetidos.
df["normalized"] = (
    df["text"]
    .str.lower()
    .str.replace(r"\s+", " ", regex=True)
    .str.strip()
)

print("\n=== DISTRIBUIÇÃO DAS CATEGORIAS ===")
print(df["intent"].value_counts().to_string())

print("\n=== TEXTOS ÚNICOS POR CATEGORIA ===")

for intent, group in df.groupby("intent"):
    unique_count = group["normalized"].nunique()

    print(
        f"{intent}: "
        f"{unique_count} textos únicos "
        f"de {len(group)} registros"
    )

print("\n=== EXEMPLOS DE BILLING ===")

billing = df[df["intent"] == "billing inquiry"]

for text in billing["text"].drop_duplicates().head(15):
    print("-", text)

print("\n=== EXEMPLOS DE CANCELLATION ===")

cancellation = df[
    df["intent"] == "cancellation request"
]

for text in cancellation["text"].drop_duplicates().head(15):
    print("-", text)

print("\n=== EXEMPLOS DE REFUND ===")

refund = df[df["intent"] == "refund request"]

for text in refund["text"].drop_duplicates().head(15):
    print("-", text)

