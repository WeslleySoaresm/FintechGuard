
import pandas as pd
import joblib

from pathlib import Path
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    classification_report,
    accuracy_score,
    confusion_matrix,
    f1_score,
)
from sklearn.dummy import DummyClassifier


# 1. Localização dos arquivos
BASE_DIR = Path(__file__).resolve().parent.parent

TRAIN_PATH = BASE_DIR / "data" / "fintechguard_train.csv"
VALIDATION_PATH = BASE_DIR / "data" / "fintechguard_validation.csv"

MODEL_PATH = BASE_DIR / "fintechguard_agents" / "intent_classifier.joblib"


# 2. Função para carregar e limpar os dados
def load_dataset(path):
    df = pd.read_csv(path)

    # Verifica se as colunas necessárias existem
    required_columns = {"text", "intent"}

    if not required_columns.issubset(df.columns):
        raise ValueError(
            f"Arquivo {path.name} precisa conter as colunas: "
            f"{required_columns}"
        )

    # Remove registros sem texto ou intenção
    df = df.dropna(subset=["text", "intent"]).copy()

    df["text"] = df["text"].astype(str).str.strip()
    df["intent"] = df["intent"].astype(str).str.strip()

    df = df[
        (df["text"] != "") &
        (df["intent"] != "")
    ]

    # Normaliza apenas para identificar duplicatas
    df["normalized_text"] = (
        df["text"]
        .str.lower()
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )

    df = df.drop_duplicates(
        subset=["normalized_text"],
        keep="first"
    )

    return df


# 3. Carregar os dois datasets
train_df = load_dataset(TRAIN_PATH)
validation_df = load_dataset(VALIDATION_PATH)

# Identificar textos presentes nos dois arquivos
train_texts = set(train_df["normalized_text"])
validation_texts = set(validation_df["normalized_text"])

overlapping_texts = train_texts.intersection(validation_texts)

print("=== AUDITORIA DOS DADOS ===")
print("Registros de treino:", len(train_df))
print("Registros de validação:", len(validation_df))
print("Textos repetidos entre os arquivos:", len(overlapping_texts))

# Remover da validação os textos que também aparecem no treino
validation_df = validation_df[
    ~validation_df["normalized_text"].isin(train_texts)
].copy()

print(
    "Validação após remoção de duplicatas:",
    len(validation_df)
)

if validation_df.empty:
    raise ValueError(
        "Não existem registros independentes para validação."
    )

# Verificar se as categorias são iguais
train_classes = set(train_df["intent"])
validation_classes = set(validation_df["intent"])

if train_classes != validation_classes:
    raise ValueError(
        "As categorias dos datasets de treino e validação são diferentes."
    )

X_train = train_df["text"]
y_train = train_df["intent"]

X_validation = validation_df["text"]
y_validation = validation_df["intent"]


# 4. Criar baseline
baseline = DummyClassifier(strategy="most_frequent")

baseline.fit(X_train, y_train)

baseline_predictions = baseline.predict(X_validation)

print("\n=== BASELINE ===")
print(
    "Accuracy:",
    accuracy_score(y_validation, baseline_predictions)
)


# 5. Criar pipeline de Machine Learning
model = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            ngram_range=(1, 2),
            min_df=1,
            max_df=0.95,
            sublinear_tf=True
        )
    ),
    (
        "classifier",
        LogisticRegression(
            max_iter=2000,
            class_weight="balanced",
            random_state=42
        )
    )
])


# 6. Treinar modelo
model.fit(X_train, y_train)


# 7. Avaliar modelo
predictions = model.predict(X_validation)

print("\n=== LOGISTIC REGRESSION ===")

print(
    "Accuracy:",
    accuracy_score(y_validation, predictions)
)

print(
    "F1 Macro:",
    f1_score(
        y_validation,
        predictions,
        average="macro",
        zero_division=0
    )
)

print("\nRelatório de classificação:")

print(
    classification_report(
        y_validation,
        predictions,
        zero_division=0
    )
)

print("\nMatriz de confusão:")

print(
    confusion_matrix(
        y_validation,
        predictions,
        labels=sorted(train_classes)
    )
)


# 8. Salvar modelo
joblib.dump(model, MODEL_PATH)

print("\nModelo salvo em:", MODEL_PATH)
