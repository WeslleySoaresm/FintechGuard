

# FintechGuard

Sistema de atendimento bancário com foco em análise de dados, segurança da informação e inteligência artificial.

## Objetivo

O **FintechGuard** é um projeto acadêmico desenvolvido ao longo de um semestre com o objetivo de construir um sistema de atendimento bancário (foco em detecção de fraudes e prevenção contra vazamento de dados) utilizando:

* Análise Exploratória de Dados (EDA)
* FastAPI
* PostgreSQL
* Autenticação JWT
* Segurança da informação e Tríade CIA
* Inteligência Artificial

---

## 🔒 Segurança e Modelagem de Ameaças

O foco central da segurança do **FintechGuard** está no combate a **Fraudes Bancárias** e na **Prevenção contra Vazamento de Dados (DLP)**.

* **Garantia da Tríade CIA (Confidencialidade, Integridade e Disponibilidade):** Proteção de dados sensíveis dos clientes (PII) contra acessos não autorizados.
* **Autenticação Segura:** Emissão de tokens JWT via fluxo OAuth2 com algoritmo de assinatura segura.
* **Hash de Senhas:** Armazenamento seguro de credenciais utilizando algoritmos de hashing forte (`bcrypt`).
* **Proteção de Variáveis Sensíveis:** Separação completa de credenciais de banco e chaves de assinatura em arquivos `.env`.

---

## Dataset

O projeto utiliza um dataset de atendimento ao cliente contendo informações sobre chamados, clientes, produtos e atendimento.

