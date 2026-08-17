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