
from datetime import datetime, timedelta
from random import choice, randint, uniform
from faker import Faker

from sqlmodel import Session, SQLModel, create_engine

# ==========================================================
# CONFIGURAÇÃO
# ==========================================================

fake = Faker("pt_BR")

DATABASE_URL = "sqlite:///./fintechguard.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
    if DATABASE_URL.startswith("sqlite")
    else {}
)

# ==========================================================
# DADOS PARA GERAÇÃO
# ==========================================================

PRODUTOS = [
    "Cartão de crédito",
    "Cartão de débito",
    "Conta digital",
    "Conta poupança",
    "Transferência bancária",
    "Transferência internacional",
    "Empréstimo pessoal",
]

TIPOS = [
    "Fraud",
    "Account Access",
    "Transaction",
    "Card",
    "Loan",
    "Security",
    "Billing",
    "Billing inquiry",
    "Cancellation request",
    "Cobrança",
    "Product inquiry",
    "Refund request",
    "V string",
    "Suporte Técnico",
    "Technical issue",
]

STATUS = ["Open", "In Progress", "Resolved", "Closed"]

PRIORIDADES = ["Low", "Medium", "High", "Critical"]

CANAIS = ["Email", "Chat", "Phone", "Mobile App"]

ASSUNTOS = {
    "Fraud": [
        "Compra não reconhecida",
        "Possível fraude em compra online",
        "Transação suspeita",
    ],
    "Account Access": [
        "Não consigo acessar minha conta",
        "Problema na redefinição da senha",
    ],
    "Transaction": [
        "Transferência não recebida",
        "Transferência atrasada",
        "Transação pendente",
    ],
    "Card": [
        "Cartão recusado durante pagamento",
        "Problema no cartão bancário",
    ],
    "Loan": [
        "Dúvida sobre taxa do empréstimo",
        "Problema com parcela do empréstimo",
    ],
    "Security": [
        "Alerta de acesso suspeito",
        "Solicitação de verificação de segurança",
    ],
    "Billing": [
        "Cobrança duplicada na fatura",
        "Valor incorreto na fatura",
    ],
    "Billing inquiry": [
        "Dúvida sobre uma cobrança",
        "Esclarecimento sobre fatura",
    ],
    "Cancellation request": [
        "Solicitação de cancelamento de serviço",
        "Cancelamento de produto bancário",
    ],
    "Cobrança": [
        "Cobrança indevida",
        "Dúvida sobre valor cobrado",
    ],
    "Product inquiry": [
        "Dúvida sobre produto bancário",
        "Informações sobre funcionalidades do produto",
    ],
    "Refund request": [
        "Solicitação de reembolso",
        "Reembolso de transação",
    ],
    "V string": [
        "Tipo de ticket desconhecido",
    ],
    "Suporte Técnico": [
        "Problema técnico no aplicativo",
        "Falha no sistema bancário",
    ],
    "Technical issue": [
        "Technical problem in the banking application",
        "System error during a transaction",
    ],
}

RESOLUCOES = [
    "Problema analisado e resolvido.",
    "Solicitação encaminhada à equipe responsável.",
    "Transação verificada pelo sistema.",
    "Orientações fornecidas ao cliente.",
    "Procedimento de segurança concluído.",
]

# ==========================================================
# GERADOR DE TICKETS
# ==========================================================

def gerar_ticket(user_id: int) -> dict:
    """Gera um ticket fictício com dados variados."""

    nome = fake.name()
    genero = choice(["Male", "Female"])
    tipo = choice(TIPOS)
    status = choice(STATUS)
    prioridade = choice(PRIORIDADES)

    # Compra realizada entre 180 dias atrás e 2 dias atrás.
    # Isso deixa margem para resposta e resolução.
    agora = datetime.now()

    data_compra = fake.date_time_between(
        start_date="-180d",
        end_date="-2d",
    )

    email = f"cliente_{fake.uuid4()}@example.com"

    data_resposta = None
    data_resolucao = None
    resolucao = None
    satisfacao = None

    # Gera a primeira resposta para tickets atendidos.
    if status in ["In Progress", "Resolved", "Closed"]:
        data_resposta = min(
            data_compra + timedelta(minutes=randint(5, 240)),
            agora,
        )

    # Gera resolução apenas para tickets resolvidos ou fechados.
    if status in ["Resolved", "Closed"]:
        data_resolucao = min(
            data_resposta + timedelta(minutes=randint(15, 2880)),
            agora,
        )

        resolucao = choice(RESOLUCOES)
        satisfacao = round(uniform(1, 5), 1)

    return {
        "user_id": user_id,
        "customer_name": nome,
        "customer_email": email,
        "customer_age": randint(18, 85),
        "customer_gender": genero,
        "product_purchased": choice(PRODUTOS),
        "date_of_purchase": data_compra,
        "ticket_type": tipo,
        "ticket_subject": choice(ASSUNTOS[tipo]),
        "ticket_description": (
            f"{nome} relata um problema relacionado a "
            f"{tipo}. Solicita análise e orientação."
        ),
        "ticket_status": status,
        "ticket_priority": prioridade,
        "ticket_channel": choice(CANAIS),
        "first_response_time": data_resposta,
        "time_to_resolution": data_resolucao,
        "resolution": resolucao,
        "customer_satisfaction_rating": satisfacao,
    }


# ==========================================================
# INSERÇÃO NO BANCO
# ==========================================================

def main():
    # Ajuste o caminho se seus modelos estiverem em outro módulo.
    from models.model_events import User, Ticket

    SQLModel.metadata.create_all(engine)

    quantidade = 300
    user_id = 4

    with Session(engine) as session:
        user = session.get(User, user_id)

        if user is None:
            print(f"Erro: não existe um usuário com id={user_id}.")
            return

        novos_tickets = [
            Ticket(**gerar_ticket(user_id=user.id))
            for _ in range(quantidade)
        ]

        session.add_all(novos_tickets)
        session.commit()

        print(f"{len(novos_tickets)} tickets inseridos com sucesso.")
        print(f"Usuário associado: {user_id}")
        print(f"Tipos disponíveis: {len(TIPOS)}")
        print("Nomes e e-mails fictícios gerados automaticamente.")


if __name__ == "__main__":
    main()
