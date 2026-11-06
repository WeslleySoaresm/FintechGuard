from collections import defaultdict

from sqlmodel import Session, select

from data.db import engine
from models.model_events import Ticket


CATEGORIAS_SUSPEITAS = {
    "string",
    "v string",
    "credito",
    "account",
}


def main():
    with Session(engine) as session:
        tickets = session.exec(
            select(Ticket).order_by(Ticket.id)
        ).all()

    encontrados = defaultdict(list)

    for ticket in tickets:
        categoria = (ticket.ticket_type or "").strip().lower()

        if categoria in CATEGORIAS_SUSPEITAS:
            encontrados[categoria].append(ticket)

    for categoria, registros in sorted(encontrados.items()):
        print("\n" + "=" * 60)
        print(f"CATEGORIA: {categoria}")
        print(f"TOTAL: {len(registros)}")
        print("=" * 60)

        for ticket in registros[:10]:
            print({
                "ticket_id": ticket.id,
                "subject": ticket.ticket_subject,
                "description": ticket.ticket_description,
                "type": ticket.ticket_type,
            })


if __name__ == "__main__":
    main()