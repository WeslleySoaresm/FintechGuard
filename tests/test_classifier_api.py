
import pytest

from fastapi.testclient import TestClient
from unittest.mock import patch

# Importa a aplicação principal do FintechGuard.
from main import app

# Cliente que simula requisições HTTP sem iniciar um servidor.
client = TestClient(app)


@pytest.fixture
def fake_user():
    """
    Simula um usuário autenticado.
    Evita depender do banco de dados neste teste.
    """
    return {
        "user_id": 1,
        "email": "test@fintechguard.com",
        "name": "Test User",
        "role": "customer"
    }


def test_classify_without_token():
    """
    Verifica se a API bloqueia requisições sem JWT.
    """
    response = client.post(
        "/classify/",
        json={"text": "I want a refund"}
    )

    assert response.status_code == 401


def test_classify_with_valid_token(fake_user):
    """
    Simula autenticação válida e verifica a resposta do classificador.
    """
    # Substitui temporariamente a previsão real por um resultado controlado.
    with patch(
        "router.classifier_router.predict_intent",
        return_value={
            "intent": "refund request",
            "confidence": 0.95
        }
    ):
        # Substitui a dependência JWT por um usuário de teste.
        from router.classifier_router import verify_token

        app.dependency_overrides[verify_token] = lambda: fake_user

        try:
            response = client.post(
                "/classify/",
                json={"text": "I want a refund"}
            )
        finally:
            # Remove a substituição para não afetar outros testes.
            app.dependency_overrides.clear()

    assert response.status_code == 200

    data = response.json()

    assert data["intent"] == "refund request"
    assert data["confidence"] == 0.95


def test_classify_empty_message(fake_user):
    """
    Verifica se o Pydantic rejeita uma mensagem vazia.
    """
    from router.classifier_router import verify_token

    app.dependency_overrides[verify_token] = lambda: fake_user

    try:
        response = client.post(
            "/classify/",
            json={"text": ""}
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 422


def test_classify_rejects_extra_fields(fake_user):
    """
    Verifica se campos não definidos no schema são rejeitados.
    """
    from router.classifier_router import verify_token

    app.dependency_overrides[verify_token] = lambda: fake_user

    try:
        response = client.post(
            "/classify/",
            json={
                "text": "I need help",
                "admin": True
            }
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 422

