import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine, select
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


@pytest.fixture(autouse=True)
def setup_database():
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


@pytest.fixture
def unauthenticated_client():
    def override_get_session():
        with Session(test_engine) as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session
    app.dependency_overrides.pop(verify_token, None)

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


def create_ticket(user_id: int) -> int:
    with Session(test_engine) as session:
        ticket = Ticket(
            user_id=user_id,
            customer_name=f"Cliente {user_id}",
            customer_email=f"cliente{user_id}@teste.com",
            ticket_subject="Problema no cartão",
        )
        session.add(ticket)
        session.commit()
        session.refresh(ticket)
        return ticket.id


# =========================================================
# TESTES DO AGENTE
# =========================================================

def test_agent_sem_token_deve_retornar_401(unauthenticated_client):
    response = unauthenticated_client.post(
        "/agent",
        json={"message": "Quero informações sobre minha conta."},
    )

    assert response.status_code == 401


def test_agent_autenticado_deve_processar_mensagem(client):
    response = client.post(
        "/agent",
        json={"message": "Quero saber sobre minha cobrança."},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["intent"] == "Billing"
    assert data["risk_level"] == "low"
    assert data["requires_human"] is False
    assert isinstance(data["response"], str)
    assert len(data["response"]) > 0


def test_agent_deve_aceitar_ticket_do_proprio_usuario(client):
    ticket_id = create_ticket(user_id=1)

    response = client.post(
        "/agent",
        json={
            "message": "Quero informações sobre meu cartão.",
            "ticket_id": ticket_id,
        },
    )

    assert response.status_code == 200


def test_agent_nao_deve_aceitar_ticket_de_outro_usuario(client):
    ticket_id = create_ticket(user_id=2)

    response = client.post(
        "/agent",
        json={
            "message": "Quero informações sobre esse ticket.",
            "ticket_id": ticket_id,
        },
    )

    assert response.status_code == 404


def test_agent_ticket_inexistente_deve_retornar_404(client):
    response = client.post(
        "/agent",
        json={
            "message": "Quero informações sobre esse ticket.",
            "ticket_id": 999999,
        },
    )

    assert response.status_code == 404


def test_agent_nao_deve_aceitar_campo_extra(client):
    response = client.post(
        "/agent",
        json={
            "message": "Preciso de ajuda.",
            "campo_inventado": "valor",
        },
    )

    assert response.status_code == 422


def test_agent_nao_deve_aceitar_mensagem_vazia(client):
    response = client.post(
        "/agent",
        json={"message": "   "},
    )

    assert response.status_code == 422
    
    
def test_agent_deve_salvar_mensagem_do_cliente_e_resposta(client):
    from models.model_events import ConversationMessage

    ticket_id = create_ticket(user_id=1)

    response = client.post(
        "/agent",
        json={
            "message": "Quero saber sobre minha cobrança.",
            "ticket_id": ticket_id,
        },
    )

    assert response.status_code == 200

    with Session(test_engine) as session:
        messages = session.exec(
            select(ConversationMessage).where(
                ConversationMessage.ticket_id == ticket_id
            )
        ).all()

    assert len(messages) == 2

    senders = {message.sender_type for message in messages}

    assert senders == {"CUSTOMER", "AGENT"}


def test_agent_sem_ticket_nao_deve_salvar_historico(client):
    from models.model_events import ConversationMessage

    response = client.post(
        "/agent",
        json={
            "message": "Quero saber sobre minha cobrança.",
        },
    )

    assert response.status_code == 200

    with Session(test_engine) as session:
        messages = session.exec(
            select(ConversationMessage)
        ).all()

    assert len(messages) == 0