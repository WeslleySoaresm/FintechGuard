from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

from utils.helpers import sanitize_field


class TicketBase(BaseModel):
    
    model_config = ConfigDict(
        extra="forbid"
    )
    
    customer_name: str
    customer_email: str
    
    
    customer_age: Optional[int] = Field(
        default=None,
        ge=0,
        le=120
    )

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
        default=None,
        ge=1.0,
        le=5.0
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
    def apply_sanitization(
        cls,
        value: Optional[str]
    ) -> Optional[str]:
        return sanitize_field(value)


# Schema utilizado para criação de tickets
class TicketCreate(TicketBase):
    model_config = ConfigDict(extra="forbid")


# Schema utilizado para atualização parcial
class TicketUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ticket_status: Optional[str] = None
    ticket_priority: Optional[str] = None
    resolution: Optional[str] = None

    customer_satisfaction_rating: Optional[float] = Field(
        default=None,
        ge=1.0,
        le=5.0
    )


# Schema utilizado nas respostas da API
class TicketResponse(TicketBase):
    id: int
    user_id: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )