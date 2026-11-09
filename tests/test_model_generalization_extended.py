
from pathlib import Path

import joblib
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "agents" / "intent_classifier.joblib"

# Mensagens inéditas para avaliação diagnóstica.
TEST_CASES = [
    # Billing inquiry
    ("Gostaria de consultar o valor da minha última fatura.", "billing inquiry"),
    ("Why was I charged this monthly maintenance fee?", "billing inquiry"),
    ("Preciso entender uma cobrança que apareceu no extrato.", "billing inquiry"),
    ("Can you explain the fees applied to my account?", "billing inquiry"),

    # Cancellation request
    ("Quero encerrar minha conta bancária definitivamente.", "cancellation request"),
    ("Please stop my subscription immediately.", "cancellation request"),
    ("Desejo cancelar o serviço contratado.", "cancellation request"),
    ("I no longer want to use this financial product.", "cancellation request"),

    # Product inquiry
    ("Quais são as vantagens do cartão premium?", "product inquiry"),
    ("What are the interest rates for your savings account?", "product inquiry"),
    ("Quero conhecer as opções de investimento disponíveis.", "product inquiry"),
    ("Does your bank offer international transfers?", "product inquiry"),

    # Refund request
    ("Fui cobrado duas vezes e quero receber o dinheiro de volta.", "refund request"),
    ("Please return the amount debited from my account.", "refund request"),
    ("Solicito o reembolso de uma compra que foi cancelada.", "refund request"),
    ("I paid for the same service twice. I need a refund.", "refund request"),

    # Technical issue
    ("Não consigo acessar o aplicativo pelo meu celular.", "technical issue"),
    ("The mobile application crashes whenever I try to log in.", "technical issue"),
    ("O site apresenta uma mensagem de erro ao carregar.", "technical issue"),
    ("My account dashboard is not loading correctly.", "technical issue"),
]


def main():
    model = joblib.load(MODEL_PATH)

    texts = [text for text, _ in TEST_CASES]
    expected = [intent for _, intent in TEST_CASES]

    predictions = model.predict(texts)

    accuracy = accuracy_score(expected, predictions)

    print("\n===== TESTE DE GENERALIZAÇÃO =====")
    print(f"Total de mensagens: {len(texts)}")
    print(f"Acertos: {sum(a == p for a, p in zip(expected, predictions))}")
    print(f"Erros: {sum(a != p for a, p in zip(expected, predictions))}")
    print(f"Accuracy: {accuracy:.4f} ({accuracy * 100:.2f}%)")

    print("\n===== RESULTADO INDIVIDUAL =====")

    for text, actual, predicted in zip(texts, expected, predictions):
        status = "ACERTO" if actual == predicted else "ERRO"

        print(f"\n[{status}]")
        print(f"Mensagem: {text}")
        print(f"Esperado: {actual}")
        print(f"Predito:  {predicted}")

    print("\n===== CLASSIFICATION REPORT =====")
    print(
        classification_report(
            expected,
            predictions,
            zero_division=0,
        )
    )

    print("\n===== MATRIZ DE CONFUSÃO =====")
    labels = sorted(set(expected))

    print(f"Classes: {labels}")
    print(confusion_matrix(expected, predictions, labels=labels))


if __name__ == "__main__":
    main()
