
import joblib
import pandas as pd

from pathlib import Path
from sklearn.metrics import classification_report, accuracy_score


# 1. Localizar o modelo treinado
BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "agents" / "intent_classifier.joblib"

model = joblib.load(MODEL_PATH)


# 2. Mensagens inéditas para avaliação
test_data = [
    {
        "text": "Minha conta foi debitada duas vezes pela mesma compra.",
        "intent": "billing inquiry",
    },
    {
        "text": "Quero cancelar o serviço e impedir novas cobranças.",
        "intent": "cancellation request",
    },
    {
        "text": "O aplicativo fecha sozinho quando tento fazer uma transferência.",
        "intent": "technical issue",
    },
    {
        "text": "Quais são os limites diários para transferências?",
        "intent": "product inquiry",
    },
    {
        "text": "Paguei por um serviço que não recebi e solicito meu dinheiro de volta.",
        "intent": "refund request",
    },
    {
        "text": "I was charged twice for the same transaction.",
        "intent": "billing inquiry",
    },
    {
        "text": "Please close my account and stop the monthly subscription.",
        "intent": "cancellation request",
    },
    {
        "text": "The mobile app crashes whenever I open my account.",
        "intent": "technical issue",
    },
    {
        "text": "Does your bank offer international transfers?",
        "intent": "product inquiry",
    },
    {
        "text": "I never received the service and want my money back.",
        "intent": "refund request",
    },
]


# 3. Separar mensagens e respostas esperadas
df = pd.DataFrame(test_data)

X_test = df["text"]
y_test = df["intent"]


# 4. Executar previsões
predictions = model.predict(X_test)


# 5. Mostrar resultados individuais
df["predicted_intent"] = predictions
df["correct"] = df["intent"] == df["predicted_intent"]

print("=== TESTE DE GENERALIZAÇÃO ===")

for _, row in df.iterrows():
    print("\nMensagem:", row["text"])
    print("Esperado:", row["intent"])
    print("Predito:", row["predicted_intent"])
    print("Resultado:", "CORRETO" if row["correct"] else "ERRO")


# 6. Métricas
print("\n=== RESULTADOS GERAIS ===")

print("Accuracy:", accuracy_score(y_test, predictions))

print("\nRelatório de classificação:")

print(
    classification_report(
        y_test,
        predictions,
        zero_division=0
    )
)
