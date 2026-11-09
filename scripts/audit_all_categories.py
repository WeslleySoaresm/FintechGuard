
from collections import Counter, defaultdict

from sqlmodel import Session, select

from data.db import engine
from models.model_events import Ticket


def normalize_description(ticket):
    description = (ticket.ticket_description or "").strip()

    # Remove o nome do cliente para não contar
    # nomes diferentes como descrições diferentes.
    if ticket.customer_name:
        description = description.replace(
            ticket.customer_name, "[CLIENTE]"
        )

    return description.lower()


def main():
    with Session(engine) as session:
        tickets = session.exec(select(Ticket)).all()

    categories = defaultdict(list)

    for ticket in tickets:
        category = (ticket.ticket_type or "SEM CLASSIFICAÇÃO").strip()
        categories[category].append(ticket)

    print("\n===== AUDITORIA GERAL POR CATEGORIA =====")
    print(f"Total de registros: {len(tickets)}")
    print(f"Total de categorias: {len(categories)}")

    for category, records in sorted(
        categories.items(),
        key=lambda item: len(item[1]),
        reverse=True
    ):
        descriptions = Counter(
            normalize_description(ticket)
            for ticket in records
        )

        generic = sum(
            1 for description in descriptions.elements()
            if "relata um problema relacionado a" in description
            and "solicita análise e orientação" in description
        )

        empty = sum(
            1 for ticket in records
            if not (ticket.ticket_description or "").strip()
        )

        print("\n----------------------------------------")
        print(f"Categoria: {category}")
        print(f"Total: {len(records)}")
        print(f"Descrições genéricas: {generic}")
        print(f"Descrições vazias: {empty}")
        print(f"Descrições distintas: {len(descriptions)}")

        print("Exemplos de assuntos:")
        for subject, count in Counter(
            ticket.ticket_subject or "SEM ASSUNTO"
            for ticket in records
        ).most_common(3):
            print(f"  {count} | {subject}")


if __name__ == "__main__":
    main()
