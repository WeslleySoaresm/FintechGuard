import sys
from pathlib import Path

# Adiciona a raiz do projeto ao caminho de importação.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd

from fintechguard_agents.predict_intent import predict_intent
# Carrega os dados usados no treinamento.
df = pd.read_csv("data/fintechguard_train.csv")

# Palavras e expressões que queremos investigar.
terms = [
    "payment history",
    "last payment",
    "payment details",
    "recent payment",
    "transaction history",
    "detalhes do pagamento",
    "último pagamento",
    "histórico de pagamento",
]

print("\n=== AUDITORIA DO DATASET ===")

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
    print(f"Ocorrências: {len(matches)}")

    if not matches.empty:
        print(matches["label"].value_counts().to_string())

print("\n=== AUDITORIA DO MODELO ===")

message = "I want to know the details of my last payment."

result = predict_intent(message)

print("Mensagem:", message)
print("Intenção:", result["intent"])
print("Confiança:", result["confidence"])
