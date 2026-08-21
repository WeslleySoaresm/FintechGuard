import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================
# 1. CARREGAR DATASET LIMPO
# ==========================================

df = pd.read_csv("data/customer_support_tickets_cleaned.csv")


# ==========================================
# 2. CONFIGURAÇÃO
# ==========================================

sns.set_theme(style="whitegrid")


# ==========================================
# 3. GRÁFICO DE BARRAS - TIPO DE TICKET
# ==========================================

plt.figure(figsize=(10, 6))

sns.countplot(
    data=df,
    x="Ticket Type",
    order=df["Ticket Type"].value_counts().index
)

plt.title("Distribuição dos Tipos de Ticket")
plt.xlabel("Tipo de Ticket")
plt.ylabel("Quantidade")

plt.xticks(rotation=30)
plt.tight_layout()

plt.savefig("graphs/ticket_type.png")
plt.show()


# ==========================================
# 4. GRÁFICO DE BARRAS - PRIORIDADE
# ==========================================

plt.figure(figsize=(10, 6))

sns.countplot(
    data=df,
    x="Ticket Priority",
    order=df["Ticket Priority"].value_counts().index
)

plt.title("Distribuição das Prioridades dos Tickets")
plt.xlabel("Prioridade")
plt.ylabel("Quantidade")

plt.tight_layout()

plt.savefig("graphs/ticket_priority.png")
plt.show()


# ==========================================
# 5. GRÁFICO DE BARRAS - CANAL
# ==========================================

plt.figure(figsize=(10, 6))

sns.countplot(
    data=df,
    x="Ticket Channel",
    order=df["Ticket Channel"].value_counts().index
)

plt.title("Distribuição dos Canais de Atendimento")
plt.xlabel("Canal")
plt.ylabel("Quantidade")

plt.tight_layout()

plt.savefig("graphs/ticket_channel.png")
plt.show()


# ==========================================
# 6. HISTOGRAMA - IDADE
# ==========================================

plt.figure(figsize=(10, 6))

sns.histplot(
    data=df,
    x="Customer Age",
    bins=20
)

plt.title("Distribuição da Idade dos Clientes")
plt.xlabel("Idade")
plt.ylabel("Quantidade")

plt.tight_layout()

plt.savefig("graphs/customer_age.png")
plt.show()


# ==========================================
# 7. HISTOGRAMA - SATISFAÇÃO
# ==========================================

plt.figure(figsize=(10, 6))

sns.histplot(
    data=df,
    x="Customer Satisfaction Rating",
    bins=5
)

plt.title("Distribuição da Satisfação dos Clientes")
plt.xlabel("Avaliação de Satisfação")
plt.ylabel("Quantidade")

plt.tight_layout()

plt.savefig("graphs/customer_satisfaction.png")
plt.show()