
from pathlib import Path
import pandas as pd

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT_DIR / "reports" / "dataset_audit.csv"

df = pd.read_csv(DATA_FILE)

# Considerar somente os registros que passaram pelo filtro inicial
df = df[df["generic"] == False].copy()

print("===== AMOSTRA PARA REVISÃO MANUAL =====")

for category, group in df.groupby("Ticket Type"):
    print(f"\n\n{'=' * 70}")
    print(f"CATEGORIA: {category}")
    print(f"TOTAL DISPONÍVEL: {len(group)}")
    print("=" * 70)

    sample = group.sample(
        n=min(20, len(group)),
        random_state=42
    )

    for index, row in enumerate(sample.itertuples(), start=1):
        print(f"\n{index}. {row[2]}")
