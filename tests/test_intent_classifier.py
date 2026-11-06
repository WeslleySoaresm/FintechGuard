import pytest

from agents.intent_classifier import classify_intent


@pytest.mark.parametrize(
    "message, expected",
    [
        (
            "Meu cartão foi clonado.",
            "Fraud",
        ),
        (
            "Não reconheço essa compra.",
            "Fraud",
        ),
        (
            "Não consigo acessar minha conta.",
            "Account Access",
        ),
        (
            "Minha senha não funciona.",
            "Account Access",
        ),
        (
            "Meu cartão foi recusado.",
            "Card",
        ),
        (
            "Não consigo realizar um PIX.",
            "Transaction",
        ),
        (
            "Minha fatura está incorreta.",
            "Billing",
        ),
        (
            "Quero solicitar um reembolso.",
            "Refund",
        ),
        (
            "O aplicativo não funciona.",
            "Technical Issue",
        ),
        (
            "Quero solicitar um empréstimo.",
            "Loan",
        ),
        (
            "Gostaria de saber o horário de atendimento.",
            "Other",
        ),
    ],
)
def test_classify_intent(message, expected):
    assert classify_intent(message) == expected


def test_classify_intent_ignores_accents():
    assert classify_intent("Quero um emprestimo.") == "Loan"


def test_classify_intent_ignores_uppercase():
    assert classify_intent("MEU CARTÃO FOI CLONADO") == "Fraud"