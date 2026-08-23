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
    # =========================================================================
    # 1. CARREGAMENTO DO DATASET
    # =========================================================================
    # O Pandas carrega o arquivo CSV da pasta 'data/'. É o primeiro passo para
    # converter o arquivo em uma estrutura manipulável (DataFrame).
    caminho_dataset = "data/customer_support_tickets.csv"
    
    if not os.path.exists(caminho_dataset):
        print(f"Erro: Arquivo '{caminho_dataset}' não encontrado.")
        return

    df = pd.read_csv(caminho_dataset)
    print(">>> Dataset carregado com sucesso!\n")

    # =========================================================================
    # 2. ANÁLISE ESTRUTURAL (SHAPE E DTYPES)
    # =========================================================================
    # df.shape retorna a tupla (linhas, colunas).
    # df.dtypes detalha a tipagem de cada coluna atribuída pelo Pandas.
    print(f"Dimensões da base: {df.shape[0]} linhas e {df.shape[1]} colunas\n")
    print("--- Tipos de Dados ---")
    print(df.dtypes)
    print("\n" + "=" * 80 + "\n")

    # =========================================================================
    # 3. DIAGNÓSTICO DE VALORES AUSENTES E DUPLICATAS
    # =========================================================================
    # df.isnull().sum() conta os nulos de cada coluna.
    # df.duplicated().sum() verifica linhas 100% idênticas.
    print("--- Contagem de Valores Ausentes ---")
    print(df.isnull().sum())
    
    qtd_duplicatas = df.duplicated().sum()
    print(f"\nTotal de linhas duplicadas: {qtd_duplicatas}")
    
    # Explicação / Decisão de limpeza:
    # Os nulos concentram-se em 'Resolution', 'Time to Resolution', 
    # 'Customer Satisfaction Rating' e 'First Response Time'. Não devem ser 
    # removidos pois representam o ciclo de vida (chamados ainda não encerrados).
    print("\n" + "=" * 80 + "\n")

    # =========================================================================
    # 4. ESTATÍSTICAS DESCRITIVAS
    # =========================================================================
    # df.describe(include='all') calcula contagem, média, desvio padrão,
    # valores mínimos, máximos e quartis para variáveis numéricas e categóricas.
    print("--- Resumo Estatístico ---")
    print(df.describe(include="all"))
    print("\n" + "=" * 80 + "\n")

    # =========================================================================
    # 5. DISTRIBUIÇÃO DA VARIÁVEL ALVO (Ticket Type)
    # =========================================================================
    # Analisamos a frequência da variável-alvo para checar desbalanceamento.
    print("--- Frequência Absoluta (Ticket Type) ---")
    print(df['Ticket Type'].value_counts(dropna=False))

    print("\n--- Frequência Relativa (%) ---")
    print((df['Ticket Type'].value_counts(normalize=True) * 100).round(2))
    print("\n" + "=" * 80 + "\n")

    # =========================================================================
    # 6. LIMPEZA, TRATAMENTO E EXPORTAÇÃO
    # =========================================================================
    # Criamos uma cópia para preservar os dados originais brutos.
    df_cleaned = df.copy()

    # Executamos a limpeza de duplicatas caso existam
    df_cleaned = df_cleaned.drop_duplicates()

    # Padronizamos pequenas inconsistências de dicionário/idioma
    df_cleaned["Ticket Type"] = df_cleaned["Ticket Type"].replace({"Cobrança": "Billing Inquiry"})
    df_cleaned["Customer Gender"] = df_cleaned["Customer Gender"].replace({"Feminino": "Female"})

    # Garantimos a existência da pasta data/ e salvamos a base limpa
    os.makedirs("data", exist_ok=True)
    caminho_destino = "data/customer_support_tickets_cleaned.csv"
    df_cleaned.to_csv(caminho_destino, index=False)
    print(f">>> Dataset limpo salvo com sucesso em: '{caminho_destino}'\n")

    # =========================================================================
    # 7. VISUALIZAÇÕES GRÁFICAS
    # =========================================================================
    # Gera gráficos de barras para examinar as distribuições visuais.
    # Salva o arquivo em graphs/eda_visualizations.png.
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