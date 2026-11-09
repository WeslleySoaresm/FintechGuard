
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd

df = pd.read_csv("data/fintechguard_train.csv")

# Remove colunas vazias geradas na exportação.
df = df.loc[:, ~df.columns.str.startswith("Unnamed")]

terms = [
    "payment",
    "paid",
    "charge",
    "charged",
    "billing",
    "invoice",
    "pagamento",
    "paguei",
    "cobrança",
    "fatura",
]

for term in terms:
    matches = df[
        df["text"].str.contains(
            term,
            case=False,
            na=False,
            regex=False
        )
    ]

    print("\n" + "=" * 60)
    print(f"TERMO: {term}")
    print(f"TOTAL: {len(matches)}")

    if not matches.empty:
        print("\nDistribuição por intenção:")
        print(matches["intent"].value_counts().to_string())

        print("\nExemplos:")
        for _, row in matches.head(5).iterrows():
            print(f"[{row['intent']}] {row['text']}")
