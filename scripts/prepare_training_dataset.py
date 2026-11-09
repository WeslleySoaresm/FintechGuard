
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

TRAIN_PATH = DATA_DIR / "fintechguard_train.csv"
SUPPLEMENTAL_PATH = DATA_DIR / "fintechguard_supplemental.csv"
OUTPUT_PATH = DATA_DIR / "fintechguard_train_v2.csv"


def normalize_text(text):
    return " ".join(str(text).lower().split())


def load_dataset(path):
    df = pd.read_csv(path)

    required_columns = {"text", "intent"}
    if not required_columns.issubset(df.columns):
        raise ValueError(
            f"{path.name} precisa conter as colunas text e intent."
        )

    df = df[["text", "intent"]].dropna().copy()
    df["text"] = df["text"].astype(str).str.strip()
    df["intent"] = df["intent"].astype(str).str.strip()

    df = df[(df["text"] != "") & (df["intent"] != "")]

    return df


def main():
    original = load_dataset(TRAIN_PATH)
    supplemental = load_dataset(SUPPLEMENTAL_PATH)

    print("Treinamento original:", len(original))
    print("Complementar:", len(supplemental))

    combined = pd.concat(
        [original, supplemental],
        ignore_index=True
    )

    combined["normalized"] = combined["text"].apply(normalize_text)

    # Remove duplicatas normalizadas, preservando a primeira ocorrência.
    combined = combined.drop_duplicates(
        subset=["normalized"],
        keep="first"
    )

    combined = combined.drop(columns=["normalized"])

    # Verifica conflitos de rótulo após normalização.
    label_counts = combined.groupby("text")["intent"].nunique()

    if (label_counts > 1).any():
        raise ValueError("Foram encontrados conflitos de rótulo.")

    combined.to_csv(
        OUTPUT_PATH,
        index=False,
        encoding="utf-8-sig"
    )

    print("\nNovo dataset criado!")
    print("Arquivo:", OUTPUT_PATH)
    print("Total final:", len(combined))

    print("\nDistribuição por categoria:")
    print(combined["intent"].value_counts().to_string())


if __name__ == "__main__":
    main()