> 🔗 **Fonte:** [Kaggle - Customer Support Ticket Dataset](https://www.kaggle.com/datasets/suraj520/customer-support-ticket-dataset?resource=download)

### Características iniciais

Após a análise inicial utilizando Pandas:

* **8.470 registros (Linhas)**
* **20 colunas**
* Dados textuais e numéricos
* Valores ausentes identificados
* Nenhuma duplicata identificada

### Detalhamento das Colunas

#### Colunas de Texto (`str` / Categóricas)

* `Customer Name` (PII)
* `Customer Email` (PII)
* `Customer Gender`
* `Product Purchased`
* `Date of Purchase`
* `Ticket Type`
* `Ticket Subject`
* `Ticket Description`
* `Ticket Status`
* `Resolution`
* `Ticket Priority`
* `Ticket Channel`
* `First Response Time`
* `Time to Resolution`

#### Colunas Numéricas

* `Customer Satisfaction Rating` (`float64`)
* `Unnamed: 17` (`float64` - Inconsistente/Sujeira)
* `Unnamed: 18` (`float64` - Inconsistente/Sujeira)
* `Unnamed: 19` (`float64` - Inconsistente/Sujeira)

### Diretriz de Limpeza

A etapa de limpeza será realizada após a identificação e análise detalhada dos valores ausentes e inconsistências.

> **Regra Importante:** Não vamos apagar dados simplesmente porque parecem inconvenientes. Cada limpeza terá uma justificativa documentada que entrará diretamente no relatório do TP1.

---

## Tecnologias

### Backend

* Python
* FastAPI
* Uvicorn
* SQLAlchemy
* PostgreSQL
* Alembic
* Pydantic / Pydantic-Settings

### Segurança

* JWT (PyJWT / Python-Jose)
* OAuth2PasswordBearer / HTTPBearer
* Hash de senhas (`passlib`, `bcrypt`)
* Variáveis de ambiente (`python-dotenv`)
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

---

## Estrutura do projeto

```text
FINTECHGUARD/
│
├── data/
│   ├── customer_support_tickets.csv    # Dataset do Kaggle
│   └── db.py                          # Gestão/carregamento da base
│
├── models/
│   └── model_events.py                # Mapeamento de eventos
│
├── router/
│   ├── auth_router.py                 # Rotas de autenticação
│   └── ticket_router.py               # Rotas CRUD de tickets
│
├── schemas/
│   ├── auth.py                        # Schemas Pydantic de autenticação
│   └── ticket.py                      # Schemas Pydantic de tickets
│
├── scripts/
│   └── eda.py                         # Script de Análise Exploratória
│
├── templates/
│   └── home.html                      # Template HTML simples
│
├── utils/
│   ├── auth.py                        # Regras e validações JWT
│   └── helpers.py                     # Funções utilitárias e regras de negócio
│
├── venv/
├── .env
├── .env.example
├── .gitignore
├── main.py
├── README.md
└── requirements.txt

```

---

## Arquitetura e Funções Utilitárias (`utils/`)

Para manter a arquitetura da API limpa, modular e alinhada às melhores práticas do **DRY (*Don't Repeat Yourself*)**, centralizamos as regras de negócio repetitivas dentro do módulo `utils/`.

Isso garante que rotas como `GET`, `POST` e `DELETE` consumam funções utilitárias unificadas, evitando duplicação de código e facilitando manutenções futuras.

### 1. `get_next_ticket_id(df)`

* **Objetivo:** Calcular e autocompletar o próximo identificador único (`Ticket ID`) sequencial para a criação de novos chamados.
* **Funcionamento:**
1. Converte a coluna `Ticket ID` do DataFrame para valores numéricos, ignorando dados inconsistentes (`errors="coerce"`).
2. Identifica o maior ID presente no dataset.
3. Incrementa `+1` ao valor máximo encontrado.
4. Caso o DataFrame esteja vazio, inicia a contagem a partir de 1.


* **Algoritmo:** Algoritmo de Busca de Valor Máximo (Maior Elemento) com coerção de tipos.
* **Complexidade Computacional:**
* **Tempo:** $O(n)$, onde $n$ é o número de linhas no DataFrame (precisa ler a coluna para achar o maior valor).
* **Espaço:** $O(n)$ temporário para armazenar a série convertida durante a checagem.



```python
def get_next_ticket_id(df: pd.DataFrame) -> int:
    if df.empty or "Ticket ID" not in df.columns:
        return 1
    numeric_ids = pd.to_numeric(df["Ticket ID"], errors="coerce")
    if numeric_ids.isna().all():
        return 1
    return int(numeric_ids.max()) + 1

```

### 2. `find_ticket_by_id(ticket_id)`

* **Objetivo:** Centralizar a busca e validação da existência de um registro no DataFrame.
* **Funcionamento:**
1. Filtra a base de dados buscando a linha correspondente ao `ticket_id` informado.
2. Lança automaticamente uma exceção `HTTP 404 Not Found` caso o registro não exista.
3. Retorna o sub-DataFrame filtrado para ser manipulado pela rota chamadora.



```python
def find_ticket_by_id(ticket_id: int) -> pd.DataFrame:
    numeric_ids = pd.to_numeric(db.df["Ticket ID"], errors="coerce")
    ticket = db.df[numeric_ids == ticket_id]

    if ticket.empty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ticket com ID {ticket_id} não encontrado."
        )
    return ticket

```

### Benefícios da Abordagem

* **Manutenibilidade:** Se a regra para encontrar um ticket ou gerar um ID mudar, basta alterar a função no `utils/` sem precisar mexer nos arquivos de rotas.
* **Tratamento de Erros Padronizado:** A validação de inexistência do ID dispara a exceção 404 direto da função utilitária, garantindo respostas padronizadas em todas as rotas.
* **Separação de Responsabilidades:** O arquivo de rotas (`router/ticket_router.py`) fica focado apenas em receber a requisição e retornar a resposta, enquanto o `utils/` lida com a lógica dos dados.

---

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

---

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
* Modelagem de ameaças (Threat Model);
* Documentar o projeto.

---

## Instalação

### 1. Criar o ambiente virtual

```bash
python3 -m venv venv

```

### 2. Ativar o ambiente virtual

```bash
# Linux / macOS
source venv/bin/activate

# Windows PowerShell
.\venv\Scripts\activate

```

### 3. Instalar as dependências

```bash
pip install "fastapi[standard]" sqlalchemy psycopg2-binary alembic "python-jose[cryptography]" pyjwt "passlib[bcrypt]" python-multipart python-dotenv pydantic-settings pandas numpy matplotlib seaborn jupyter pytest httpx black isort flake8

```

### 4. Gerar o requirements.txt

```bash
pip freeze > requirements.txt

```

### 5. Executar a partir do requirements.txt

```bash
pip install -r requirements.txt

```

---

## Execução da EDA

Com o ambiente virtual ativado:

```bash
python scripts/eda.py

```

---

## Execução da API

Para iniciar o servidor de desenvolvimento:

```bash
fastapi dev main.py

```

Documentação interativa disponível em: `[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)`

---

## Evolução do projeto

### TP1

EDA + FastAPI + JWT + Modelos Pydantic + Funções Utilitárias (`utils/`) + Repositório Git + Readme + Modelagem de ameaças (Threat Model).

---

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

---

## Status

🚧 **Em desenvolvimento**

Projeto atualmente na etapa **TP1 - Análise Exploratória de Dados e estrutura inicial da API**.

---

## Autores

* **Weslley Soares**
* **Bruno Santos**
