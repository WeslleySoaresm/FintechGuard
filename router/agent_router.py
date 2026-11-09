
import logging
import os
import logging

logger = logging.getLogger(__name__)
from agents import Runner
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select

from data.db import get_session
from fintechguard_agents.customer_service_agent import customer_service_agent
from fintechguard_agents.orchestrator import process_message
from fintechguard_agents.response_generator import generate_response
from fintechguard_agents.schemas import AgentRequest, AgentResponse
from models.model_events import (
    Conversation,
    ConversationMessage,
    Ticket,
)
from utils.auth import verify_token


# --------------------------------------------------
# CONFIGURAÇÕES
# --------------------------------------------------

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

templates = Jinja2Templates(directory=TEMPLATES_DIR)

router = APIRouter(
    prefix="/agent",
    tags=["Agent"],
)


# --------------------------------------------------
# PÁGINA DO AGENTE
# --------------------------------------------------

@router.get("", response_class=HTMLResponse)
async def render_agent(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="agent.html",
    )


# --------------------------------------------------
# LISTAR CONVERSAS DO USUÁRIO
# --------------------------------------------------

@router.get("/conversations")
async def list_conversations(
    current_user: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    user_id = int(current_user["user_id"])

    statement = (
        select(Conversation)
        .where(Conversation.user_id == user_id)
        .order_by(Conversation.id.desc())
    )

    conversations = session.exec(statement).all()

    return [
        {
            "id": conversation.id,
            "ticket_id": conversation.ticket_id,
        }
        for conversation in conversations
    ]


# --------------------------------------------------
# CONSULTAR CONVERSA E MENSAGENS
# --------------------------------------------------

@router.get("/conversations/{conversation_id}")
async def get_conversation(
    conversation_id: int,
    current_user: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    user_id = int(current_user["user_id"])

    conversation_statement = select(Conversation).where(
        Conversation.id == conversation_id,
        Conversation.user_id == user_id,
    )

    conversation = session.exec(
        conversation_statement
    ).first()

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversa não encontrada.",
        )

    messages_statement = (
        select(ConversationMessage)
        .where(
            ConversationMessage.conversation_id == conversation.id
        )
        .order_by(
            ConversationMessage.created_at,
            ConversationMessage.id,
        )
    )

    messages = session.exec(messages_statement).all()

    return {
        "id": conversation.id,
        "ticket_id": conversation.ticket_id,
        "messages": [
            {
                "id": message.id,
                "sender_type": message.sender_type,
                "message": message.message,
                "created_at": message.created_at,
            }
            for message in messages
        ],
    }


# --------------------------------------------------
# CHAT COM O AGENTE
# --------------------------------------------------

@router.post("", response_model=AgentResponse)
async def chat_with_agent(
    payload: AgentRequest,
    current_user: dict = Depends(verify_token),
    session: Session = Depends(get_session),
):
    user_id = int(current_user["user_id"])

    # 1. VALIDAÇÃO DO TICKET

    ticket = None

    if payload.ticket_id is not None:
        ticket_statement = select(Ticket).where(
            Ticket.id == payload.ticket_id,
            Ticket.user_id == user_id,
        )

        ticket = session.exec(ticket_statement).first()

        if ticket is None:
            raise HTTPException(
                status_code=404,
                detail="Ticket não encontrado.",
            )

    # 2. RECUPERAR OU CRIAR CONVERSA

    if payload.conversation_id is not None:

        conversation_statement = select(Conversation).where(
            Conversation.id == payload.conversation_id,
            Conversation.user_id == user_id,
        )

        conversation = session.exec(
            conversation_statement
        ).first()

        if conversation is None:
            raise HTTPException(
                status_code=404,
                detail="Conversa não encontrada.",
            )

        # Impede associar a conversa a outro ticket.
        if (
            ticket is not None
            and conversation.ticket_id is not None
            and conversation.ticket_id != ticket.id
        ):
            raise HTTPException(
                status_code=409,
                detail="Esta conversa já está associada a outro ticket.",
            )

        # Associa o ticket caso a conversa ainda não tenha um.
        if ticket is not None and conversation.ticket_id is None:
            conversation.ticket_id = ticket.id

            session.add(conversation)
            session.commit()
            session.refresh(conversation)

    else:

        conversation = Conversation(
            user_id=user_id,
            ticket_id=ticket.id if ticket else None,
        )

        session.add(conversation)
        session.commit()
        session.refresh(conversation)

    # Guarda a associação efetiva da conversa.
    effective_ticket_id = conversation.ticket_id

    # 3. ANÁLISE DE INTENÇÃO E SEGURANÇA

    try:
        analysis = process_message(payload.message)

    except Exception:
        logger.exception(
            "Erro ao analisar a mensagem do usuário."
        )

        raise HTTPException(
            status_code=500,
            detail="Não foi possível analisar a mensagem.",
        )

    # 4. RECUPERAR HISTÓRICO

    history_statement = (
        select(ConversationMessage)
        .where(
            ConversationMessage.conversation_id == conversation.id
        )
        .order_by(
            ConversationMessage.created_at,
            ConversationMessage.id,
        )
    )

    previous_messages = session.exec(
        history_statement
    ).all()

    conversation_history = [
        {
            "role": (
                "assistant"
                if message.sender_type == "AGENT"
                else "user"
            ),
            "content": message.message,
        }
        for message in previous_messages
        if message.sender_type in {"CUSTOMER", "AGENT"}
    ]

    # 5. SALVAR MENSAGEM DO CLIENTE

    customer_message = ConversationMessage(
        conversation_id=conversation.id,
        ticket_id=effective_ticket_id,
        sender_type="CUSTOMER",
        message=payload.message,
    )

    try:
        session.add(customer_message)
        session.commit()
        session.refresh(customer_message)

    except Exception:
        session.rollback()

        logger.exception(
            "Erro ao salvar mensagem do cliente."
        )

        raise HTTPException(
            status_code=500,
            detail="Não foi possível salvar sua mensagem.",
        )

    # 6. ADICIONAR NOVA MENSAGEM AO HISTÓRICO

    conversation_history.append(
        {
            "role": "user",
            "content": payload.message,
        }
    )

    # 7. DECISÃO DE SEGURANÇA E EXECUÇÃO DO AGENTE

    if analysis["requires_human"]:

        response_text = generate_response(
            intent=analysis["intent"],
            risk_level=analysis["risk_level"],
            requires_human=True,
        )

    else:

        try:
            result = await Runner.run(
                customer_service_agent,
                input=conversation_history,
            )

            response_text = result.final_output

            if (
                not isinstance(response_text, str)
                or not response_text.strip()
            ):
                raise ValueError(
                    "O agente retornou uma resposta vazia."
                )

        except Exception:

            logger.exception(
                "Falha na execução do Customer Service Agent. "
                "Verifique a configuração da API, as ferramentas "
                "e as credenciais."
            )

            response_text = generate_response(
                intent=analysis["intent"],
                risk_level=analysis["risk_level"],
                requires_human=False,
            )

    # 8. SALVAR RESPOSTA DO AGENTE

    agent_message = ConversationMessage(
        conversation_id=conversation.id,
        ticket_id=effective_ticket_id,
        sender_type="AGENT",
        message=response_text,
    )

    try:
        session.add(agent_message)
        session.commit()

    except Exception:
            logger.exception(
                "Erro durante a execução do Customer Service Agent."
            )

            response_text = generate_response(
                intent=analysis["intent"],
                risk_level=analysis["risk_level"],
                requires_human=False,
            )

    # 9. RETORNAR RESULTADO

    return AgentResponse(
        conversation_id=conversation.id,
        intent=analysis["intent"],
        risk_level=analysis["risk_level"],
        requires_human=analysis["requires_human"],
        action=analysis["action"],
        priority=analysis["priority"],
        response=response_text,
    )
