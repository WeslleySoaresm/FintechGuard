
# Auditoria inicial do dataset de intenções do FintechGuard.
# O objetivo é conhecer a distribuição dos dados antes de treinar novamente.

import pandas as pd

from pathlib import Path


# Localiza a raiz do projeto.
BASE_DIR = Path(__file__).resolve().parent.parent

# Caminho do dataset utilizado no treinamento.
DATASET_PATH = BASE_DIR / "data" / "intent_dataset_v3_pending.csv"


def main():

    # Carrega os dados.
    df = pd.read_csv(DATASET_PATH)

    print("\n=== INFORMAÇÕES GERAIS ===")
    print("Total de registros:", len(df))
    print("Colunas:", df.columns.tolist())

    # Verifica registros vazios.
    print("\n=== DADOS AUSENTES ===")
    print(df[["text", "intent"]].isna().sum())

    # Verifica quantidade de textos duplicados.
    print("\n=== TEXTOS DUPLICADOS ===")
    print(df["text"].duplicated().sum())

    # Distribuição das intenções.
    print("\n=== DISTRIBUIÇÃO DAS INTENÇÕES ===")
    print(df["intent"].value_counts())

    # Analisa o tamanho das mensagens.
    df["text_length"] = df["text"].astype(str).str.len()

    print("\n=== TAMANHO DAS MENSAGENS ===")
    print(df["text_length"].describe())

    # Mostra 10 exemplos aleatórios de cada intenção.
    print("\n=== EXEMPLOS POR INTENÇÃO ===")
    
    
    # Investiga a origem dos registros.
    print("\n=== ORIGEM DOS DADOS ===")
    print(df["source"].value_counts(dropna=False))

    # Investiga o estado de revisão dos registros.
    print("\n=== STATUS DE REVISÃO ===")
    print(df["review_status"].value_counts(dropna=False))

    # Cruza a origem com a intenção.
    print("\n=== ORIGEM POR INTENÇÃO ===")
    print(pd.crosstab(df["intent"], df["source"]))

    # Cruza o status de revisão com a intenção.
    print("\n=== REVISÃO POR INTENÇÃO ===")
    print(pd.crosstab(df["intent"], df["review_status"]))

    # Mostra exemplos de cada origem para inspeção manual.
    print("\n=== EXEMPLOS POR ORIGEM ===")

    for source in df["source"].dropna().unique():
        print(f"\nORIGEM: {source}")

        examples = df[df["source"] == source]["text"].sample(
            min(5, len(df[df["source"] == source])),
            random_state=42
        )

        for example in examples:
            print("-", example)


if __name__ == "__main__":
    main()

