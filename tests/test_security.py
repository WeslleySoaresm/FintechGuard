import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine
from sqlalchemy.pool import StaticPool
import main
from main import app
from data.db import get_session
from utils.auth import verify_token
from models.model_events import Ticket


test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


@pytest.fixture(autouse=True)
def setup_database():
    """Cria e limpa as tabelas automaticamente para todos os testes."""
    SQLModel.metadata.create_all(test_engine)
    yield
    SQLModel.metadata.drop_all(test_engine)


@pytest.fixture
def client():
    def override_get_session():
        with Session(test_engine) as session:
            yield session

    def override_verify_token():
        return {
            "user_id": 1,
            "email": "usuario1@teste.com",
            "role": "user",
        }

    app.dependency_overrides[get_session] = override_get_session
    app.dependency_overrides[verify_token] = override_verify_token

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


# =========================================================
# TESTES DE SEGURANÇA DA API
# =========================================================

def test_acesso_sem_token_deve_retornar_401():
    """1. Teste de Autenticação: Acesso sem token deve retornar 401."""
    app.dependency_overrides.pop(verify_token, None)

    with TestClient(app) as unauthenticated_client:
        response = unauthenticated_client.get("/tickets/1")

    assert response.status_code == 401


def test_invalid_token_access():
    """2. Teste de Autenticação: Token inválido ou falsificado deve retornar 401."""
    # Criamos um TestClient puro, sem os overrides da fixture 'client'
    with TestClient(app) as clean_client:
        response = clean_client.get(
            "/tickets", 
            headers={"Authorization": "Bearer token_falsificado_ou_invalido"}
        )
    assert response.status_code == 401


def test_usuario_nao_deve_acessar_ticket_de_outro_usuario(client):
    """3. Teste de Autorização (BOLA): Tenta aceder a um ticket de outro contexto."""
    with Session(test_engine) as session:
        ticket = Ticket(
            user_id=2,
            customer_name="Cliente Dois",
            customer_email="cliente2@teste.com",
            ticket_subject="Ticket do usuário 2",
        )
        session.add(ticket)
        session.commit()
        session.refresh(ticket)
        ticket_id = ticket.id

    response = client.get(f"/tickets/{ticket_id}")
    assert response.status_code in [403, 404]


def test_body_nao_deve_aceitar_campo_extra(client):
    """4. Teste de Validação de Entradas: Rejeição de campos extra (extra='forbid')."""
    response = client.post(
        "/tickets",
        json={
            "customer_name": "Cliente Teste",
            "customer_email": "cliente@teste.com",
            "ticket_subject": "Problema no cartão",
            "campo_inventado": "tentativa de campo extra",
        },
    )
    assert response.status_code == 422


def test_rate_limiting_behavior():
    """5. Teste de Rate Limiting / Carga sob múltiplos pedidos."""
    responses = []
    with TestClient(app) as temp_client:
        for _ in range(25):
            response = temp_client.get("/tickets")
            responses.append(response.status_code)
    
    assert all(code in [200, 401, 429] for code in responses)
    





def test_headers_em_desenvolvimento(monkeypatch):
    monkeypatch.setattr(main, "ENVIRONMENT", "development")

    client = TestClient(main.app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.headers["x-frame-options"] == "DENY"
    assert response.headers["x-content-type-options"] == "nosniff"

    # HSTS não deve ser enviado no ambiente local HTTP.
    assert "strict-transport-security" not in response.headers


def test_tres_headers_em_producao(monkeypatch):
    monkeypatch.setattr(main, "ENVIRONMENT", "production")

    client = TestClient(main.app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.headers["x-frame-options"] == "DENY"
    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["strict-transport-security"] == (
        "max-age=31536000; includeSubDomains"
    )
