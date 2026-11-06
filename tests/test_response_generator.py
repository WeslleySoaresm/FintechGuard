import pytest

from agents.response_generator import generate_response


def test_critical_risk_response():
    response = generate_response(
        intent="Fraud",
        risk_level="critical",
        requires_human=True,
    )

    assert "Não compartilhe senhas" in response
    assert "equipe especializada" in response


def test_high_risk_response():
    response = generate_response(
        intent="Fraud",
        risk_level="high",
        requires_human=True,
    )

    assert "equipe humana" in response


def test_low_risk_response():
    response = generate_response(
        intent="Billing",
        risk_level="low",
        requires_human=False,
    )

    assert "cobrança ou fatura" in response


def test_unknown_intent():
    response = generate_response(
        intent="Unknown",
        risk_level="low",
        requires_human=False,
    )

    assert "mais detalhes" in response