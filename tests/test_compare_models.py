
from pathlib import Path

import joblib
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
)

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_V1_PATH = (
    BASE_DIR / "fintechguard_agents" / "intent_classifier.joblib"
)

MODEL_V2_PATH = (
    BASE_DIR / "fintechguard_agents" / "intent_classifier_v2.joblib"
)


# Mesmas 20 mensagens do teste anterior.
TEST_CASES = [
    ("Gostaria de consultar o valor da minha última fatura.", "billing inquiry"),
    ("Why was I charged this monthly maintenance fee?", "billing inquiry"),
    ("Preciso entender uma cobrança que apareceu no extrato.", "billing inquiry"),
    ("Can you explain the fees applied to my account?", "billing inquiry"),

    ("Quero encerrar minha conta bancária definitivamente.", "cancellation request"),
    ("Please stop my subscription immediately.", "cancellation request"),
    ("Desejo cancelar o serviço contratado.", "cancellation request"),
    ("I no longer want to use this financial product.", "cancellation request"),

    ("Quais são as vantagens do cartão premium?", "product inquiry"),
    ("What are the interest rates for your savings account?", "product inquiry"),
    ("Quero conhecer as opções de investimento disponíveis.", "product inquiry"),
    ("Does your bank offer international transfers?", "product inquiry"),

    ("Fui cobrado duas vezes e quero receber o dinheiro de volta.", "refund request"),
    ("Please return the amount debited from my account.", "refund request"),
    ("Solicito o reembolso de uma compra que foi cancelada.", "refund request"),
    ("I paid for the same service twice. I need a refund.", "refund request"),

    ("Não consigo acessar o aplicativo pelo meu celular.", "technical issue"),
    ("The mobile application crashes whenever I try to log in.", "technical issue"),
    ("O site apresenta uma mensagem de erro ao carregar.", "technical issue"),
    ("My account dashboard is not loading correctly.", "technical issue"),
]


def evaluate_model(model_name, model_path, X, y_true):

    if not model_path.exists():
        raise FileNotFoundError(
            f"Modelo não encontrado: {model_path}"
        )

    model = joblib.load(model_path)
    predictions = model.predict(X)

    accuracy = accuracy_score(y_true, predictions)
    f1 = f1_score(
        y_true,
        predictions,
        average="macro",
        zero_division=0,
    )

    print(f"\n{'=' * 55}")
    print(f"RESULTADOS: {model_name}")
    print(f"{'=' * 55}")

    for text, expected, predicted in zip(
        X, y_true, predictions
    ):
        status = "ACERTO" if expected == predicted else "ERRO"

        print(f"\n[{status}]")
        print(f"Mensagem: {text}")
        print(f"Esperado: {expected}")
        print(f"Predito:  {predicted}")

    print("\nClassification Report:")
    print(
        classification_report(
            y_true,
            predictions,
            zero_division=0,
        )
    )

    print("Matriz de confusão:")
    print(confusion_matrix(y_true, predictions))

    return {
        "modelo": model_name,
        "accuracy": accuracy,
        "f1_macro": f1,
        "predictions": predictions,
    }


def main():

    X = [case[0] for case in TEST_CASES]
    y_true = [case[1] for case in TEST_CASES]

    result_v1 = evaluate_model(
        "V1",
        MODEL_V1_PATH,
        X,
        y_true,
    )

    result_v2 = evaluate_model(
        "V2",
        MODEL_V2_PATH,
        X,
        y_true,
    )

    print("\n===== COMPARAÇÃO FINAL =====")

    print(
        f"V1 Accuracy: {result_v1['accuracy']:.2%}"
    )
    print(
        f"V2 Accuracy: {result_v2['accuracy']:.2%}"
    )

    print(
        f"V1 F1 Macro: {result_v1['f1_macro']:.2%}"
    )
    print(
        f"V2 F1 Macro: {result_v2['f1_macro']:.2%}"
    )

    print("\n===== MENSAGENS COM RESULTADOS DIFERENTES =====")

    for text, expected, pred_v1, pred_v2 in zip(
        X,
        y_true,
        result_v1["predictions"],
        result_v2["predictions"],
    ):
        if pred_v1 != pred_v2:
            print(f"\nMensagem: {text}")
            print(f"Esperado: {expected}")
            print(f"V1: {pred_v1}")
            print(f"V2: {pred_v2}")


if __name__ == "__main__":
    main()

