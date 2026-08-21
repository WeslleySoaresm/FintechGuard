from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


# Base com todos os campos compartilhados
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator
from utils.helpers import sanitize_field, sanitize_text

class TicketBase(BaseModel):
    customer_name: str
    customer_email: str
    customer_age: Optional[int] = Field(default=None, ge=0, le=120)
    customer_gender: Optional[str] = None

    product_purchased: Optional[str] = None
    date_of_purchase: Optional[datetime] = None

    ticket_type: Optional[str] = None
    ticket_subject: str
    ticket_description: Optional[str] = None
    ticket_status: Optional[str] = "Open"
    ticket_priority: Optional[str] = None
    ticket_channel: Optional[str] = None

    first_response_time: Optional[datetime] = None
    time_to_resolution: Optional[datetime] = None
    resolution: Optional[str] = None
    customer_satisfaction_rating: Optional[float] = Field(
        default=None, ge=1.0, le=5.0
    )

    @field_validator(
        "customer_name",
        "customer_email",
        "product_purchased",
        "ticket_type",
        "ticket_subject",
        "ticket_description",
        "resolution",
        "ticket_priority",
        "ticket_channel",
        mode="before"
    )
    @classmethod
    def apply_sanitization(cls, value: Optional[str]) -> Optional[str]:
        return sanitize_field(value)
    
# Schema para recepção de requisições de criação (POST)
class TicketCreate(TicketBase):
    pass


class TicketResponse(TicketBase):
    ticket_id: int

    class Config:
        from_attributes = True


# Schema para atualização parcial de tickets (PATCH / PUT)
class TicketUpdate(BaseModel):
    ticket_status: Optional[str] = None
    ticket_priority: Optional[str] = None
    resolution: Optional[str] = None
    customer_satisfaction_rating: Optional[float] = None


# Schema de resposta da API (GET)
class TicketResponse(TicketBase):
    id: int
    ticket_id: int
    created_at: datetime

    # Compatibilidade com Pydantic v2 para leitura direta do SQLAlchemy
    model_config = ConfigDict(from_attributes=True)