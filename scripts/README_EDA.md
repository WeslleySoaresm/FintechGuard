
# 🛡️ FintechGuard - Sistema de Atendimento com IA & API FastAPI
**Projeto de Bloco: Análise e Segurança de Agentes de IA — TP1**

## 🎯 Objetivo do Projeto
O objetivo deste projeto é construir a base estrutural de um sistema de atendimento ao cliente impulsionado por inteligência artificial. Nesta etapa inicial (TP1), é realizada a **Análise Exploratória de Dados (EDA)** em um dataset de suporte, identificando intenções e padrões de chamados, aliada à configuração da **API FastAPI modular** protegida por autenticação via token JWT.

---

## 📄 Escolha e Documentação do Dataset

* **Nome do Dataset:** Customer Support Ticket Dataset
* **Fonte:** [Kaggle — Customer Support Ticket Dataset](https://www.kaggle.com/datasets/suraj520/customer-support-ticket-dataset)
* **Licença:** Apache 2.0
* **Razão da Escolha:** O dataset é composto por **8.469 amostras** (superando a exigência mínima de 500 registros) e contempla colunas essenciais para classificação de intenção, como descrição do chamado (`Ticket Description`), assunto (`Ticket Subject`), tipo de ticket (`Ticket Type`), canal de atendimento (`Ticket Channel`) e prioridade (`Ticket Priority`).

---

## 📊 Análise Exploratória de Dados (EDA)

### 1. Visão Geral da Estrutura
* **Shape:** 8.469 linhas e 17 colunas.
* **Duplicatas:** 0 registros duplicados.
* **Valores Ausentes:** 
  * `Resolution`: 5.700 nulos (67,3%)
  * `Time to Resolution`: 5.700 nulos (67,3%)
  * `Customer Satisfaction Rating`: 5.700 nulos (67,3%)
  * `First Response Time`: 2.819 nulos (33,3%)
  
> **Decisão de Limpeza:** Os valores nulos foram mantidos na base tratada (`data/customer_support_tickets_cleaned.csv`), pois são **nulos estruturais**: refletem o ciclo de vida do chamado (tickets em aberto ainda não possuem tempo de resolução ou avaliação de satisfação).

### 2. Distribuição da Variável-Alvo (`Ticket Type`)
A variável `Ticket Type` representa a intenção principal do cliente:
* **Refund request:** 1.752 registros (20,69%)
* **Technical issue:** 1.747 registros (20,63%)
* **Cancellation request:** 1.695 registros (20,01%)
* **Product inquiry:** 1.641 registros (19,38%)
* **Billing inquiry:** 1.634 registros (19,29%)

### 3. Hipóteses Formuladas sobre as Intenções dos Usuários
1. **Perfeito Balanceamento das Classes:** Como todas as 5 categorias de intenção giram em torno de 20%, o modelo de IA treinado com essa base não sofrerá de viés (bias) derivado de desbalanceamento de classes.
2. **Foco em Demandas Financeiras e Cancelamento:** A soma de solicitações de reembolso (`Refund request`) e cancelamento (`Cancellation request`) compõe mais de 40% dos chamados, indicando que fricções pós-compra são a maior fonte de atendimento.
3. **Independência de Canais:** Os chamados dividem-se de maneira uniforme entre os 4 canais disponíveis (`Email`, `Phone`, `Social Media` e `Chat`), indicando que o canal escolhido pelo cliente não é um fator determinante para prever a intenção.

---

## 💻 Código de Análise Exploratória (`eda.py`)

```python
"""
===============================================================================
PROJETO DE BLOCO: Análise e Segurança de Agentes de IA - TP1
Arquivo: eda.py
Descrição: Análise Exploratória de Dados (EDA) e limpeza do dataset de tickets.
===============================================================================
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def executar_eda():
    # 1. CARREGAMENTO DO DATASET
    caminho_dataset = "data/customer_support_tickets.csv"
    
    if not os.path.exists(caminho_dataset):
        print(f"Erro: Arquivo '{caminho_dataset}' não encontrado.")
        return

    df = pd.read_csv(caminho_dataset)
    print(">>> Dataset carregado com sucesso!\n")

    # 2. ANÁLISE ESTRUTURAL (SHAPE E DTYPES)
    print(f"Dimensões da base: {df.shape[0]} linhas e {df.shape[1]} colunas\n")
    print("--- Tipos de Dados ---")
    print(df.dtypes)
    print("\n" + "=" * 80 + "\n")

    # 3. DIAGNÓSTICO DE VALORES AUSENTES E DUPLICATAS
    print("--- Contagem de Valores Ausentes ---")
    print(df.isnull().sum())
    
    qtd_duplicatas = df.duplicated().sum()
    print(f"\nTotal de linhas duplicadas: {qtd_duplicatas}")
    print("\n" + "=" * 80 + "\n")

    # 4. ESTATÍSTICAS DESCRITIVAS
    print("--- Resumo Estatístico ---")
    print(df.describe(include="all"))
    print("\n" + "=" * 80 + "\n")

    # 5. DISTRIBUIÇÃO DA VARIÁVEL ALVO (Ticket Type)
    print("--- Frequência Absoluta (Ticket Type) ---")
    print(df['Ticket Type'].value_counts(dropna=False))

    print("\n--- Frequência Relativa (%) ---")
    print((df['Ticket Type'].value_counts(normalize=True) * 100).round(2))
    print("\n" + "=" * 80 + "\n")

    # 6. LIMPEZA, TRATAMENTO E EXPORTAÇÃO
    df_cleaned = df.copy()
    df_cleaned = df_cleaned.drop_duplicates()

    df_cleaned["Ticket Type"] = df_cleaned["Ticket Type"].replace({"Cobrança": "Billing Inquiry"})
    df_cleaned["Customer Gender"] = df_cleaned["Customer Gender"].replace({"Feminino": "Female"})

    os.makedirs("data", exist_ok=True)
    caminho_destino = "data/customer_support_tickets_cleaned.csv"
    df_cleaned.to_csv(caminho_destino, index=False)
    print(f">>> Dataset limpo salvo com sucesso em: '{caminho_destino}'\n")

    # 7. VISUALIZACÕES GRÁFICAS
    os.makedirs("graphs", exist_ok=True)
    
    sns.set_theme(style="whitegrid")
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # Gráfico 1: Tipo de Ticket (Variável Alvo)
    sns.countplot(
        data=df_cleaned, 
        y="Ticket Type", 
        order=df_cleaned["Ticket Type"].value_counts().index, 
        ax=axes[0], 
        palette="viridis"
    )
    axes[0].set_title("Distribuição do Tipo de Ticket (Alvo)")
    axes[0].set_xlabel("Quantidade")

    # Gráfico 2: Prioridade do Chamado
    sns.countplot(
        data=df_cleaned, 
        x="Ticket Priority", 
        order=["Low", "Medium", "High", "Critical"], 
        ax=axes[1], 
        palette="magma"
    )
    axes[1].set_title("Distribuição da Prioridade")
    axes[1].set_ylabel("Quantidade")

    # Gráfico 3: Canal de Atendimento
    sns.countplot(
        data=df_cleaned, 
        x="Ticket Channel", 
        order=df_cleaned["Ticket Channel"].value_counts().index, 
        ax=axes[2], 
        palette="mako"
    )
    axes[2].set_title("Distribuição do Canal de Suporte")
    axes[2].set_ylabel("Quantidade")

    plt.tight_layout()
    caminho_grafico = "graphs/eda_visualizations.png"
    plt.savefig(caminho_grafico)
    print(f">>> Gráficos gerados e salvos em: '{caminho_grafico}'")
    plt.show()


if __name__ == "__main__":
    executar_eda()

```

---

## 📁 Estrutura do Projeto

```text
.
├── data/
│   ├── customer_support_tickets.csv
│   └── customer_support_tickets_cleaned.csv
├── graphs/
│   └── eda_visualizations.png
├── router/
│   ├── auth_router.py
│   └── ticket_router.py
├── schemas/
│   └── auth.py
├── templates/
│   ├── dashboard.html
│   └── login.html
├── utils/
│   └── auth.py
├── eda.py
├── main.py
├── README.md
└── requirements.txt

```

---

## ⚙️ Instruções de Instalação e Execução

### 1. Configurar o Ambiente Virtual

```bash
# Criar o ambiente virtual
python -m venv venv

# Ativar o ambiente virtual (Linux/macOS)
source venv/bin/activate

# Ativar o ambiente virtual (Windows PowerShell)
.\venv\Scripts\Activate.ps1

```

### 2. Instalar as Dependências

```bash
pip install -r requirements.txt

```

### 3. Executar a Análise Exploratória (EDA)

```bash
python eda.py

```

### 4. Executar a API FastAPI

```bash
uvicorn main:app --reload

```

Acesse a aplicação no seu navegador:

* **Interface de Login:** `[http://127.0.0.1:8000/login](http://127.0.0.1:8000/login)`
* **Documentação Swagger API:** `[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)`

```