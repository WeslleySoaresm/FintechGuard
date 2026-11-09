from collections import Counter

from sqlmodel import Session, select

from data.db import engine
from models.model_events import Ticket


def main():
    with Session(engine) as session:

        statement = select(Ticket)
        tickets = session.exec(statement).all()

        print("=" * 50)
        print("DIAGNÓSTICO DO DATASET FINTECHGUARD")
        print("=" * 50)

        print(f"\nTotal de tickets: {len(tickets)}")

        # Distribuição das classes
        classes = Counter(
            ticket.ticket_type.strip()
            for ticket in tickets
            if ticket.ticket_type
            and ticket.ticket_type.strip()
        )

        print("\nDISTRIBUIÇÃO DAS CLASSES")

        for classe, quantidade in classes.most_common():
            percentual = quantidade / len(tickets) * 100

            print(
                f"{classe}: {quantidade} "
                f"({percentual:.2f}%)"
            )

        # Registros sem classificação
        sem_tipo = sum(
            not ticket.ticket_type
            or not ticket.ticket_type.strip()
            for ticket in tickets
        )

        # Registros sem assunto
        sem_assunto = sum(
            not ticket.ticket_subject
            or not ticket.ticket_subject.strip()
            for ticket in tickets
        )

        # Registros sem descrição
        sem_descricao = sum(
            not ticket.ticket_description
            or not ticket.ticket_description.strip()
            for ticket in tickets
        )

        # Registros sem assunto e descrição
        sem_texto = sum(
            not (
                (ticket.ticket_subject or "").strip()
                or (ticket.ticket_description or "").strip()
            )
            for ticket in tickets
        )

        # Duplicidade de assunto + descrição + classe
        combinacoes = [
            (
                (ticket.ticket_subject or "").strip().lower(),
                (ticket.ticket_description or "").strip().lower(),
                (ticket.ticket_type or "").strip().lower()
            )
            for ticket in tickets
        ]

        duplicados = len(combinacoes) - len(set(combinacoes))

        print("\nQUALIDADE DOS DADOS")
        print(f"Sem classificação: {sem_tipo}")
        print(f"Sem assunto: {sem_assunto}")
        print(f"Sem descrição: {sem_descricao}")
        print(f"Sem assunto e descrição: {sem_texto}")
        print(f"Combinações duplicadas: {duplicados}")

        print("\nEXEMPLOS ANONIMIZADOS")

        for ticket in tickets[:5]:
            print({
                "subject": ticket.ticket_subject,
                "description": ticket.ticket_description,
                "type": ticket.ticket_type
            })


if __name__ == "__main__":
    main()