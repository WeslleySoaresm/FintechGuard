
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_PATH = BASE_DIR / "data" / "fintechguard_train.csv"

df = pd.read_csv(DATASET_PATH)

# Palavras relacionadas a consultas de cobrança
terms = [
    "payment history",
    "last payment",
    "payment details",
    "transaction history",
    "recent payment",
    "histórico de pagamento",
    "último pagamento",
    "detalhes do pagamento",
    "extrato",
]

print("\n=== INVESTIGAÇÃO DE BILLING ===")

for term in terms:
    matches = df[
        df["text"].str.contains(
            term,
            case=False,
            na=False,
            regex=False
        )
    ]

    print(f"\nExpressão: {term}")
    print(f"Total: {len(matches)}")

    if not matches.empty:
        print(
            matches[["text", "intent"]]
            .to_string(index=False)
        )

