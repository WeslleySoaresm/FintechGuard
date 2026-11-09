import pytest

from fintechguard_agents.orchestrator import process_message


@pytest.mark.parametrize(
    "message, expected_intent, expected_risk, expected_human",
    [
        (
            "Quero saber sobre minha cobrança.",
            "Billing",
            "low",
            False,
        ),
        (
            "Não reconheço essa compra.",
            "Fraud",
            "high",
            True,
        ),
        (
            "Alguém está pedindo minha senha.",
            "Account Access",
            "critical",
            True,
        ),
        (
            "Meu cartão foi clonado.",
            "Fraud",
            "high",
            True,
        ),
        (
            "Olá, gostaria de uma informação.",
            "Other",
            "low",
            False,
        ),
    ],
)
def test_process_message(
    message,
    expected_intent,
    expected_risk,
    expected_human,
):
    result = process_message(message)

    assert result["intent"] == expected_intent
    assert result["risk_level"] == expected_risk
    assert result["requires_human"] is expected_human
    assert isinstance(result["response"], str)
    assert len(result["response"]) > 0