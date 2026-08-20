import pandas as pd


# ==========================================
# 1. CARREGAMENTO DO DATASET
# ==========================================

df = pd.read_csv("data/customer_support_tickets.csv")


# ==========================================
# 2. VISÃO INICIAL DOS DADOS
# ==========================================

print("\n========== PRIMEIRAS LINHAS ==========")
print(df.head())


print("\n========== DIMENSÕES ==========")
print(f"Linhas: {df.shape[0]}")
print(f"Colunas: {df.shape[1]}")


print("\n========== COLUNAS ==========")
print(df.columns.tolist())


print("\n========== TIPOS DE DADOS ==========")
print(df.dtypes)


print("\n========== INFORMAÇÕES DO DATASET ==========")
df.info()


print("\n========== VALORES AUSENTES ==========")
print(df.isnull().sum())


print("\n========== DUPLICATAS ==========")
print(f"Quantidade de duplicatas: {df.duplicated().sum()}")


print("\n========== ESTATÍSTICAS ==========")
print(df.describe(include="all"))

print("\n========== DISTRIBUIÇÃO DAS CLASSES ==========")
coluna_texto = df.select_dtypes(include="object").columns

for coluna in coluna_texto:
    print(f"\nColuna --- {coluna}---")
    print(df[coluna].value_counts(dropna=False).head(15))

print("\n========== INICIANDO LIMPEZA ==========")

# Criar uma cópia do dataset original para limpeza
df_cleaned = df.copy()


# ==========================================
# 4.  remove duplicates
# ==========================================

df_cleaned = df_cleaned.drop_duplicates()

# ==========================================
# 5. corrigir valores claramente invalidos
# ==========================================

# valores "string" representa dados invalidos
valor_invalido = "string"
colunas_categoricas = [
    "Customer Gender",
    "Ticket Type",
    "Ticket Priority",
    "Ticket Channel",
]

for coluna in colunas_categoricas:
    df_cleaned[coluna] = df_cleaned[coluna].replace(
        valor_invalido,
        pd.NA
    )

# ==========================================
# 6. padronizar categorias
# ==========================================

df_cleaned["Customer Gender"] = df_cleaned["Customer Gender"].replace({
    "Feminino": "Female"
})

df_cleaned["Ticket Type"] = df_cleaned["Ticket Type"].replace({
    "Cobrança": "Billing Inquiry"
})

# ==========================================
# 7. salvar dataset limpo
# ==========================================

df_cleaned.to_csv("data/customer_support_tickets_cleaned.csv", index=False)

# =========================================
# 8. verificação final
# =========================================

print("\n========== DATASET LIMPO ==========")
print(f"Linhas: {df_cleaned.shape[0]}")
print(f"Colunas: {df_cleaned.shape[1]}")

print("\nvalores ausentes depois da limpeza:")
print(df_cleaned.isnull().sum())

print("\n duplicadas depois da limpeza:")
print(df_cleaned.duplicated().sum())

print("\n arquivo salvo em:")
print("data/customer_support_tickets_cleaned.csv")

print("\n========== STATUS DOS TICKETS ==========")
print(df_cleaned["Ticket Status"].value_counts(dropna=False))

print("\n========== STATUS X RESOLUTION ==========")
print(
    pd.crosstab(
        df_cleaned["Ticket Status"],
        df_cleaned["Resolution"].isna(),
        margins=True
    )
)
