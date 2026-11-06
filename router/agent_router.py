from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from agents.orchestrator import process_message
from agents.schemas import AgentRequest, AgentResponse
from data.db import get_session
from models.model_events import Ticket, ConversationMessage
from utils.auth import verify_token


router = APIRouter(
    prefix="/agent",
    tags=["Agent"],
)


@router.post("", response_model=AgentResponse)
def chat_with_agent(
    payload: AgentRequest,
    current_user: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    ticket = None

    # 1. Verifica se o ticket pertence ao usuário autenticado.
    if payload.ticket_id is not None:
        statement = select(Ticket).where(
            Ticket.id == payload.ticket_id,
            Ticket.user_id == current_user["user_id"],
        )

        ticket = session.exec(statement).first()

        if ticket is None:
            raise HTTPException(
                status_code=404,
                detail="Ticket não encontrado.",
            )

    # 2. Processa a mensagem.
    result = process_message(payload.message)

    # 3. Monta e valida a resposta.
    agent_response = AgentResponse(**result)

    # 4. Persiste a conversa somente quando existe um ticket autorizado.
    if ticket is not None:
        customer_message = ConversationMessage(
            ticket_id=ticket.id,
            sender_type="CUSTOMER",
            message=payload.message,
        )

        agent_message = ConversationMessage(
            ticket_id=ticket.id,
            sender_type="AGENT",
            message=agent_response.response,
        )

        session.add(customer_message)
        session.add(agent_message)

        # Salva as duas mensagens na mesma transação.
        session.commit()

    return agent_response