from typing import Optional
from fastapi import APIRouter, HTTPException, status, Depends
import pandas as pd
from data import db
from data.db import CSV_PATH, df
from schemas.ticket import TicketCreate
from utils.helpers import find_ticket_by_id, get_next_ticket_id, sanitize_text
from utils.auth import verify_token


router = APIRouter(prefix="/tickets", tags=["Tickets"])



@router.get("/root", status_code=status.HTTP_200_OK)
def root():
    return {"message": "API FintechGuard em execução"}



@router.post("", status_code=status.HTTP_201_CREATED)
def create_ticket(ticket: TicketCreate, user_data: dict = Depends(verify_token)):
    # Sanitização dos textos antes de salvar
    clean_name = sanitize_text(ticket.customer_name)
    clean_description = sanitize_text(ticket.ticket_description)
    
    # Obtém o ticket_id caso exista no schema ou gera o próximo automaticamente
    ticket_id = getattr(ticket, "ticket_id", None)
    next_id = ticket_id if ticket_id is not None else get_next_ticket_id(db.df)

    # Mapeamento do schema para as colunas do DataFrame
    new_data = {
        "Ticket ID": next_id,
        "Customer Name": clean_name,
        "Customer Email": ticket.customer_email,
        "Customer Age": ticket.customer_age,
        "Customer Gender": ticket.customer_gender,
        "Product Purchased": ticket.product_purchased,
        "Date of Purchase": ticket.date_of_purchase,
        "Ticket Type": ticket.ticket_type,
        "Ticket Subject": ticket.ticket_subject,
        "Ticket Description": clean_description,
        "Ticket Status": ticket.ticket_status,
        "Resolution": ticket.resolution,
        "Ticket Priority": ticket.ticket_priority,
        "Ticket Channel": ticket.ticket_channel,
        "First Response Time": ticket.first_response_time,
        "Time to Resolution": ticket.time_to_resolution,
        "Customer Satisfaction Rating": ticket.customer_satisfaction_rating,
    }

    new_df = pd.DataFrame([new_data])
    db.df = pd.concat([db.df, new_df], ignore_index=True)

    # Persiste no arquivo CSV
    db.df.to_csv(db.CSV_PATH, index=False)

    return new_data


@router.get("")
def read_tickets(skip: int = 0, limit: Optional[int] = None):
    
    # Se limit for informado, corta o DataFrame; caso contrário, retorna todos
    if limit is not None:
        paginated_df = db.df.iloc[skip : skip + limit].where(pd.notnull(db.df), None)
    else:
        paginated_df = db.df.iloc[skip:].where(pd.notnull(db.df), None)
        
    return paginated_df.to_dict(orient="records")


@router.get("/{ticket_id}")  # Adicionada a barra antes de {ticket_id}
def read_ticket(ticket_id: int):
    ticket = find_ticket_by_id(ticket_id)
    
    ticket_clean = ticket.where(pd.notnull(ticket), None)
    return ticket_clean.to_dict(orient="records")[0]


@router.delete("/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ticket(ticket_id: int, user_data: dict = Depends(verify_token)):
    find_ticket_by_id(ticket_id)

    numeric_ids = pd.to_numeric(db.df["Ticket ID"], errors="coerce")
    db.df = db.df[numeric_ids != ticket_id]

    db.df.to_csv(db.CSV_PATH, index=False)

    return None

