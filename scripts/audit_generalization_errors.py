
from pathlib import Path

import pandas as pd
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "agents" / "intent_classifier.joblib"
TRAIN_PATH = BASE_DIR / "data" / "fintechguard_train.csv"

ERROR_CASES = [
    {
        "text": "Can you explain the fees applied to my account?",
        "expected": "billing inquiry",
    },
    {
        "text": "My account dashboard is not loading correctly.",
        "expected": "technical issue",
    },
]


def main():
    df = pd.read_csv(TRAIN_PATH)

    df = df.dropna(subset=["text", "intent"]).copy()

    df["text"] = df["text"].astype(str).str.strip()
    df["intent"] = df["intent"].astype(str).str.strip()

    df = df[
        (df["text"] != "") &
        (df["intent"] != "")
    ].copy()

    model = joblib.load(MODEL_PATH)

    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        sublinear_tf=True,
    )

    train_matrix = vectorizer.fit_transform(df["text"])

    print("\n===== AUDITORIA POR SIMILARIDADE =====")

    for case in ERROR_CASES:
        text = case["text"]
        expected = case["expected"]

        prediction = model.predict([text])[0]
        probabilities = model.predict_proba([text])[0]

        ranking = sorted(
            zip(model.classes_, probabilities),
            key=lambda item: item[1],
            reverse=True,
        )

        query_vector = vectorizer.transform([text])

        similarities = cosine_similarity(
            query_vector,
            train_matrix,
        )[0]

        df_results = df.copy()
        df_results["similarity"] = similarities

        print("\n" + "=" * 65)
        print("Mensagem:", text)
        print("Esperado:", expected)
        print("Predito:", prediction)

        print("\nProbabilidades do modelo:")

        for intent, probability in ranking:
            print(f"{intent}: {probability:.2%}")

        print("\nCinco exemplos mais semelhantes:")

        top_examples = df_results.nlargest(5, "similarity")

        for _, row in top_examples.iterrows():
            print(f"\nSimilaridade: {row['similarity']:.2%}")
            print(f"Categoria: {row['intent']}")
            print(f"Texto: {row['text']}")


if __name__ == "__main__":
    main()
