
from collections import defaultdict, Counter

from sqlmodel import Session, select

from data.db import engine
from models.model_events import Ticket


CATEGORY_MAPPING = {
    "cobrança": "Billing",
    "billing": "Billing",
    "billing inquiry": "Billing",
    "suporte técnico": "Technical Issue",
    "technical issue": "Technical Issue",
    "fraud": "Fraud",
    "security": "Security",
    "card": "Card",
    "transaction": "Transaction",
    "account access": "Account Access",
    "loan": "Loan",
    "cancellation request": "Cancellation",
    "product inquiry": "Product Inquiry",
    "refund request": "Refund",
}


def main():
    with Session(engine) as session:
        tickets = session.exec(select(Ticket)).all()

    grouped = defaultdict(Counter)
    unmapped = Counter()

    for ticket in tickets:
        original = (ticket.ticket_type or "").strip()
        normalized = CATEGORY_MAPPING.get(original.lower())

        if normalized:
            grouped[normalized][original] += 1
        else:
            unmapped[original or "SEM CLASSIFICAÇÃO"] += 1

    print("\n===== PROPOSTA DE PADRONIZAÇÃO =====")

    for normalized, originals in sorted(grouped.items()):
        total = sum(originals.values())

        print(f"\n{normalized}: {total} registros")

        for original, count in originals.items():
            print(f"  {original}: {count}")

    print("\n===== CATEGORIAS NÃO MAPEADAS =====")

    for original, count in unmapped.most_common():
        print(f"{original}: {count}")

    print("\n===== TOTAL =====")
    print(f"Registros analisados: {len(tickets)}")
    print(f"Registros mapeados: {sum(map(sum, grouped.values()))}")
    print(f"Registros não mapeados: {sum(unmapped.values())}")


if __name__ == "__main__":
    main()
