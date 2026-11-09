
from pathlib import Path
import pandas as pd

ROOT_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = ROOT_DIR / "data" / "intent_dataset_v2.csv"
OUTPUT_FILE = ROOT_DIR / "reports" / "intent_dataset_review.csv"

df = pd.read_csv(INPUT_FILE)

# Organiza os exemplos por categoria.
df = df.sort_values(["intent", "text"]).reset_index(drop=True)

# Adiciona campos para revisão humana.
df["is_correct"] = ""
df["review_notes"] = ""

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUTPUT_FILE, index=False)

print("Arquivo de revisão criado!")
print(f"Total de exemplos: {len(df)}")
print(f"Arquivo: {OUTPUT_FILE}")

print("\nExemplos por categoria:")
print(df.groupby("intent").size())
