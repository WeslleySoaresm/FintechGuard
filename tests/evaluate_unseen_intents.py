
# Avaliação independente do classificador FintechGuard.
# Estas mensagens não devem ser adicionadas ao treinamento.
# Permite localizar a raiz do projeto durante a execução do script.
import sys
from pathlib import Path

# Obtém a pasta raiz do FintechGuard.
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Adiciona a raiz ao caminho de importação do Python.
sys.path.insert(0, str(PROJECT_ROOT))

from sklearn.metrics import classification_report, confusion_matrix
from fintechguard_agents.predict_intent import predict_intent


# Mensagens inéditas e suas categorias esperadas.
# Os exemplos foram escritos para representar solicitações reais.
TEST_CASES = [
    # Billing inquiry
    ("Minha fatura veio com um valor diferente do contratado.", "billing inquiry"),
    ("Why is my monthly statement higher this month?", "billing inquiry"),
    ("Quero entender uma cobrança que apareceu na minha conta.", "billing inquiry"),
    ("Can you explain the fees on my latest invoice?", "billing inquiry"),

    # Cancellation request
    ("Desejo encerrar minha assinatura imediatamente.", "cancellation request"),
    ("Please stop renewing my subscription.", "cancellation request"),
    ("Como faço para cancelar esse serviço?", "cancellation request"),
    ("I no longer want to use this plan.", "cancellation request"),

    # Product inquiry
    ("Quais são os benefícios da conta premium?", "product inquiry"),
    ("Does your bank offer international transfers?", "product inquiry"),
    ("Gostaria de conhecer as funcionalidades do cartão.", "product inquiry"),
    ("What are the advantages of this financial product?", "product inquiry"),

    # Refund request
    ("Quero receber de volta o dinheiro de uma compra.", "refund request"),
    ("I was charged incorrectly and want my money back.", "refund request"),
    ("Solicito o estorno do valor pago ontem.", "refund request"),
    ("Please return the amount charged to my account.", "refund request"),

    # Technical issue
    ("O aplicativo fecha sozinho quando tento acessar.", "technical issue"),
    ("I cannot log in because the application keeps crashing.", "technical issue"),
    ("A tela de transferência fica carregando e não termina.", "technical issue"),
    ("The mobile app displays an unexpected error.", "technical issue"),
]


def main():
    # Armazena as categorias reais e previstas pelo modelo.
    expected = []
    predicted = []

    print("\n=== AVALIAÇÃO COM MENSAGENS INÉDITAS ===\n")

    for message, expected_intent in TEST_CASES:
        # Executa a previsão sem modificar o modelo.
        result = predict_intent(message)

        predicted_intent = result["intent"]
        confidence = result["confidence"]

        expected.append(expected_intent)
        predicted.append(predicted_intent)

        # Exibe o resultado individual.
        status = "CORRETO" if predicted_intent == expected_intent else "ERRO"

        print(f"Mensagem: {message}")
        print(f"Esperado: {expected_intent}")
        print(f"Previsto: {predicted_intent}")
        print(f"Confiança: {confidence:.2%}")
        print(f"Resultado: {status}")
        print("-" * 60)

    # Exibe as métricas gerais.
    print("\n=== RELATÓRIO DE CLASSIFICAÇÃO ===")

    print(
        classification_report(
            expected,
            predicted,
            zero_division=0
        )
    )

    print("\n=== MATRIZ DE CONFUSÃO ===")

    labels = [
        "billing inquiry",
        "cancellation request",
        "product inquiry",
        "refund request",
        "technical issue",
    ]

    print(confusion_matrix(expected, predicted, labels=labels))


if __name__ == "__main__":
    main()
