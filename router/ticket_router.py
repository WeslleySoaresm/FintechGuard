
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from data.db import get_session
from models.model_events import Ticket
from schemas.ticket import TicketCreate, TicketResponse
from utils.auth import verify_token
from utils.helpers import sanitize_text


router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"]
)


@router.get(
    "/root",
    status_code=status.HTTP_200_OK
)
def root():
    return {
        "message": "API FintechGuard em execução"
    }


@router.post(
    "",
    response_model=TicketResponse,
    status_code=status.HTTP_201_CREATED
)
def create_ticket(
    ticket: TicketCreate,
    current_user: dict = Depends(verify_token),
    session: Session = Depends(get_session)
):
    """
    Cria um novo ticket para o usuário autenticado.
    """

    # ID do usuário autenticado
    user_id = current_user["user_id"]

    # ---------------------------------------------------------
    # 1. Sanitizar campos de texto
    # ---------------------------------------------------------

    clean_name = sanitize_text(ticket.customer_name)

    clean_description = None

    if ticket.ticket_description:
        clean_description = sanitize_text(
            ticket.ticket_description
        )

    clean_subject = sanitize_text(
        ticket.ticket_subject
    )

    # ---------------------------------------------------------
    # 2. Criar objeto Ticket
    # ---------------------------------------------------------

    new_ticket = Ticket(
        user_id=user_id,

        customer_name=clean_name,
        customer_email=ticket.customer_email,
        customer_age=ticket.customer_age,
        customer_gender=ticket.customer_gender,
        product_purchased=ticket.product_purchased,
        date_of_purchase=ticket.date_of_purchase,

        ticket_type=ticket.ticket_type,
        ticket_subject=clean_subject,
        ticket_description=clean_description,

        ticket_status=ticket.ticket_status or "Open",
        ticket_priority=ticket.ticket_priority,
        ticket_channel=ticket.ticket_channel,

        first_response_time=ticket.first_response_time,
        time_to_resolution=ticket.time_to_resolution,
        resolution=ticket.resolution,

        customer_satisfaction_rating=(
            ticket.customer_satisfaction_rating
        )
    )

    # ---------------------------------------------------------
    # 3. Salvar no banco
    # ---------------------------------------------------------

    session.add(new_ticket)

    session.commit()

    session.refresh(new_ticket)

    return new_ticket

@router.get(
    "",
    response_model=list[TicketResponse]
)
def read_tickets(
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(verify_token),
    session: Session = Depends(get_session)
):
    """
    Retorna somente os tickets pertencentes ao
    usuário autenticado.
    """

    user_id = current_user["user_id"]

    statement = (
        select(Ticket)
        .where(Ticket.user_id == user_id)
        .offset(skip)
        .limit(limit)
    )

    tickets = session.exec(statement).all()

    return tickets


@router.get(
    "/{ticket_id}",
    response_model=TicketResponse
)
def read_ticket(
    ticket_id: int,
    current_user: dict = Depends(verify_token),
    session: Session = Depends(get_session)
):
    """
    Retorna um ticket específico somente se ele
    pertencer ao usuário autenticado.
    """

    user_id = current_user["user_id"]

    statement = select(Ticket).where(
        Ticket.id == ticket_id,
        Ticket.user_id == user_id
    )

    ticket = session.exec(statement).first()

    if ticket is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket não encontrado."
        )

    return ticket


@router.delete(
    "/{ticket_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_ticket(
    ticket_id: int,
    current_user: dict = Depends(verify_token),
    session: Session = Depends(get_session)
):
    """
    Exclui um ticket somente se ele pertencer
    ao usuário autenticado.
    """

    user_id = current_user["user_id"]

    statement = select(Ticket).where(
        Ticket.id == ticket_id,
        Ticket.user_id == user_id
    )

    ticket = session.exec(statement).first()

    if ticket is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket não encontrado."
        )

    session.delete(ticket)

    session.commit()

    return None