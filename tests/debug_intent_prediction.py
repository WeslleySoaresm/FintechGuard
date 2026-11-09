import joblib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "fintechguard_agents" / "intent_classifier.joblib"

model = joblib.load(MODEL_PATH)

messages = [
    "I want to know the details of my last payment.",
    "Can you show me my recent payment history?",
    "Why was I charged this amount?",
    "I would like to understand the fees on my bank statement.",
    "Please explain the amount debited from my account.",
]

print("\n=== TESTE DE GENERALIZAÇÃO: BILLING ===")

for message in messages:
    prediction = model.predict([message])[0]
    probabilities = model.predict_proba([message])[0]

    classes = model.named_steps["classifier"].classes_

    confidence = max(probabilities)

    print("\nMensagem:", message)
    print("Intenção:", prediction)
    print(f"Confiança: {confidence:.2%}")

    ranking = sorted(
        zip(classes, probabilities),
        key=lambda item: item[1],
        reverse=True,
    )

    for intent, probability in ranking[:3]:
        print(f"  {intent}: {probability:.2%}")