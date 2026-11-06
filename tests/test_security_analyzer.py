import pytest

from agents.security_analyzer import analyze_security


@pytest.mark.parametrize(
    "message, expected_risk, expected_human",
    [
        (
            "Não reconheço essa compra.",
            "high",
            True,
        ),
        (
            "Meu cartão foi clonado.",
            "high",
            True,
        ),
        (
            "Alguém está pedindo minha senha.",
            "critical",
            True,
        ),
        (
            "Tenho uma cobrança indevida.",
            "medium",
            False,
        ),
        (
            "Gostaria de saber mais sobre um empréstimo.",
            "low",
            False,
        ),
        (
            "Olá, preciso de ajuda.",
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
    assert result["requires_human"] is expected_human