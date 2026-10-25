
from fastapi.testclient import TestClient
from router.predict_router import verify_token
from main import app


client = TestClient(app)

PREDICT_URL = "/predict"


def fake_verify_token():
    """Simula um usuário autenticado para testar a rota."""
    return {
        "user_id": 1,
        "email": "teste@fintechguard.local",
        "name": "Usuário de Teste",
        "role": "user",
    }


def test_predict_without_token():
    """A rota deve rejeitar requisições sem token JWT."""

    response = client.post(
        PREDICT_URL,
        json={
            "ticket_description": "Não consigo acessar minha conta",
            "ticket_subject": "Problema de acesso",
        },
    )

    assert response.status_code == 401


def test_predict_with_invalid_token():
    """A rota deve rejeitar um token inválido."""

    response = client.post(
        PREDICT_URL,
        headers={"Authorization": "Bearer token-invalido"},
        json={
            "ticket_description": "Não consigo acessar minha conta",
            "ticket_subject": "Problema de acesso",
        },
    )

    assert response.status_code == 401


def test_predict_with_valid_token():
    """A rota deve responder corretamente para um usuário autenticado."""

    app.dependency_overrides[verify_token] = fake_verify_token

    try:
        response = client.post(
            PREDICT_URL,
            json={
                "ticket_description": "Não consigo acessar minha conta",
                "ticket_subject": "Problema de acesso",
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert data["status"] == "success"
        assert data["predicted_category"] == "Technical Issue"
        assert data["confidence"] == 0.95

    finally:
        app.dependency_overrides.pop(verify_token, None)


def test_predict_with_missing_description():
    """A API deve rejeitar uma descrição ausente."""

    app.dependency_overrides[verify_token] = fake_verify_token

    try:
        response = client.post(
            PREDICT_URL,
            json={
                "ticket_subject": "Problema de acesso",
            },
        )

        assert response.status_code == 422

    finally:
        app.dependency_overrides.pop(verify_token, None)
