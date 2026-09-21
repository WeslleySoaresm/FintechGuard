import pytest

from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine
from sqlalchemy.pool import StaticPool

from main import app
from data.db import get_session
from utils.auth import verify_token
from models.model_events import Ticket


test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


@pytest.fixture
def test_db():
    SQLModel.metadata.create_all(test_engine)

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

    yield ticket_id

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


def test_acesso_sem_token_deve_retornar_401():
    """
    Um usuário sem token JWT não deve conseguir
    acessar um endpoint protegido.
    """

    # Removemos temporariamente o override da autenticação
    app.dependency_overrides.pop(verify_token, None)

    with TestClient(app) as unauthenticated_client:
        response = unauthenticated_client.get("/tickets/1")

    assert response.status_code == 401


def test_usuario_nao_deve_acessar_ticket_de_outro_usuario(
    client,
    test_db,
):
    """
    O usuário 1 tenta acessar um ticket pertencente ao usuário 2.

    Deve ser bloqueado pela proteção BOLA.
    """

    response = client.get(f"/tickets/{test_db}")

    assert response.status_code == 404


def test_body_nao_deve_aceitar_campo_extra(client):
    """
    O endpoint deve rejeitar campos que não pertencem
    ao schema TicketCreate.

    Isso testa ConfigDict(extra='forbid').
    """

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