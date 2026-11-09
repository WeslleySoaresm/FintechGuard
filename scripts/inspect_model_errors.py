
from pathlib import Path
import joblib

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "agents" / "intent_classifier.joblib"

MESSAGES = [
    "Can you explain the fees applied to my account?",
    "My account dashboard is not loading correctly.",
]

def main():
    model = joblib.load(MODEL_PATH)

    vectorizer = model.named_steps["tfidf"]
    classifier = model.named_steps["classifier"]

    feature_names = vectorizer.get_feature_names_out()

    for message in MESSAGES:
        print("\n" + "=" * 70)
        print(f"Mensagem: {message}")

        transformed = vectorizer.transform([message])
        probabilities = classifier.predict_proba(transformed)[0]

        ranking = sorted(
            zip(classifier.classes_, probabilities),
            key=lambda item: item[1],
            reverse=True,
        )

        print("\nProbabilidades:")
        for intent, probability in ranking:
            print(f"{intent}: {probability:.2%}")

        print("\nPalavras reconhecidas pelo TF-IDF:")
        recognized = [
            (feature_names[index], transformed[0, index])
            for index in transformed.indices
        ]

        for word, weight in sorted(
            recognized,
            key=lambda item: item[1],
            reverse=True,
        ):
            print(f"{word}: {weight:.4f}")

if __name__ == "__main__":
    main()
