import pytest

from fintechguard_agents.security_analyzer import analyze_security


@pytest.mark.parametrize(
    "message, expected_risk, expected_human",
    [
        (
            "Minha senha foi roubada.",
            "critical",
            True,
        ),
        (
            "Não reconheço essa compra no meu cartão.",
            "high",
            True,
        ),
        (
            "Não autorizei essa transferência.",
            "high",
            True,
        ),
        (
            "Minha conta foi invadida.",
            "high",
            True,
        ),
        (
            "Fui cobrado duas vezes.",
            "medium",
            False,
        ),
        (
            "Gostaria de saber o horário de atendimento.",
            "low",
            False,
        ),
    ],
)
def test_analyze_security(
    message,
    expected_risk,
    expected_human,
):
    result = analyze_security(message)

    assert result["risk_level"] == expected_risk
    assert result["requires_human"] == expected_human