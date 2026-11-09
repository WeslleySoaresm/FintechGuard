
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent

INPUT_FILE = BASE_DIR / "customer_support_tickets_cleaned.csv"
OUTPUT_FILE = BASE_DIR / "trainxing_dataset.csv"
CONFLICTS_FILE = BASE_DIR / "training_conflicts.csv"


def prepare_dataset():
    df = pd.read_csv(INPUT_FILE)

    # Selecionar somente as colunas necessárias
    df = df[["Ticket Type", "Ticket Description"]].copy()

    # Normalizar categorias
    df["Ticket Type"] = (
        df["Ticket Type"]
        .astype("string")
        .str.strip()
        .str.lower()
    )

    # Normalizar textos
    df["Ticket Description"] = (
        df["Ticket Description"]
        .astype("string")
        .str.strip()
    )

    # Remover registros inválidos
    df = df.dropna(
        subset=["Ticket Type", "Ticket Description"]
    )

    df = df[
        (df["Ticket Type"] != "") &
        (df["Ticket Description"] != "")
    ].copy()

    # Identificar descrições com categorias conflitantes
    category_counts = (
        df.groupby("Ticket Description")["Ticket Type"]
        .nunique()
    )

    conflicting_texts = category_counts[
        category_counts > 1
    ].index

    conflicts = df[
        df["Ticket Description"].isin(conflicting_texts)
    ].copy()

    # Remover todos os textos conflitantes
    df = df[
        ~df["Ticket Description"].isin(conflicting_texts)
    ].copy()

    # Remover duplicatas consistentes
    df = df.drop_duplicates(
        subset=["Ticket Description"]
    )

    # Salvar os resultados
    df.to_csv(OUTPUT_FILE, index=False)
    conflicts.to_csv(CONFLICTS_FILE, index=False)

    print("Preparação concluída.")
    print("Registros para treinamento:", len(df))
    print("Textos conflitantes removidos:", len(conflicts))
    print("Categorias:", df["Ticket Type"].nunique())

    print("\nDistribuição das classes:")
    print(df["Ticket Type"].value_counts())

    print("\nArquivos gerados:")
    print(OUTPUT_FILE)
    print(CONFLICTS_FILE)


if __name__ == "__main__":
    prepare_dataset()
