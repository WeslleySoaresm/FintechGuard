
from collections import Counter
from sqlmodel import Session, select

from data.db import engine
from models.model_events import Ticket


GENERIC_TEXT = (
    "relata um problema relacionado a fraud. "
    "solicita análise e orientação."
)


def main():
    with Session(engine) as session:
        statement = select(Ticket).where(
            Ticket.ticket_type == "Fraud"
        )
        tickets = session.exec(statement).all()

    total = len(tickets)
    generic = 0
    empty = 0
    useful = 0

    subjects = Counter()
    descriptions = Counter()
    statuses = Counter()
    priorities = Counter()

    for ticket in tickets:
        subject = (ticket.ticket_subject or "").strip()
        description = (ticket.ticket_description or "").strip()

        subjects[subject] += 1
        statuses[ticket.ticket_status or "Sem status"] += 1
        priorities[ticket.ticket_priority or "Sem prioridade"] += 1

        if not description:
            empty += 1
        elif GENERIC_TEXT in description.lower():
            generic += 1
        else:
            useful += 1

        descriptions[description] += 1

    print("\n===== QUALIDADE DOS REGISTROS DE FRAUDE =====")
    print(f"Total: {total}")
    print(f"Descrições genéricas: {generic}")
    print(f"Descrições vazias: {empty}")
    print(f"Outras descrições: {useful}")

    print("\n===== ASSUNTOS MAIS FREQUENTES =====")
    for subject, count in subjects.most_common(15):
        print(f"{count:5} | {subject}")

    print("\n===== DESCRIÇÕES MAIS REPETIDAS =====")
    for description, count in descriptions.most_common(10):
        print(f"{count:5} | {description[:120]}")

    print("\n===== DISTRIBUIÇÃO DE STATUS =====")
    for status, count in statuses.most_common():
        print(f"{count:5} | {status}")

    print("\n===== DISTRIBUIÇÃO DE PRIORIDADE =====")
    for priority, count in priorities.most_common():
        print(f"{count:5} | {priority}")


if __name__ == "__main__":
    main()
