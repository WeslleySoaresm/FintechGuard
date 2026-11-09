
import pytest

from fintechguard_agents.orchestrator import classify_message


# Testa mensagens que devem continuar sendo reconhecidas pelas regras.
@pytest.mark.parametrize(
    "message, expected",
    [
        ("Não reconheço essa compra.", "Fraud"),
        ("Alguém está pedindo minha senha.", "Account Access"),
        ("Quero saber sobre minha cobrança.", "Billing"),
        ("Meu cartão foi clonado.", "Fraud"),
        ("Olá, gostaria de uma informação.", "Other"),
    ],
)
def test_existing_rules_are_preserved(message, expected):
    # Confirma que a integração não alterou as regras antigas.
    assert classify_message(message) == expected


def test_ml_classifies_banking_message():
    # Mensagem em inglês que não deve depender de uma regra específica.
    result = classify_message(
        "I need to request a refund for my recent payment."
    )

    assert result == "Refund"


def test_ml_does_not_force_classification_outside_domain():
    # Uma saudação não deve ser classificada como intenção bancária.
    result = classify_message("Hello, how are you today?")

    assert result == "Other"
