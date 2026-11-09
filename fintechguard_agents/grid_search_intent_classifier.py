
from pathlib import Path

import joblib
import pandas as pd

from sklearn.dummy import DummyClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from sklearn.pipeline import Pipeline


BASE_DIR = Path(__file__).resolve().parent.parent

TRAIN_PATH = BASE_DIR / "data" / "fintechguard_train_augmented.csv"
VALIDATION_PATH = BASE_DIR / "data" / "fintechguard_validation.csv"

# Não sobrescreve o modelo original.
MODEL_PATH = (
    BASE_DIR
    / "fintechguard_agents"
    / "intent_classifier_v2.joblib"
)

def normalize_text(text: str) -> str:
    """Normaliza texto para comparação de duplicatas."""
    return " ".join(str(text).lower().split())


def load_dataset(path: Path) -> pd.DataFrame:
    """Carrega e limpa um dataset."""
    if not path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")

    df = pd.read_csv(path)

    # Remove colunas extras.
    df = df.loc[
        :,
        ~df.columns.str.startswith("Unnamed")
    ].copy()

    required_columns = {"text", "intent"}
    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Colunas ausentes em {path.name}: {missing_columns}"
        )

    # Remove registros sem texto ou intenção.
    df = df.dropna(subset=["text", "intent"]).copy()

    df["text"] = df["text"].astype(str).str.strip()
    df["intent"] = df["intent"].astype(str).str.strip()

    df = df[
        (df["text"] != "") &
        (df["intent"] != "")
    ].copy()

    # Remove duplicatas normalizadas.
    df["_normalized"] = df["text"].map(normalize_text)
    df = df.drop_duplicates(subset="_normalized")

    return df.drop(columns="_normalized")


