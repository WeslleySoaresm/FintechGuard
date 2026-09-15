
import pandas as pd
from fastapi import HTTPException, status
import pandas as pd
import html


# def retorna proximo max id
def get_next_ticket_id(df: pd.DataFrame) -> int:
    """Retorna o próximo ID numérico disponível para um novo ticket."""
    if df.empty or "Ticket ID" not in df.columns:
        return 1

    # Converte a coluna para numérico descartando valores inválidos
    numeric_ids = pd.to_numeric(df["Ticket ID"], errors="coerce")

    if numeric_ids.isna().all():
        return 1

    return int(numeric_ids.max()) + 1


# def buscar ticket

def find_ticket_by_id(ticket_id: int) -> pd.DataFrame:
    """Busca um ticket no DataFrame e lança 404 se não encontrar."""
    numeric_ids = pd.to_numeric(db.df["Ticket ID"], errors="coerce")
    ticket = db.df[numeric_ids == ticket_id]

    if ticket.empty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ticket com ID {ticket_id} não encontrado."
        )
    
    return ticket


def sanitize_text(text: str) -> str:
    """
    Remove/escapa caracteres especiais de HTML para prevenir Stored XSS.
    Exemplo: '<script>' vira '&lt;script&gt;'
    """
    if not isinstance(text, str):
        return text
    return html.escape(text.strip())

def sanitize_field(value: str | None) -> str | None:
    """Função genérica para ser usada diretamente em validadores do Pydantic."""
    if isinstance(value, str):
        return sanitize_text(value)
    return value