from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Ticket(Base):
    __tablename__ = "tickets"

    # Chave primária gerada pelo banco de dados
    id = Column(Integer, primary_key=True, index=True)

    # Identificador do Ticket do dataset original
    ticket_id = Column(Integer, unique=True, index=True, nullable=False)

    # Informações do Cliente
    customer_name = Column(String(255), nullable=False)
    customer_email = Column(String(255), index=True, nullable=False)
    customer_age = Column(Integer, nullable=True)
    customer_gender = Column(String(50), nullable=True)

    # Informações do Produto / Compra
    product_purchased = Column(String(255), nullable=True)
    date_of_purchase = Column(DateTime, nullable=True)

    # Detalhes do Chamado (Ticket)
    ticket_type = Column(String(100), nullable=True)
    ticket_subject = Column(String(255), nullable=False)
    ticket_description = Column(Text, nullable=True)
    ticket_status = Column(String(50), default="Open", index=True)
    ticket_priority = Column(String(50), nullable=True)
    ticket_channel = Column(String(50), nullable=True)

    # Atendimento e Resolução
    first_response_time = Column(DateTime, nullable=True)
    time_to_resolution = Column(DateTime, nullable=True)
    resolution = Column(Text, nullable=True)
    customer_satisfaction_rating = Column(Float, nullable=True)

    # Auditoria interna
    created_at = Column(DateTime, default=datetime.utcnow)