from typing import Optional
from fastapi import APIRouter, HTTPException, status, Depends
import pandas as pd
from data import db
from data.db import CSV_PATH, df
from schemas.ticket import TicketCreate
from utils.helpers  import find_ticket_by_id, get_next_ticket_id, sanitize_text
from utils.auth import verify_token


router = APIRouter(prefix="/tickets", tags=["Tickets"])

@router.post("/{create_user}", status_code=status.HTTP_201_CREATED)
def create_ticket(ticket: TicketCreate, user_data: dict = Depends(verify_token)):
    global df
    
   # Sanitização manual de campos específicos, se necessário:
    clean_name = sanitize_text(ticket.customer_name)
    clean_description = sanitize_text(ticket.ticket_description)
    
    # Se não enviou ticket_id, chama a função auxiliar
    #Helpers para calcular o proximo id
    next_id = ticket.ticket_id or get_next_ticket_id(df)

    # Mapeamento completo entre o schema e os nomes das colunas no CSV
    new_data = {
        "Ticket ID": next_id,
        "Customer Name": ticket.customer_name,
        "Customer Email": ticket.customer_email,
        "Customer Age": ticket.customer_age,
        "Customer Gender": ticket.customer_gender,
        "Product Purchased": ticket.product_purchased,
        "Date of Purchase": ticket.date_of_purchase,
        "Ticket Type": ticket.ticket_type,
        "Ticket Subject": ticket.ticket_subject,
        "Ticket Description": ticket.ticket_description,
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

    # Persiste no arquivo mantendo a limpeza das colunas Unnamed
    db.df.to_csv(db.CSV_PATH, index=False)

    return new_data

@router.get("/")
def read_tickets(skip: int = 0, limit: int = 100):
    paginated_df = df.iloc[skip : skip + limit].where(pd.notnull(df), None)
    return paginated_df.to_dict(orient="records")


@router.get("/{ticket_id}")
def read_ticket(ticket_id: int):
    # Usa a função auxiliar
    ticket = find_ticket_by_id(ticket_id)
    
    # Trata valores nulos para o JSON
    ticket_clean = ticket.where(pd.notnull(ticket), None)
    return ticket_clean.to_dict(orient="records")[0]


@router.delete("/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ticket(ticket_id: int, user_data: dict = Depends(verify_token)):
    # Reutiliza a busca (se não existir, já lança o erro 404 automaticamente)
    find_ticket_by_id(ticket_id)

    # Remove o ticket filtrando o DataFrame
    numeric_ids = pd.to_numeric(db.df["Ticket ID"], errors="coerce")
    db.df = db.df[numeric_ids != ticket_id]

    # Salva as alterações no arquivo CSV
    db.df.to_csv(db.CSV_PATH, index=False)

    return None
        