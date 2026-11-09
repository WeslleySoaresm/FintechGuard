
from collections import defaultdict
import random
import re

from sqlmodel import Session, select

from data.db import engine
from models.model_events import Ticket


def anonymize(text, customer_name):
    text = text or ""

    if customer_name:
        text = re.sub(
            re.escape(customer_name),
            "[CLIENTE]",
            text,
            flags=re.IGNORECASE
        )

    return text


def main():
    random.seed(42)

    with Session(engine) as session:
        tickets = session.exec(select(Ticket)).all()

    categories = defaultdict(list)

    for ticket in tickets:
        category = (ticket.ticket_type or "SEM CLASSIFICAÇÃO").strip()
        categories[category].append(ticket)

    print("\n===== AMOSTRA DE ASSUNTOS E DESCRIÇÕES =====")

    for category, records in sorted(
        categories.items(),
        key=lambda item: len(item[1]),
        reverse=True
    ):
        print("\n" + "=" * 65)
        print(f"CATEGORIA: {category} | TOTAL: {len(records)}")

        samples = random.sample(records, min(3, len(records)))

        for ticket in samples:
            print("\nAssunto:", ticket.ticket_subject)
            print(
                "Descrição:",
                anonymize(
                    ticket.ticket_description,
                    ticket.customer_name
                )
            )


if __name__ == "__main__":
    main()

