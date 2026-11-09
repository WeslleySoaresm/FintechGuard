
from pathlib import Path
import pandas as pd

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT_DIR / "data" / "training_dataset.csv"

df = pd.read_csv(DATA_FILE)

print("\n===== AUDITORIA DO DATASET =====")

# 1. Remover colunas completamente vazias
empty_columns = df.columns[df.isna().all()].tolist()

print("\nColunas completamente vazias:")
print(empty_columns)

# 2. Manter apenas as colunas utilizadas
df = df[["Ticket Type", "Ticket Description"]].copy()

# 3. Remover registros incompletos
df = df.dropna(subset=["Ticket Type", "Ticket Description"])

# 4. Identificar descrições genéricas
generic_patterns = [
    "i'm having an issue with the {product_purchased}",
    "please assist",
    "the issue i'm facing is intermittent",
]

def is_generic(text):
    text = str(text).lower()
    return any(pattern in text for pattern in generic_patterns)

df["generic"] = df["Ticket Description"].apply(is_generic)

print("\nDescrições identificadas como genéricas:")
print(df["generic"].value_counts())

print("\nPercentual genérico:")
print(f"{df['generic'].mean() * 100:.2f}%")

# 5. Verificar categorias e distribuição
print("\nDistribuição por categoria:")
print(df["Ticket Type"].value_counts())

print("\n===== RESULTADO POR CATEGORIA =====")
print(
    df.groupby("Ticket Type")["generic"]
    .agg(["count", "sum", "mean"])
)

# 6. Salvar relatório
output = ROOT_DIR / "reports" / "dataset_audit.csv"
output.parent.mkdir(exist_ok=True)

df.to_csv(output, index=False)

print(f"\nRelatório salvo em: {output}")

