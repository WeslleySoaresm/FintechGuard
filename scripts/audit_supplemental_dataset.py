
from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

SUPPLEMENTAL_PATH = DATA_DIR / "fintechguard_supplemental.csv"
TRAIN_PATH = DATA_DIR / "fintechguard_train.csv"
VALIDATION_PATH = DATA_DIR / "fintechguard_validation.csv"

SIMILARITY_THRESHOLD = 0.75


def normalize_text(text):
    return " ".join(str(text).lower().split())


def load_dataset(path):
    df = pd.read_csv(path)
    df = df.dropna(subset=["text", "intent"]).copy()

    df["text"] = df["text"].astype(str).str.strip()
    df["intent"] = df["intent"].astype(str).str.strip()
    df["normalized"] = df["text"].apply(normalize_text)

    return df[
        (df["normalized"] != "")
        & (df["intent"] != "")
    ].copy()


def audit_against(supplemental, reference, reference_name):
    print("\n" + "=" * 75)
    print(f"AUDITORIA CONTRA: {reference_name}")
    print("=" * 75)

    exact_matches = 0
    conflicts = 0
    similar_matches = 0

    # Verifica duplicatas exatas
    reference_lookup = {}

    for _, row in reference.iterrows():
        reference_lookup.setdefault(row["normalized"], []).append(row)

    for _, new_row in supplemental.iterrows():
        matches = reference_lookup.get(new_row["normalized"], [])

        for old_row in matches:
            exact_matches += 1

            if new_row["intent"] != old_row["intent"]:
                conflicts += 1
                print("\nCONFLITO DE RÓTULO:")
                print(f"Novo: {new_row['text']}")
                print(f"Categoria nova: {new_row['intent']}")
                print(f"Original: {old_row['text']}")
                print(f"Categoria original: {old_row['intent']}")

    # Verifica similaridade textual
    combined = pd.concat(
        [supplemental["text"], reference["text"]],
        ignore_index=True
    )

    vectorizer = TfidfVectorizer(
        analyzer="char_wb",
        ngram_range=(3, 5),
        min_df=1
    )

    matrix = vectorizer.fit_transform(combined)

    new_matrix = matrix[:len(supplemental)]
    reference_matrix = matrix[len(supplemental):]

    similarities = cosine_similarity(new_matrix, reference_matrix)

    for i, (_, new_row) in enumerate(supplemental.iterrows()):
        best_indices = similarities[i].argsort()[::-1][:3]

        for index in best_indices:
            score = similarities[i][index]

            if score >= SIMILARITY_THRESHOLD:
                old_row = reference.iloc[index]
                similar_matches += 1

                print("\nEXEMPLO SEMELHANTE:")
                print(f"Similaridade: {score:.2%}")
                print(f"Novo: [{new_row['intent']}] {new_row['text']}")
                print(f"Referência: [{old_row['intent']}] {old_row['text']}")

                if new_row["intent"] != old_row["intent"]:
                    print("ATENÇÃO: categorias diferentes!")

    print("\nRESUMO:")
    print(f"Duplicatas exatas: {exact_matches}")
    print(f"Conflitos de rótulo exatos: {conflicts}")
    print(f"Pares semelhantes encontrados: {similar_matches}")


def main():
    supplemental = load_dataset(SUPPLEMENTAL_PATH)
    train = load_dataset(TRAIN_PATH)
    validation = load_dataset(VALIDATION_PATH)

    print("CONTAGEM DOS DATASETS")
    print(f"Complementar: {len(supplemental)}")
    print(f"Treinamento: {len(train)}")
    print(f"Validação: {len(validation)}")

    print("\nDISTRIBUIÇÃO DO COMPLEMENTAR:")
    print(supplemental["intent"].value_counts().to_string())

    audit_against(supplemental, train, "TREINAMENTO")
    audit_against(supplemental, validation, "VALIDAÇÃO")


if __name__ == "__main__":
    main()

