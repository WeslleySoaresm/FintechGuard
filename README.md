# FintechGuard

Sistema de atendimento bancário com foco em análise de dados, segurança da informação e inteligência artificial.

## Objetivo

O **FintechGuard** é um projeto acadêmico desenvolvido ao longo de um semestre com o objetivo de construir um sistema de atendimento bancário utilizando:

* Análise Exploratória de Dados (EDA)
* FastAPI
* PostgreSQL
* Autenticação JWT
* Segurança da informação
* Inteligência Artificial

## Dataset

O projeto utiliza um dataset de atendimento ao cliente contendo informações sobre chamados, clientes, produtos e atendimento.

### Características iniciais

Após a análise inicial utilizando Pandas:

* **8.470 registros**
* **20 colunas**
* Dados textuais e numéricos
* Valores ausentes identificados
* Nenhuma duplicata identificada

A etapa de limpeza será realizada após a identificação e análise dos valores ausentes.

## Tecnologias

### Backend

* Python
* FastAPI
* Uvicorn
* SQLAlchemy
* PostgreSQL
* Alembic

### Segurança

* JWT
* OAuth2PasswordBearer
* Hash de senhas
* Variáveis de ambiente
* Controle de acesso
* Logs e auditoria

### Análise de dados

* Pandas
* NumPy
* Matplotlib
* Seaborn
* Jupyter Notebook

### Testes e qualidade

* Pytest
* HTTPX
* Black
* isort
* Flake8

## Estrutura do projeto

```text
FINTECHGUARD/
│
├── data/
│   
│
├── models/
├── router/
├── templates/
│
├── scripts/
│   └── eda.py
│
├── main.py
├── .env
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

## Análise Exploratória de Dados

A EDA será realizada utilizando Pandas, buscando compreender a estrutura e os padrões existentes no dataset.

A análise inicial contempla:

1. Dimensão do dataset
2. Tipos de dados
3. Valores ausentes
4. Registros duplicados
5. Distribuição das categorias
6. Distribuição das principais variáveis
7. Identificação de padrões
8. Formulação de hipóteses sobre as intenções dos usuários

## TP1

O primeiro TP tem como objetivo:

* Escolher e documentar o dataset;
* Realizar a EDA inicial;
* Identificar valores ausentes;
* Verificar duplicatas;
* Analisar categorias;
* Criar gráficos exploratórios;
* Formular hipóteses sobre as intenções dos usuários;
* Configurar a estrutura inicial da FastAPI;
* Implementar autenticação JWT;
* Configurar PostgreSQL;
* Elaborar o DFD;
* Aplicar a tríade CIA;
* Documentar o projeto.

## Instalação

### 1. Criar o ambiente virtual

```bash
python3 -m venv venv
```

### 2. Ativar o ambiente virtual

```bash
source venv/bin/activate
```

### 3. Instalar as dependências

```bash
pip install "fastapi[standard]" sqlalchemy psycopg2-binary alembic "python-jose[cryptography]" "passlib[bcrypt]" python-multipart python-dotenv pydantic-settings pandas numpy matplotlib seaborn jupyter pytest httpx black isort flake8
```

### 4. Gerar o requirements.txt

```bash
pip freeze > requirements.txt
```

### 5. Gerar apartir do requirement.txt

### - Executar o requirement.txt 
```bash
pip install requirement.txt 
```
 
## Execução da EDA

Com o ambiente virtual ativado:

```bash
python scripts/eda.py
```

## Evolução do projeto

### TP1

EDA + FastAPI + JWT + Modelos Pydantic + Repositorio Git + Readme + Modelogem de ameaças (Threat model).


## Apresentação final

Ao final do semestre, será apresentada a solução completa, contemplando:

* Análise de dados
* Atendimento bancário
* API
* PostgreSQL
* Autenticação
* Segurança
* Inteligência Artificial
* Monitoramento
* Auditoria

## Status

🚧 **Em desenvolvimento**

Projeto atualmente na etapa **TP1 - Análise Exploratória de Dados e estrutura inicial da API**.

## Autores

* Weslley Soares 
* Bruno Santos