def main():

    # 1. Carregamento dos datasets.
    train_df = load_dataset(TRAIN_PATH)
    validation_df = load_dataset(VALIDATION_PATH)

    # 2. Remove do treinamento qualquer texto presente na validação.
    validation_texts = set(
        validation_df["text"].map(normalize_text)
    )

    train_df["_normalized"] = train_df["text"].map(normalize_text)

    overlap_count = train_df["_normalized"].isin(validation_texts).sum()

    train_df = train_df[
        ~train_df["_normalized"].isin(validation_texts)
    ].drop(columns="_normalized").copy()

    if train_df.empty or validation_df.empty:
        raise ValueError("Treinamento ou validação está vazio.")

    # 3. Separação das variáveis.
    X_train = train_df["text"]
    y_train = train_df["intent"]

    X_validation = validation_df["text"]
    y_validation = validation_df["intent"]

    # 4. Verificação das classes.
    if set(y_train.unique()) != set(y_validation.unique()):
        raise ValueError(
            "Treinamento e validação precisam conter as mesmas classes."
        )

    class_counts = y_train.value_counts()

    if class_counts.min() < 5:
        raise ValueError(
            "Cada classe precisa ter pelo menos 5 exemplos "
            "para utilizar StratifiedKFold com 5 divisões."
        )

    print("\n===== DADOS CARREGADOS =====")
    print(f"Treinamento: {len(X_train)}")
    print(f"Validação: {len(X_validation)}")
    print(f"Sobreposições removidas do treino: {overlap_count}")

    print("\nDistribuição das classes no treinamento:")
    print(class_counts)

    # 5. Pipeline de Machine Learning.
    pipeline = Pipeline([
        (
            "tfidf",
            TfidfVectorizer(
                min_df=1,
                max_df=0.95,
                sublinear_tf=True,
            ),
        ),
        (
            "classifier",
            LogisticRegression(
                max_iter=2000,
                random_state=42,
            ),
        ),
    ])

    # 6. Hiperparâmetros.
    param_grid = {
        "tfidf__ngram_range": [
            (1, 1),
            (1, 2),
            (1, 3),
        ],
        "classifier__C": [
            0.1,
            1,
            10,
        ],
        "classifier__class_weight": [
            None,
            "balanced",
        ],
    }

    # 7. Validação cruzada estratificada.
    cv = StratifiedKFold(
        n_splits=5,
        shuffle=True,
        random_state=42,
    )

    # 8. GridSearchCV.
    grid_search = GridSearchCV(
        estimator=pipeline,
        param_grid=param_grid,
        scoring="f1_macro",
        cv=cv,
        n_jobs=-1,
        verbose=2,
        refit=True,
    )

    total_combinations = len(param_grid["tfidf__ngram_range"]) * (
        len(param_grid["classifier__C"])
        * len(param_grid["classifier__class_weight"])
    )

    print("\n===== INICIANDO GRIDSEARCHCV =====")
    print(f"Combinações: {total_combinations}")
    print(f"Treinamentos: {total_combinations * cv.get_n_splits()}")

    # A busca utiliza exclusivamente os dados de treinamento.
    grid_search.fit(X_train, y_train)

    best_model = grid_search.best_estimator_

    # 9. Avaliação do modelo V2.
    predictions = best_model.predict(X_validation)

    tuned_accuracy = accuracy_score(y_validation, predictions)
    tuned_precision = precision_score(
        y_validation, predictions, average="macro", zero_division=0
    )
    tuned_recall = recall_score(
        y_validation, predictions, average="macro", zero_division=0
    )
    tuned_f1 = f1_score(
        y_validation, predictions, average="macro", zero_division=0
    )

    # 10. Baseline.
    baseline = DummyClassifier(strategy="most_frequent")
    baseline.fit(X_train, y_train)

    baseline_predictions = baseline.predict(X_validation)

    baseline_accuracy = accuracy_score(
        y_validation, baseline_predictions
    )
    baseline_f1 = f1_score(
        y_validation,
        baseline_predictions,
        average="macro",
        zero_division=0,
    )

    # 11. Resultados.
    print("\n===== MELHORES HIPERPARÂMETROS =====")
    print(grid_search.best_params_)

    print(
        "\nMelhor F1 Macro na validação cruzada: "
        f"{grid_search.best_score_:.4f}"
    )

    print("\n===== COMPARAÇÃO COM BASELINE =====")
    print(f"Baseline Accuracy: {baseline_accuracy:.4f}")
    print(f"Modelo V2 Accuracy: {tuned_accuracy:.4f}")
    print(
        "Ganho Accuracy: "
        f"{(tuned_accuracy - baseline_accuracy) * 100:.2f} p.p."
    )

    print(f"\nBaseline F1 Macro: {baseline_f1:.4f}")
    print(f"Modelo V2 F1 Macro: {tuned_f1:.4f}")
    print(
        "Ganho F1 Macro: "
        f"{(tuned_f1 - baseline_f1) * 100:.2f} p.p."
    )

    print("\n===== MÉTRICAS DO MODELO V2 =====")
    print(f"Precision Macro: {tuned_precision:.4f}")
    print(f"Recall Macro: {tuned_recall:.4f}")
    print(f"F1 Macro: {tuned_f1:.4f}")

    print("\n===== CLASSIFICATION REPORT =====")
    print(
        classification_report(
            y_validation,
            predictions,
            zero_division=0,
        )
    )

    print("\n===== MATRIZ DE CONFUSÃO =====")
    labels = sorted(y_train.unique())

    matrix = confusion_matrix(
        y_validation,
        predictions,
        labels=labels,
    )

    print(pd.DataFrame(
        matrix,
        index=[f"Real: {label}" for label in labels],
        columns=[f"Previsto: {label}" for label in labels],
    ))

    # 12. Salvamento do modelo V2.
    joblib.dump(best_model, MODEL_PATH)

    print(f"\nModelo V2 salvo em: {MODEL_PATH}")
    print("\n===== TREINAMENTO V2 CONCLUÍDO =====")


if __name__ == "__main__":
    main()
