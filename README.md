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
│   └── db.py                            # Gestão/carregamento da base
│
├── models/
│   └── model_events.py                  # Mapeamento de eventos
│
├── router/
│   ├── auth_router.py                   # Rotas de autenticação
│   └── ticket_router.py                 # Rotas CRUD de tickets
│
├── schemas/
│   ├── auth.py                          # Schemas Pydantic de autenticação
│   └── ticket.py                        # Schemas Pydantic de tickets
│
├── scripts/
│   └── eda.py                           # Script de Análise Exploratória
│
├── templates/
│   └── home.html                        # Template HTML simples
│
├── utils/
│   ├── auth.py                          # Regras e validações JWT
│   └── helpers.py                       # Funções utilitárias e regras de negócio
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

  * **Tempo:** `O(n)`, onde `n` é o número de linhas no DataFrame (precisa ler a coluna para achar o maior valor).
  * **Espaço:** `O(n)` temporário para armazenar a série convertida durante a checagem.

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

Documentação interativa disponível em:

`http://127.0.0.1:8000/docs`

---

## Evolução do projeto

### TP1

EDA + FastAPI + JWT + Modelos Pydantic + Funções Utilitárias (`utils/`) + Repositório Git + README + Modelagem de ameaças (Threat Model).

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

---

# FintechGuard 🛡️

**FintechGuard** é uma API de autenticação segura e de alto desempenho desenvolvida com **FastAPI**, focada na proteção contra ataques de força bruta (*brute-force*) utilizando **Redis** para gerenciamento de estado distribuído e limitação de taxa (*rate-limiting*), totalmente containerizada via **Docker**.

---

## 🚀 Tecnologias Utilizadas

* **Python 3.12+ / FastAPI**: Framework web assíncrono para construção da API.
* **Redis**: Banco de dados em memória para controle de tentativas de login e TTL (*Time To Live*).
* **JWT (JSON Web Tokens)**: Mecanismo de autenticação *stateless* e geração de acesso seguro.
* **Docker & Docker Compose**: Conteinerização da aplicação e orquestração dos serviços.
* **Postman**: Automação e execução de suítes de teste de integração.

---

## 🛠️ Implementações Realizadas

### 1. Sistema de Rate Limiting com Redis

* **Estratégia por IP + Usuário:** O controle de acesso bloqueia exclusivamente a combinação da chave `login_attempts:<ip>:<username>`, impedindo bloqueios indevidos para outros usuários na mesma rede.
* **Expiração Automática (TTL):** Configurado o bloqueio com expiração automática via Redis (`180` segundos) na primeira falha detectada.
* **Reset por Sucesso:** Limpeza imediata do histórico de falhas no Redis quando o login é efetuado com credenciais válidas.

### 2. Rotas de Autenticação & Tratamento de Erros

* **Endpoint `POST /auth/login`:** Validação de credenciais e geração de tokens Bearer.
* **Status HTTP 429 (Too Many Requests):** Interpolação do tempo restante (`TTL`) na resposta para informar ao cliente quanto tempo falta para o desbloqueio.
* **Status HTTP 401 (Unauthorized):** Resposta padrão para combinação incorreta de usuário/senha.

### 3. Containerização Completa

* **`Dockerfile`:** Configurado com imagem leve Python 3.12-slim, otimizando o isolamento da aplicação FastAPI.
* **`docker-compose.yml`:** Criado orquestrador declarativo unindo os serviços de API e Redis em uma rede virtual privada (`fintech-network`), com persistência de dados do Redis via volumes Docker.
* **Injeção via Variáveis de Ambiente:** Adaptado o `utils/rate_limiter.py` para usar `REDIS_HOST` e `REDIS_PORT` dinâmicos (fallback automático para `localhost` no desenvolvimento local).

### 4. Bateria de Testes Automatizados (Postman)

* **Scripts na aba `Scripts > Post-response`:**

  * Validação de *Status Code* `200 OK` e persistência do `access_token` em variáveis de coleção.
  * Teste de erro de credenciais invalidando a entrada (`401 Unauthorized`).
  * Loop automatizado via `postman.setNextRequest()` para validar o estouro de tentativas e confirmação do bloqueio via `429 Too Many Requests`.

---

## ⚙️ Como Rodar o Projeto

## ⚙️ Como Executar o Projeto

O FintechGuard pode ser executado de duas formas: utilizando **Docker**, recomendado para facilitar a configuração do ambiente, ou diretamente no ambiente Python utilizando **Uvicorn**.

### 🐳 Execução com Docker

A execução utilizando Docker é a forma recomendada para ambientes de apresentação, testes ou quando o projeto for executado em outro computador.

Com o Docker instalado e em execução, basta executar:

```bash
docker compose up --build
```

O Docker Compose será responsável por inicializar os serviços necessários para a aplicação, incluindo a API FastAPI e o Redis utilizado pelo sistema de **rate limiting**.

Essa abordagem evita a necessidade de instalar e configurar manualmente as dependências da aplicação e o Redis na máquina.

Para executar os containers em segundo plano:

```bash
docker compose up --build -d
```

Os logs da aplicação podem ser acompanhados com:

```bash
docker compose logs -f
```

Para encerrar os serviços:

```bash
docker compose down
```

### 🐍 Execução local com Python e Uvicorn

Também é possível executar o FintechGuard diretamente no ambiente Python. Essa opção é mais adequada para desenvolvimento e alterações no código.

Primeiro, crie e ative o ambiente virtual:

```bash
python -m venv venv
```

No Linux ou macOS:

```bash
source venv/bin/activate
```

No Windows PowerShell:

```powershell
venv\Scripts\activate
```

Em seguida, instale as dependências do projeto:

```bash
pip install -r requirements.txt
```

Como o sistema utiliza o Redis para controlar as tentativas de autenticação e implementar o **rate limiting**, o serviço Redis também precisa estar ativo.

Com as dependências instaladas e o Redis em execução, inicie a API:

```bash
uvicorn main:app --reload
```

A opção `--reload` permite que o servidor seja reiniciado automaticamente durante o desenvolvimento quando houver alterações no código.

### 📌 Execução em uma nova máquina

O projeto pode ser transferido para outro computador sem a necessidade de reinstalar manualmente todas as dependências uma por uma.

Para ambientes que possuem Docker, recomenda-se utilizar:

```bash
docker compose up --build
```

Quando o Docker não estiver disponível, a aplicação pode ser executada diretamente com Python, desde que o computador possua:

* Python instalado;
* Ambiente virtual configurado;
* Dependências instaladas pelo `requirements.txt`;
* Redis em execução;
* Variáveis de ambiente configuradas conforme o arquivo `.env.example`.

### 🌐 Acesso à API

Após iniciar a aplicação, a API estará disponível em:

```text
http://localhost:8000
```

A documentação interativa do FastAPI pode ser acessada pelo Swagger:

```text
http://localhost:8000/docs
```

A documentação alternativa do FastAPI também estará disponível em:

```text
http://localhost:8000/redoc
```

> **Recomendação:** Para apresentação e execução em computadores diferentes, utilize Docker. Para desenvolvimento diário, o ambiente virtual com Uvicorn oferece uma execução mais direta e facilita o processo de desenvolvimento.
