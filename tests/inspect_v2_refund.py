import joblib

MODEL_PATH = "agents/intent_classifier_v2.joblib"

model = joblib.load(MODEL_PATH)

messages = [
    "Fui cobrado duas vezes e quero receber o dinheiro de volta.",
    "Fui cobrado duas vezes.",
    "Quero receber meu dinheiro de volta.",
    "Solicito o reembolso de uma cobrança duplicada.",
    "Recebi uma cobrança duplicada e quero estorno.",
    "I was charged twice and want my money back.",
]

for message in messages:
    probabilities = model.predict_proba([message])[0]
    classes = model.classes_

    ranking = sorted(
        zip(classes, probabilities),
        key=lambda item: item[1],
        reverse=True
    )

    print("\nMensagem:", message)
    print("Predição:", model.predict([message])[0])

    for intent, probability in ranking:
        print(f"  {intent}: {probability:.2%}")