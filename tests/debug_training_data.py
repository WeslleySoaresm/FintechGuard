import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_PATH = BASE_DIR / "data" / "fintechguard_train.csv"

df = pd.read_csv(DATASET_PATH)

print("\n=== DISTRIBUIÇÃO COMPLETA ===")
print(df["intent"].value_counts().to_string())

print("\n=== DIVERSIDADE DE MENSAGENS ===")

for intent, group in df.groupby("intent"):
    unique_messages = group["text"].str.lower().nunique()

    print(f"\nIntenção: {intent}")
    print(f"Total de registros: {len(group)}")
    print(f"Mensagens únicas: {unique_messages}")

    print("\nExemplos:")
    for message in group["text"].drop_duplicates().head(5):
        print("-", message)