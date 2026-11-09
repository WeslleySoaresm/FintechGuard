import re

from sqlmodel import Session, select

from data.db import engine
from models.model_events import Ticket


def main():
    with Session(engine) as session:

        statement = select(Ticket).where(
            Ticket.ticket_type == "Fraud"
        )

        tickets = session.exec(statement).all()

        print("=" * 60)
        print("AUDITORIA DOS REGISTROS DE FRAUDE")
        print("=" * 60)

        print(f"\nTotal de tickets classificados como Fraud: {len(tickets)}")

        print("\nAMOSTRA DE REGISTROS:\n")

        for ticket in tickets[:20]:

            description = ticket.ticket_description or ""

            # Oculta o nome cadastrado do cliente
            if ticket.customer_name:
                description = re.sub(
                    re.escape(ticket.customer_name),
                    "[CLIENTE]",
                    description,
                    flags=re.IGNORECASE
                )

            print({
                "id": ticket.id,
                "subject": ticket.ticket_subject,
                "description": description,
                "type": ticket.ticket_type,
                "status": ticket.ticket_status,
                "priority": ticket.ticket_priority,
            })


if __name__ == "__main__":
    main()