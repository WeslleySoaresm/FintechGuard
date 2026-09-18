"""
===============================================================================

PROJETO: FintechGuard

Arquivo: eda.py

Descrição:
Análise Exploratória de Dados (EDA), limpeza dos dados,
visualizações avançadas e teste de hipótese.

===============================================================================
"""

import os
from html import unescape

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import mannwhitneyu


# =============================================================================
# CONFIGURAÇÕES
# =============================================================================

CAMINHO_DATASET = "data/customer_support_tickets.csv"
CAMINHO_ANOMALIAS = "data/customer_support_tickets_anomalies.csv"
PASTA_GRAFICOS = "graphs"

os.makedirs(PASTA_GRAFICOS, exist_ok=True)


# =============================================================================
# FUNÇÃO PRINCIPAL
# =============================================================================

def executar_eda():

    print("=" * 80)
    print("FINTECHGUARD - EDA AVANÇADA")
    print("=" * 80)

    # -------------------------------------------------------------------------
    # 1. CARREGAMENTO
    # -------------------------------------------------------------------------

    if not os.path.exists(CAMINHO_DATASET):
        print(f"Erro: Arquivo '{CAMINHO_DATASET}' não encontrado.")
        return

    df = pd.read_csv(CAMINHO_DATASET)

    quantidade_linhas_originais = len(df)

    print("\n[1] DIMENSÕES ORIGINAIS")
    print(f"Linhas: {quantidade_linhas_originais}")
    print(f"Colunas: {df.shape[1]}")

    # -------------------------------------------------------------------------
    # 2. INFORMAÇÕES INICIAIS
    # -------------------------------------------------------------------------

    print("\n[2] COLUNAS")
    print(df.columns.tolist())

    print("\n[3] TIPOS DE DADOS")
    print(df.dtypes)

    print("\n[4] VALORES AUSENTES")
    print(df.isnull().sum())

    print("\n[5] DUPLICADOS")
    print(f"Quantidade: {df.duplicated().sum()}")

    # -------------------------------------------------------------------------
    # 3. LIMPEZA BÁSICA
    # -------------------------------------------------------------------------

    print("\n" + "=" * 80)
    print("LIMPEZA DOS DADOS")
    print("=" * 80)

    # Remove linhas completamente vazias
    mascara_vazia = df.isna().all(axis=1)

    quantidade_vazias = mascara_vazia.sum()

    df_cleaned = df.loc[~mascara_vazia].copy()

    print(
        f"\nLinhas completamente vazias removidas: "
        f"{quantidade_vazias}"
    )

    # Remove duplicados
    duplicados = df_cleaned.duplicated().sum()

    df_cleaned = df_cleaned.drop_duplicates().copy()

    print(f"Duplicados removidos: {duplicados}")

    # -------------------------------------------------------------------------
    # 4. NORMALIZAÇÃO DE CATEGORIAS
    # -------------------------------------------------------------------------

    print("\n[6] NORMALIZAÇÃO DAS CATEGORIAS")

    if "Ticket Type" in df_cleaned.columns:

        mapa_ticket_type = {
            "Cobrança": "Billing inquiry",
            "Suporte Técnico": "Technical issue"
        }

        df_cleaned["Ticket Type"] = (
            df_cleaned["Ticket Type"]
            .replace(mapa_ticket_type)
        )

        print("Categorias normalizadas:")
        print("  Cobrança -> Billing inquiry")
        print("  Suporte Técnico -> Technical issue")

    # -------------------------------------------------------------------------
    # 5. IDENTIFICAÇÃO DE ANOMALIAS
    # -------------------------------------------------------------------------

    print("\n[7] IDENTIFICAÇÃO DE ANOMALIAS")

    colunas_textuais = [
        "Customer Name",
        "Customer Email",
        "Product Purchased",
        "Ticket Type",
        "Ticket Subject",
        "Ticket Description",
        "Ticket Status",
        "Resolution",
        "Ticket Priority",
        "Ticket Channel"
    ]

    colunas_textuais = [
        coluna
        for coluna in colunas_textuais
        if coluna in df_cleaned.columns
    ]

    # Cria uma cópia textual para inspeção e decodifica
    # entidades HTML.
    texto_inspecao = (
        df_cleaned[colunas_textuais]
        .fillna("")
        .astype(str)
        .apply(
            lambda coluna: coluna.map(unescape)
        )
    )

    # -------------------------------------------------------------------------
    # 5.1 - DETECÇÃO DE CONTEÚDO POTENCIALMENTE SUSPEITO
    # -------------------------------------------------------------------------

    # Detectamos a presença de HTML/JavaScript,
    # mas NÃO removemos automaticamente esses tickets.

    mascara_payload = texto_inspecao.apply(
        lambda coluna: coluna.str.contains(
            r"<\s*script\b",
            case=False,
            regex=True,
            na=False
        )
    ).any(axis=1)

    df_conteudo_suspeito = df_cleaned.loc[
        mascara_payload
    ].copy()

    print(
        f"Tickets contendo conteúdo potencialmente suspeito: "
        f"{len(df_conteudo_suspeito)}"
    )

    if len(df_conteudo_suspeito) > 0:

        print("\nTickets com possível conteúdo HTML/JavaScript:")

        print(
            df_conteudo_suspeito[
                [
                    "Ticket ID",
                    "Customer Name",
                    "Customer Age",
                    "Ticket Type"
                ]
            ].to_string(index=False)
        )

    # -------------------------------------------------------------------------
    # 5.2 - DETECÇÃO DE REGISTROS DE TESTE/ESTRUTURALMENTE ANÔMALOS
    # -------------------------------------------------------------------------

    quantidade_string = texto_inspecao.apply(
        lambda coluna:
            coluna.str.strip()
            .str.lower()
            .eq("string")
    ).sum(axis=1)

    idade_numerica = pd.to_numeric(
        df_cleaned["Customer Age"],
        errors="coerce"
    )

    # Registros com idade 120 e vários campos preenchidos
    # literalmente como "string" são tratados como
    # dados de teste/anômalos.

    mascara_string_suspeita = (
        (quantidade_string >= 3)
        & (idade_numerica == 120)
    )

    mascara_anomalia = mascara_string_suspeita

    print(
        f"\nRegistros estruturais/anômalos identificados: "
        f"{mascara_anomalia.sum()}"
    )

    if mascara_anomalia.any():

        print("\nRegistros removidos da EDA:")

        print(
            df_cleaned.loc[
                mascara_anomalia,
                [
                    "Ticket ID",
                    "Customer Name",
                    "Customer Age",
                    "Ticket Type"
                ]
            ].to_string(index=False)
        )

        # Mantém os registros separados para auditoria.
        df_cleaned.loc[mascara_anomalia].to_csv(
            CAMINHO_ANOMALIAS,
            index=False
        )

        print(
            f"\nRegistros anômalos salvos em: "
            f"{CAMINHO_ANOMALIAS}"
        )

    # Guarda a quantidade de linhas antes da remoção
    # das anomalias.
    linhas_antes_anomalias = len(df_cleaned)

    # Remove somente os registros estruturalmente anômalos.
    df_cleaned = df_cleaned.loc[
        ~mascara_anomalia
    ].copy()

    print(
        f"\nLinhas antes da remoção das anomalias: "
        f"{linhas_antes_anomalias}"
    )

    print(
        f"Linhas após limpeza: "
        f"{len(df_cleaned)}"
    )

    print(
        f"Total removido para análise: "
        f"{linhas_antes_anomalias - len(df_cleaned)}"
    )

    # -------------------------------------------------------------------------
    # 6. ESTATÍSTICAS DESCRITIVAS
    # -------------------------------------------------------------------------

    print("\n" + "=" * 80)
    print("ESTATÍSTICAS DESCRITIVAS")
    print("=" * 80)

    print(df_cleaned.describe(include="all"))

    # -------------------------------------------------------------------------
    # 7. DISTRIBUIÇÃO DOS TIPOS DE TICKET
    # -------------------------------------------------------------------------

    print("\n[8] DISTRIBUIÇÃO DOS TIPOS DE TICKET")

    if "Ticket Type" in df_cleaned.columns:

        distribuicao_ticket = (
            df_cleaned["Ticket Type"]
            .value_counts(dropna=False)
        )

        print(distribuicao_ticket)

    # -------------------------------------------------------------------------
    # 8. CONVERSÃO DO FIRST RESPONSE TIME
    # -------------------------------------------------------------------------

    print("\n" + "=" * 80)
    print("TRATAMENTO DO FIRST RESPONSE TIME")
    print("=" * 80)

    df_cleaned["First Response Datetime"] = pd.to_datetime(
        df_cleaned["First Response Time"],
        errors="coerce"
    )

    quantidade_validos = (
        df_cleaned["First Response Datetime"]
        .notna()
        .sum()
    )

    print(
        f"Valores de First Response Time convertidos: "
        f"{quantidade_validos}"
    )

    # Converte o horário para minutos desde 00:00
    df_cleaned["First Response Minutes"] = (
        df_cleaned["First Response Datetime"].dt.hour * 60
        + df_cleaned["First Response Datetime"].dt.minute
        + df_cleaned["First Response Datetime"].dt.second / 60
    )

    # -------------------------------------------------------------------------
    # 9. VISUALIZAÇÕES BÁSICAS
    # -------------------------------------------------------------------------

    print("\n" + "=" * 80)
    print("GERANDO VISUALIZAÇÕES")
    print("=" * 80)

    fig, axes = plt.subplots(
        1,
        3,
        figsize=(18, 5)
    )

    if "Ticket Type" in df_cleaned.columns:

        ordem = (
            df_cleaned["Ticket Type"]
            .value_counts()
            .index
        )

        sns.countplot(
            data=df_cleaned,
            y="Ticket Type",
            order=ordem,
            ax=axes[0]
        )

        axes[0].set_title(
            "Distribuição por Tipo de Ticket"
        )

        axes[0].set_xlabel("Quantidade")
        axes[0].set_ylabel("Tipo de Ticket")

    if "Ticket Priority" in df_cleaned.columns:

        sns.countplot(
            data=df_cleaned,
            x="Ticket Priority",
            ax=axes[1]
        )

        axes[1].set_title(
            "Distribuição por Prioridade"
        )

        axes[1].set_xlabel("Prioridade")
        axes[1].set_ylabel("Quantidade")

    if "Ticket Channel" in df_cleaned.columns:

        sns.countplot(
            data=df_cleaned,
            x="Ticket Channel",
            ax=axes[2]
        )

        axes[2].set_title(
            "Distribuição por Canal"
        )

        axes[2].set_xlabel("Canal")
        axes[2].set_ylabel("Quantidade")

    plt.tight_layout()

    caminho = os.path.join(
        PASTA_GRAFICOS,
        "eda_visualizations.png"
    )

    plt.savefig(
        caminho,
        dpi=150
    )

    plt.close()

    print(f"Gráfico salvo: {caminho}")

    # -------------------------------------------------------------------------
    # 10. HEATMAP DE CORRELAÇÃO
    # -------------------------------------------------------------------------

    print("\n" + "=" * 80)
    print("HEATMAP DE CORRELAÇÃO")
    print("=" * 80)

    colunas_correlacao = [
        "Customer Age",
        "First Response Minutes",
        "Customer Satisfaction Rating"
    ]

    df_correlacao = df_cleaned[
        colunas_correlacao
    ].copy()

    matriz_correlacao = df_correlacao.corr(
        numeric_only=True
    )

    print("\nMatriz de correlação:")
    print(
        matriz_correlacao.round(3)
    )

    plt.figure(
        figsize=(8, 6)
    )

    sns.heatmap(
        matriz_correlacao,
        annot=True,
        fmt=".3f",
        cmap="coolwarm",
        center=0,
        square=True
    )

    plt.title(
        "Heatmap de Correlação - FintechGuard"
    )

    plt.tight_layout()

    caminho = os.path.join(
        PASTA_GRAFICOS,
        "heatmap_correlacao.png"
    )

    plt.savefig(
        caminho,
        dpi=150
    )

    plt.close()

    print(
        f"Heatmap salvo: {caminho}"
    )

    # -------------------------------------------------------------------------
    # 11. SCATTER - TEMPO DE RESPOSTA X SATISFAÇÃO
    # -------------------------------------------------------------------------

    print(
        "\n[9] SCATTER PLOT - "
        "RESPOSTA X SATISFAÇÃO"
    )

    dados_resposta = df_cleaned[
        [
            "First Response Minutes",
            "Customer Satisfaction Rating"
        ]
    ].dropna()

    if len(dados_resposta) > 0:

        plt.figure(
            figsize=(9, 6)
        )

        sns.scatterplot(
            data=dados_resposta,
            x="First Response Minutes",
            y="Customer Satisfaction Rating",
            alpha=0.4
        )

        plt.title(
            "First Response Time x Satisfação do Cliente"
        )

        plt.xlabel(
            "Horário da primeira resposta "
            "(minutos desde 00:00)"
        )

        plt.ylabel(
            "Satisfação do Cliente"
        )

        plt.tight_layout()

        caminho = os.path.join(
            PASTA_GRAFICOS,
            "scatter_resposta_satisfacao.png"
        )

        plt.savefig(
            caminho,
            dpi=150
        )

        plt.close()

        print(
            f"Scatter plot salvo: {caminho}"
        )

    # -------------------------------------------------------------------------
    # 12. SCATTER - IDADE X SATISFAÇÃO
    # -------------------------------------------------------------------------

    print(
        "\n[10] SCATTER PLOT - "
        "IDADE X SATISFAÇÃO"
    )

    dados_idade = df_cleaned[
        [
            "Customer Age",
            "Customer Satisfaction Rating"
        ]
    ].dropna()

    if len(dados_idade) > 0:

        plt.figure(
            figsize=(9, 6)
        )

        sns.scatterplot(
            data=dados_idade,
            x="Customer Age",
            y="Customer Satisfaction Rating",
            alpha=0.4
        )

        plt.title(
            "Idade x Satisfação do Cliente"
        )

        plt.xlabel("Idade")
        plt.ylabel("Satisfação do Cliente")

        plt.tight_layout()

        caminho = os.path.join(
            PASTA_GRAFICOS,
            "scatter_idade_satisfacao.png"
        )

        plt.savefig(
            caminho,
            dpi=150
        )

        plt.close()

        print(
            f"Scatter plot salvo: {caminho}"
        )

    # -------------------------------------------------------------------------
    # 13. TESTE DE HIPÓTESE
    # -------------------------------------------------------------------------

    print("\n" + "=" * 80)
    print("TESTE DE HIPÓTESE - MANN-WHITNEY U")
    print("=" * 80)

    dados_teste = df_cleaned[
        [
            "First Response Minutes",
            "Customer Satisfaction Rating"
        ]
    ].dropna()

    if len(dados_teste) >= 10:

        # Mediana do horário de primeira resposta
        mediana_resposta = (
            dados_teste[
                "First Response Minutes"
            ].median()
        )

        grupo_mais_cedo = dados_teste[
            dados_teste[
                "First Response Minutes"
            ] <= mediana_resposta
        ]["Customer Satisfaction Rating"]

        grupo_mais_tarde = dados_teste[
            dados_teste[
                "First Response Minutes"
            ] > mediana_resposta
        ]["Customer Satisfaction Rating"]

        estatistica_u, p_valor = mannwhitneyu(
            grupo_mais_cedo,
            grupo_mais_tarde,
            alternative="two-sided"
        )

        alpha = 0.05

        print(
            f"\nMediana de First Response Time: "
            f"{mediana_resposta:.2f} minutos"
        )

        print(
            f"Grupo de resposta mais cedo: "
            f"{len(grupo_mais_cedo)} registros"
        )

        print(
            f"Grupo de resposta mais tarde: "
            f"{len(grupo_mais_tarde)} registros"
        )

        print(
            f"Mediana da satisfação - resposta mais cedo: "
            f"{grupo_mais_cedo.median():.2f}"
        )

        print(
            f"Mediana da satisfação - resposta mais tarde: "
            f"{grupo_mais_tarde.median():.2f}"
        )

        print(
            f"\nEstatística U: "
            f"{estatistica_u:.2f}"
        )

        print(
            f"p-valor: "
            f"{p_valor:.6f}"
        )

        print(
            f"Alpha: "
            f"{alpha}"
        )

        if p_valor < alpha:

            print(
                "\nResultado: existe evidência estatística "
                "de diferença entre as distribuições de "
                "satisfação dos dois grupos."
            )

        else:

            print(
                "\nResultado: não há evidência estatística "
                "suficiente, ao nível de 5%, para afirmar "
                "que as distribuições de satisfação "
                "diferem entre os grupos."
            )

        # ---------------------------------------------------------------------
        # 14. BOXPLOT
        # ---------------------------------------------------------------------

        dados_boxplot = dados_teste.copy()

        dados_boxplot["Grupo"] = dados_boxplot[
            "First Response Minutes"
        ].apply(
            lambda x:
                "Resposta mais cedo"
                if x <= mediana_resposta
                else "Resposta mais tarde"
        )

        plt.figure(
            figsize=(8, 6)
        )

        sns.boxplot(
            data=dados_boxplot,
            x="Grupo",
            y="Customer Satisfaction Rating"
        )

        plt.title(
            "Distribuição da Satisfação por Grupo "
            "de Horário da Primeira Resposta"
        )

        plt.xlabel("Grupo")
        plt.ylabel("Satisfação")

        plt.tight_layout()

        caminho = os.path.join(
            PASTA_GRAFICOS,
            "boxplot_resposta_satisfacao.png"
        )

        plt.savefig(
            caminho,
            dpi=150
        )

        plt.close()

        print(
            f"Boxplot salvo: {caminho}"
        )

    else:

        print(
            "Dados insuficientes para realizar "
            "o teste de hipótese."
        )

    # -------------------------------------------------------------------------
    # 15. RESUMO FINAL
    # -------------------------------------------------------------------------

    print("\n" + "=" * 80)
    print("EDA CONCLUÍDA")
    print("=" * 80)

    print(
        f"\nDataset original: "
        f"{quantidade_linhas_originais} linhas"
    )

    print(
        f"Dataset utilizado na análise: "
        f"{len(df_cleaned)} linhas"
    )

    print("\nArquivos gerados:")

    arquivos = [
        "eda_visualizations.png",
        "heatmap_correlacao.png",
        "scatter_resposta_satisfacao.png",
        "scatter_idade_satisfacao.png",
        "boxplot_resposta_satisfacao.png"
    ]

    for arquivo in arquivos:

        caminho = os.path.join(
            PASTA_GRAFICOS,
            arquivo
        )

        if os.path.exists(caminho):

            print(
                f"  ✓ graphs/{arquivo}"
            )

    if os.path.exists(CAMINHO_ANOMALIAS):

        print(
            f"  ✓ {CAMINHO_ANOMALIAS}"
        )


# =============================================================================
# EXECUÇÃO
# =============================================================================

if __name__ == "__main__":
    executar_eda()