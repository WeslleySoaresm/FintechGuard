
from datetime import datetime
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=255)
    email: str = Field(max_length=255, index=True, unique=True)
    password_hash: str = Field(max_length=255)
    role: str = Field(default="CUSTOMER", max_length=50)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    tickets: List["Ticket"] = Relationship(back_populates="user")
    conversations: List["Conversation"] = Relationship(
        back_populates="user"
    )


class Ticket(SQLModel, table=True):
    __tablename__ = "tickets"

    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: int = Field(foreign_key="users.id", index=True)

    customer_name: str = Field(max_length=255)
    customer_email: str = Field(max_length=255, index=True)

    customer_age: Optional[int] = None
    customer_gender: Optional[str] = Field(default=None, max_length=50)
    product_purchased: Optional[str] = Field(default=None, max_length=255)
    date_of_purchase: Optional[datetime] = None
    ticket_type: Optional[str] = Field(default=None, max_length=100)

    ticket_subject: str = Field(max_length=255)
    ticket_description: Optional[str] = None

    ticket_status: str = Field(
        default="Open",
        max_length=50,
        index=True
    )

    ticket_priority: Optional[str] = Field(default=None, max_length=50)
    ticket_channel: Optional[str] = Field(default=None, max_length=50)
    first_response_time: Optional[datetime] = None
    time_to_resolution: Optional[datetime] = None
    resolution: Optional[str] = None

    customer_satisfaction_rating: Optional[float] = Field(
        default=None,
        ge=1.0,
        le=5.0
    )

    created_at: datetime = Field(default_factory=datetime.utcnow)

    user: Optional[User] = Relationship(back_populates="tickets")

    conversations: List["Conversation"] = Relationship(
        back_populates="ticket"
    )


class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"

    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: int = Field(foreign_key="users.id", index=True)

    ticket_id: Optional[int] = Field(
        default=None,
        foreign_key="tickets.id",
        index=True
    )

    created_at: datetime = Field(default_factory=datetime.utcnow)

    user: Optional[User] = Relationship(back_populates="conversations")

    ticket: Optional[Ticket] = Relationship(
        back_populates="conversations"
    )

    messages: List["ConversationMessage"] = Relationship(
        back_populates="conversation"
    )


class ConversationMessage(SQLModel, table=True):
    __tablename__ = "conversation_messages"

    id: Optional[int] = Field(default=None, primary_key=True)

    conversation_id: int = Field(
        foreign_key="conversations.id",
        index=True
    )

    ticket_id: Optional[int] = Field(
        default=None,
        foreign_key="tickets.id",
        index=True
    )

    sender_type: str = Field(max_length=20)

    message: str

    created_at: datetime = Field(default_factory=datetime.utcnow)

    conversation: Optional[Conversation] = Relationship(
        back_populates="messages"
    )

    ticket: Optional[Ticket] = Relationship()
