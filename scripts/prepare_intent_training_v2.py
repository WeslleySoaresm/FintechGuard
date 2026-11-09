
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

TRAIN_PATH = DATA_DIR / "fintechguard_train.csv"
VALIDATION_PATH = DATA_DIR / "fintechguard_validation.csv"
SUPPLEMENTAL_PATH = DATA_DIR / "fintechguard_supplemental.csv"

OUTPUT_PATH = DATA_DIR / "fintechguard_train_augmented.csv"


def normalize_text(text):
    return " ".join(str(text).lower().split())


def load_dataset(path):
    df = pd.read_csv(path)

    required = {"text", "intent"}

    if not required.issubset(df.columns):
        raise ValueError(
            f"{path.name}: colunas text e intent são obrigatórias."
        )

    df = df[["text", "intent"]].dropna().copy()

    df["text"] = df["text"].astype(str).str.strip()
    df["intent"] = df["intent"].astype(str).str.strip()

    df = df[
        (df["text"] != "") &
        (df["intent"] != "")
    ].copy()

    df["normalized"] = df["text"].apply(normalize_text)

    return df


def main():
    original = load_dataset(TRAIN_PATH)
    validation = load_dataset(VALIDATION_PATH)
    supplemental = load_dataset(SUPPLEMENTAL_PATH)

    print("Treinamento original:", len(original))
    print("Validação original:", len(validation))
    print("Complementar:", len(supplemental))

    # Combina somente treinamento original e complementar.
    combined = pd.concat(
        [original, supplemental],
        ignore_index=True
    )

    # Remove duplicatas exatas normalizadas.
    before = len(combined)

    combined = combined.drop_duplicates(
        subset="normalized",
        keep="first"
    ).copy()

    removed_duplicates = before - len(combined)

    # Impede que textos da validação entrem no treinamento.
    validation_texts = set(validation["normalized"])

    overlap = combined["normalized"].isin(validation_texts)

    removed_overlap = int(overlap.sum())

    combined = combined.loc[~overlap].copy()

    # Verifica conflitos de rótulo.
    conflicts = (
        combined.groupby("normalized")["intent"]
        .nunique()
    )

    if (conflicts > 1).any():
        raise ValueError(
            "Existem textos com categorias conflitantes."
        )

    # Verifica se as cinco categorias estão presentes.
    expected_classes = {
        "billing inquiry",
        "cancellation request",
        "product inquiry",
        "refund request",
        "technical issue"
    }

    actual_classes = set(combined["intent"])

    if actual_classes != expected_classes:
        raise ValueError(
            f"Categorias inesperadas: {actual_classes}"
        )

    combined = combined[["text", "intent"]]

    combined.to_csv(
        OUTPUT_PATH,
        index=False,
        encoding="utf-8-sig"
    )

    print("\nPREPARAÇÃO CONCLUÍDA")
    print("Duplicatas removidas:", removed_duplicates)
    print("Sobreposições com validação removidas:", removed_overlap)
    print("Total final:", len(combined))

    print("\nDistribuição:")
    print(combined["intent"].value_counts().to_string())

    print("\nArquivo gerado:", OUTPUT_PATH)


if __name__ == "__main__":
    main()
