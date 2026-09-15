Perfeito. Aqui está o `README.md` completo, já estruturado para o estado atual do **FintechGuard / TP2**.

````markdown
# FintechGuard

## Atendimento Bancário Seguro com Inteligência Artificial

Projeto acadêmico desenvolvido na disciplina **Análise e Segurança de Agentes de IA [26E3_5]**, com foco em segurança de aplicações, proteção de dados e atendimento bancário assistido por Inteligência Artificial.

---

## 👨‍💻 Autores

- **Weslley Soares**
- **Bruno Santos**

**Professor:** Ricardo Pires Mesquita

---

# 📌 Sobre o Projeto

O **FintechGuard** é uma aplicação voltada para atendimento bancário, desenvolvida com foco em **segurança, proteção de dados e prevenção de fraudes**.

A proposta é construir uma aplicação capaz de receber e gerenciar solicitações de clientes bancários, mantendo os dados protegidos contra problemas comuns em aplicações web, como:

- acesso indevido a dados de outros usuários;
- manipulação de campos da API;
- SQL Injection;
- força bruta contra autenticação;
- exposição de informações sensíveis;
- ataques relacionados a configuração de navegador;
- falhas de controle de acesso;
- entrada de dados maliciosos.

O projeto também possui uma etapa de análise exploratória dos dados (**EDA**) utilizando técnicas estatísticas e visualizações para compreender o conjunto de dados utilizado no desenvolvimento.

---

# 🎯 Objetivos

## Objetivo geral

Desenvolver uma aplicação de atendimento bancário que utilize recursos de Inteligência Artificial e mecanismos de segurança para reduzir riscos relacionados a fraude e vazamento de dados.

## Objetivos específicos

- Desenvolver uma API REST utilizando FastAPI.
- Implementar autenticação baseada em JWT.
- Proteger senhas utilizando bcrypt.
- Implementar controle de acesso baseado no usuário autenticado.
- Evitar acesso indevido a recursos de outros usuários.
- Implementar validação rigorosa dos dados recebidos.
- Reduzir riscos de ataques de força bruta.
- Implementar headers de segurança HTTP.
- Configurar política de CORS.
- Implementar Content Security Policy.
- Utilizar migrations com Alembic.
- Persistir dados utilizando SQLModel.
- Realizar análise exploratória dos dados.
- Utilizar testes automatizados para validar controles de segurança.
- Realizar análise de segurança utilizando OWASP ZAP.
- Preparar a aplicação para futuras funcionalidades relacionadas a agentes de IA.

---

# 🏗️ Arquitetura Atual

A aplicação possui uma arquitetura separada entre API, banco de dados, autenticação, schemas, modelos e frontend.

```text
FintechGuard/
│
├── main.py
│
├── data/
│   ├── db.py
│   ├── fintechguard.db
│   └── customer_support_tickets.csv
│
├── models/
│   ├── model_events.py
│   └── ...
│
├── schemas/
│   ├── auth.py
│   ├── ticket.py
│   └── ...
│
├── router/
│   ├── auth_router.py
│   ├── ticket_router.py
│   ├── predict_router.py
│   └── dashboard_router.py
│
├── utils/
│   ├── auth.py
│   ├── helpers.py
│   └── ...
│
├── scripts/
│   └── create_user.py
│
├── alembic/
│   ├── versions/
│   └── ...
│
├── templates/
│   ├── login.html
│   └── dashboard.html
│
├── static/
│   ├── css/
│   │   ├── login.css
│   │   └── dashboard.css
│   │
│   └── js/
│       ├── login.js
│       └── dashboard.js
│
├── tests/
│   └── ...
│
├── requirements.txt
├── alembic.ini
└── README.md
````

---

# 🛠️ Tecnologias

## Backend

* Python
* FastAPI
* Pydantic
* SQLModel
* SQLAlchemy
* Alembic
* JWT
* bcrypt
* Redis

## Banco de dados

* SQLite atualmente utilizado no ambiente de desenvolvimento
* SQLModel para ORM/modelagem
* Alembic para migrations

## Análise de dados

* Pandas
* NumPy
* SciPy
* Matplotlib
* Seaborn
* Jupyter Notebook

## Frontend

* HTML5
* CSS3
* JavaScript

## Segurança

* JWT
* bcrypt
* CORS
* CSP
* HSTS
* Security Headers
* Rate Limiting
* BOLA / Broken Object Level Authorization
* Validação Pydantic
* OWASP ZAP

## Testes

* pytest

## Infraestrutura

* Redis
* Docker / Docker Compose
* Git
* GitHub

---

# 📊 Dataset

O projeto utiliza o dataset:

**Customer Support Ticket Dataset**

O dataset possui aproximadamente:

* **8.470 registros**
* **20 colunas originalmente**

Durante a etapa de preparação dos dados foram identificadas colunas sem utilidade para a análise, como:

```text
Unnamed: 17
Unnamed: 18
Unnamed: 19
```

Essas colunas são removidas durante o carregamento do dataset.

Também foi realizada verificação de valores duplicados.

Resultado encontrado:

```text
Duplicados: 0
```

---

# 🔬 Análise Exploratória de Dados

A análise exploratória faz parte do TP2.

O objetivo é compreender o comportamento dos dados antes de utilizar os mesmos na aplicação.

Foram utilizadas técnicas como:

* análise de distribuição;
* estatísticas descritivas;
* correlação;
* heatmap;
* scatter plots;
* análise de variáveis categóricas;
* comparação entre grupos;
* testes estatísticos.

Ferramentas utilizadas:

```text
Pandas
NumPy
Matplotlib
Seaborn
SciPy
Jupyter Notebook
```

---

# 🧪 Teste de Hipótese

Como parte da análise estatística do TP2, é utilizada uma hipótese definida durante o projeto.

Dependendo das características dos dados e da distribuição observada, poderá ser utilizado:

* **Independent t-test**
* **Mann–Whitney U**

A escolha do teste deve considerar as características dos dados, principalmente distribuição e pressupostos estatísticos.

O resultado deve ser interpretado de forma acessível, evitando tratar correlação ou associação estatística como causalidade.

---

# 🗄️ Banco de Dados

A aplicação deixou de utilizar o CSV como mecanismo principal de persistência da aplicação.

O CSV permanece sendo utilizado para:

```text
EDA
↓
Pandas
↓
Análise estatística
↓
Visualizações
```

Enquanto a aplicação utiliza:

```text
FastAPI
↓
SQLModel
↓
Banco de dados
```

Essa separação evita misturar análise de dados com persistência operacional da aplicação.

---

# 📐 Modelo de Dados

O modelo atual possui três entidades principais:

```text
User
   │
   │ 1:N
   ▼
Ticket
   │
   │ 1:N
   ▼
ConversationMessage
```

## User

Representa o usuário autenticado da aplicação.

Principais campos:

```text
id
name
email
password_hash
role
created_at
```

O email é utilizado como identificador de login.

A senha não é armazenada em texto puro.

---

## Ticket

Representa um atendimento.

Principais informações:

```text
id
user_id
customer_name
customer_email
customer_age
customer_gender
product_purchased
date_of_purchase
ticket_type
ticket_subject
ticket_description
ticket_status
ticket_priority
ticket_channel
first_response_time
time_to_resolution
resolution
customer_satisfaction_rating
created_at
```

O campo:

```text
user_id
```

estabelece a relação entre o ticket e o usuário responsável.

---

## ConversationMessage

Representa mensagens relacionadas a um ticket.

Estrutura conceitual:

```text
id
ticket_id
sender_type
message
created_at
```

---

# 🔄 Migrations com Alembic

O projeto utiliza Alembic para controle de alterações do banco.

Exemplo:

```bash
alembic current
```

Para criar uma migration:

```bash
alembic revision --autogenerate -m "descricao_da_migration"
```

Para aplicar:

```bash
alembic upgrade head
```

Para voltar uma migration:

```bash
alembic downgrade -1
```

Uma das migrations realizadas no TP2 removeu o campo legado:

```text
ticket_id
```

A aplicação passou a utilizar o:

```text
id
```

como identificador principal do ticket.

---

# 🔐 Autenticação

A autenticação utiliza **JWT (JSON Web Token)**.

Fluxo:

```text
Usuário
   │
   ▼
POST /auth/token
   │
   ▼
Validação do email
   │
   ▼
Verificação da senha com bcrypt
   │
   ▼
JWT
   │
   ▼
Cliente envia:
Authorization: Bearer <token>
```

---

# 🔑 Proteção de Senhas

As senhas não são armazenadas diretamente no banco.

É utilizado:

```text
bcrypt
```

Para criação do hash:

```python
bcrypt.hashpw(
    password.encode("utf-8"),
    bcrypt.gensalt()
)
```

Para verificar uma senha:

```python
bcrypt.checkpw(
    password.encode("utf-8"),
    user.password_hash.encode("utf-8")
)
```

Também existe validação relacionada ao limite de tamanho suportado pelo bcrypt.

---

# 🛡️ Controle de Acesso

Um dos controles mais importantes implementados é a proteção contra:

## BOLA

**Broken Object Level Authorization**

O problema acontece quando um usuário consegue acessar um recurso pertencente a outro usuário apenas alterando o ID da requisição.

Exemplo de requisição:

```text
GET /tickets/10
```

Não basta verificar:

```python
Ticket.id == ticket_id
```

A aplicação também verifica:

```python
Ticket.user_id == user_id
```

A consulta possui, conceitualmente:

```python
select(Ticket).where(
    Ticket.id == ticket_id,
    Ticket.user_id == user_id
)
```

Dessa maneira, o ticket precisa:

1. existir;
2. possuir o ID solicitado;
3. pertencer ao usuário autenticado.

Caso contrário:

```text
404 Ticket não encontrado
```

---

# 🚫 Validação de Entrada

Os schemas Pydantic utilizam:

```python
ConfigDict(extra="forbid")
```

Isso impede que campos não definidos no schema sejam enviados silenciosamente para a API.

Exemplo:

```json
{
    "customer_name": "João",
    "customer_email": "joao@email.com",
    "campo_malicioso": "teste"
}
```

O campo:

```text
campo_malicioso
```

não pertence ao contrato da API e deve ser rejeitado.

Essa medida ajuda a manter o contrato da API explícito e reduz superfícies de entrada desnecessárias.

---

# 🧹 Sanitização

Entradas textuais passam por funções de sanitização antes de serem utilizadas em determinadas operações.

Exemplo:

```python
sanitize_text()
```

Também são utilizados validadores Pydantic para campos específicos.

Além da sanitização, a aplicação evita construir SQL utilizando concatenação de strings.

---

# 💉 SQL Injection

As consultas são realizadas utilizando SQLModel/SQLAlchemy.

Exemplo conceitual:

```python
select(Ticket).where(
    Ticket.id == ticket_id
)
```

Não são utilizadas consultas SQL construídas por concatenação de strings fornecidas pelo usuário.

Isso reduz o risco de SQL Injection.

---

# 🚦 Rate Limiting

O endpoint de autenticação possui proteção contra tentativas excessivas de login.

Endpoint protegido:

```text
POST /auth/token
```

O mecanismo utiliza:

```text
Redis
```

O objetivo é dificultar ataques de força bruta contra credenciais.

Fluxo:

```text
Tentativa de login
       │
       ▼
Identificação do usuário/IP
       │
       ▼
Redis
       │
       ├── dentro do limite → permite
       │
       └── limite excedido → bloqueia temporariamente
```

O uso do Redis permite armazenar temporariamente os contadores de tentativas.

---

# 🌐 CORS

A aplicação utiliza uma lista de origens permitidas.

Atualmente:

```text
http://localhost:3000
http://localhost:5173
```

Exemplo:

```python
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",
]
```

Isso evita liberar indiscriminadamente qualquer origem.

Uma origem não autorizada pode receber resposta HTTP normalmente, mas o navegador não permitirá que um frontend daquela origem leia a resposta como uma requisição CORS válida.

---

# 🧱 Security Headers

Foram implementados headers de segurança HTTP.

## X-Frame-Options

```text
X-Frame-Options: DENY
```

Ajuda a impedir que a aplicação seja carregada em frames de outros sites.

---

## X-Content-Type-Options

```text
X-Content-Type-Options: nosniff
```

Evita que o navegador tente interpretar o conteúdo utilizando um MIME type diferente daquele declarado.

---

## HSTS

Em produção:

```text
Strict-Transport-Security:
max-age=31536000; includeSubDomains
```

O HSTS é aplicado somente em produção porque o ambiente de desenvolvimento utiliza HTTP local.

Não faz sentido ensinar um navegador a exigir HTTPS de um servidor local que está deliberadamente rodando em HTTP.

---

# 🛡️ Content Security Policy

Foi implementada uma política CSP.

## Desenvolvimento

O ambiente de desenvolvimento possui uma política um pouco mais permissiva para permitir o funcionamento da documentação Swagger UI.

Exemplo de recursos permitidos:

```text
self
cdn.jsdelivr.net
```

Também são permitidos recursos inline necessários ao funcionamento atual do ambiente de desenvolvimento.

---

## Produção

A política planejada é mais restritiva:

```text
default-src 'self';
script-src 'self';
style-src 'self';
img-src 'self' data:;
font-src 'self';
connect-src 'self';
frame-ancestors 'none';
```

A aplicação também está sendo organizada para manter JavaScript e CSS em arquivos externos.

Estrutura:

```text
static/
├── css/
│   ├── login.css
│   └── dashboard.css
│
└── js/
    ├── login.js
    └── dashboard.js
```

Isso facilita uma CSP mais rígida e reduz a necessidade de:

```text
unsafe-inline
```

---

# 🖥️ Frontend

O frontend possui:

```text
Login
Dashboard
Tickets
Filtros
Indicadores
Modal de criação
Modal de detalhes
```

---

# 📊 Dashboard

O dashboard apresenta indicadores como:

* quantidade total de tickets;
* tickets abertos;
* tickets de alta prioridade;
* média de avaliação.

Também possui filtros para facilitar a visualização dos atendimentos.

---

# 🎫 Gerenciamento de Tickets

A aplicação permite:

### Criar ticket

```text
POST /tickets
```

### Listar tickets

```text
GET /tickets
```

### Consultar ticket específico

```text
GET /tickets/{ticket_id}
```

### Excluir ticket

```text
DELETE /tickets/{ticket_id}
```

Todas as rotas protegidas exigem autenticação.

---

# 🔎 Detalhes do Ticket

O dashboard possui uma janela modal para visualizar informações detalhadas do ticket.

São apresentados dados como:

```text
ID
Assunto
Status
Prioridade
Avaliação
Cliente
Email
Idade
Gênero
Produto
Tipo do ticket
Canal
Data da compra
Descrição
Tempo até primeira resposta
Tempo de resolução
Resolução
Usuário responsável
Data de criação
```

Os dados são inseridos no DOM utilizando:

```javascript
textContent
```

em vez de inserir diretamente HTML recebido da API.

Isso reduz o risco de execução de conteúdo HTML/JavaScript fornecido por usuários.

---

# 📁 Separação do Frontend

Os arquivos foram separados para melhorar organização e segurança.

## HTML

```text
templates/dashboard.html
```

## CSS

```text
static/css/dashboard.css
```

## JavaScript

```text
static/js/dashboard.js
```

O HTML não deve conter o código completo de CSS ou JavaScript.

Da mesma forma:

```text
CSS ≠ JavaScript
JavaScript ≠ HTML
Python ≠ HTML
```

Cada responsabilidade possui seu próprio arquivo.

---

# 📡 Principais Endpoints

## Health Check

```http
GET /health
```

Verifica se a API está funcionando.

---

## Login

```http
POST /auth/token
```

Responsável pela autenticação.

---

## Tickets

```http
POST /tickets
GET /tickets
GET /tickets/{ticket_id}
DELETE /tickets/{ticket_id}
```

---

## Prediction

```http
POST /predict
```

Endpoint reservado para a funcionalidade de previsão/classificação relacionada à IA.

---

## Dashboard

```http
GET /dashboard
```

Interface web da aplicação.

---

## Swagger

A documentação da API está disponível em:

```text
/docs
```

---

# 🧪 Testes de Segurança

O TP2 prevê testes automatizados relacionados à segurança.

Entre os cenários previstos:

### 1. Endpoint protegido sem token

Uma requisição sem JWT deve ser rejeitada.

---

### 2. BOLA

Um usuário autenticado não deve conseguir acessar o ticket pertencente a outro usuário.

---

### 3. Campo adicional

Um payload contendo um campo não previsto pelo schema deve ser rejeitado.

Exemplo:

```json
{
    "customer_name": "João",
    "customer_email": "joao@email.com",
    "campo_extra": "ataque"
}
```

A API deve rejeitar a requisição.

---

# 🕵️ OWASP ZAP

O projeto utiliza o **OWASP ZAP** para realizar análise passiva da aplicação.

O objetivo é identificar possíveis problemas de segurança observáveis nas respostas HTTP.

O processo previsto é:

```text
Executar FastAPI
       ↓
Abrir aplicação
       ↓
Executar ZAP
       ↓
Passive Scan
       ↓
Exportar relatório
       ↓
Analisar findings
       ↓
Corrigir problemas
       ↓
Executar novo scan
```

Os resultados classificados como Medium ou High devem ser analisados individualmente.

---

# 🔐 Práticas de Segurança Implementadas

Até o momento, o projeto possui os seguintes controles:

| Controle                          | Estado                |
| --------------------------------- | --------------------- |
| JWT Authentication                | ✅ Implementado        |
| bcrypt                            | ✅ Implementado        |
| BOLA / Ownership                  | ✅ Implementado        |
| Pydantic `extra="forbid"`         | ✅ Implementado        |
| Sanitização de entradas           | ✅ Implementado        |
| SQLModel / queries parametrizadas | ✅ Implementado        |
| Rate limiting com Redis           | ✅ Implementado        |
| CORS allowlist                    | ✅ Implementado        |
| X-Frame-Options                   | ✅ Implementado        |
| X-Content-Type-Options            | ✅ Implementado        |
| HSTS em produção                  | ✅ Implementado        |
| CSP                               | ✅ Implementado        |
| Alembic                           | ✅ Implementado        |
| Separação HTML/CSS/JS             | ✅ Implementado        |
| Testes automatizados de segurança | 🔄 Em desenvolvimento |
| OWASP ZAP                         | 🔄 Em desenvolvimento |
| IA para classificação/atendimento | 🔄 Em desenvolvimento |

---

# 🚀 Instalação

## 1. Clonar o projeto

```bash
git clone https://github.com/WeslleySoaresm/FintechGuard.git
```

Entrar no diretório:

```bash
cd FintechGuard
```

---

# 🐍 Criar ambiente virtual

Linux/macOS:

```bash
python3 -m venv .venv
```

Ativar:

```bash
source .venv/bin/activate
```

Windows:

```powershell
python -m venv .venv
```

Ativar:

```powershell
.venv\Scripts\activate
```

---

# 📦 Instalar dependências

```bash
pip install -r requirements.txt
```

---

# 🔴 Redis

O projeto utiliza Redis para rate limiting.

Com Docker:

```bash
docker compose up -d redis
```

Verificar:

```bash
docker ps
```

---

# 🗄️ Executar migrations

Depois de configurar o ambiente:

```bash
alembic upgrade head
```

Verificar a migration atual:

```bash
alembic current
```

---

# 👤 Criar usuário

O projeto possui um script para criação de usuário.

Inicialmente:

```bash
touch scripts/__init__.py
touch data/__init__.py
touch models/__init__.py
```

Depois:

```bash
python -m scripts.create_user
```

---

# ▶️ Executar a aplicação

Utilizando Uvicorn:

```bash
uvicorn main:app --reload
```

A API ficará disponível localmente em:

```text
http://127.0.0.1:8000
```

---

# 📚 Documentação da API

Swagger:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

---

# 🧪 Executar testes

```bash
pytest
```

Para maior detalhamento:

```bash
pytest -v
```

---

# 🔍 Testes manuais

Health check:

```bash
curl http://127.0.0.1:8000/health
```

Teste de CORS autorizado:

```bash
curl -i \
-H "Origin: http://localhost:5173" \
http://127.0.0.1:8000/health
```

A resposta deve conter:

```text
access-control-allow-origin: http://localhost:5173
```

---

# 🔒 Teste de endpoint protegido

Sem token:

```bash
curl -i http://127.0.0.1:8000/tickets
```

A API deve rejeitar a requisição.

Com token:

```text
Authorization: Bearer <JWT>
```

o acesso é permitido conforme as permissões do usuário.

---

# 🧠 Inteligência Artificial

A arquitetura do projeto está sendo preparada para incorporar funcionalidades de Inteligência Artificial.

O objetivo final é utilizar IA no contexto de:

* classificação de tickets;
* atendimento automatizado;
* análise de solicitações;
* identificação de possíveis comportamentos fraudulentos;
* proteção contra vazamento de informações;
* segurança de agentes de IA.

A implementação completa do agente de IA será desenvolvida nas etapas posteriores do projeto.

---

# 🛡️ Segurança de Agentes de IA

Uma etapa futura do projeto terá foco específico em segurança de agentes de IA.

Entre os pontos de interesse:

```text
Prompt Injection
Data Leakage
Excessive Agency
Insecure Output Handling
Improper Access Control
Sensitive Information Disclosure
```

O objetivo é avaliar não apenas a segurança da API tradicional, mas também os riscos introduzidos por sistemas baseados em agentes de IA.

---

# 🗺️ Roadmap

## TP1

* [x] Estrutura inicial do projeto
* [x] FastAPI
* [x] Dataset
* [x] EDA inicial
* [x] Autenticação JWT
* [x] Estrutura inicial do banco

---

## TP2

### Dados

* [x] Limpeza inicial do dataset
* [x] Verificação de duplicados
* [x] Análise exploratória
* [x] Heatmap
* [x] Scatter plots
* [ ] Teste estatístico final documentado
* [ ] Interpretação final da hipótese

### API

* [x] SQLModel
* [x] Alembic
* [x] User
* [x] Ticket
* [x] ConversationMessage
* [x] CRUD básico de tickets
* [x] JWT
* [x] bcrypt

### Segurança

* [x] `extra="forbid"`
* [x] Sanitização
* [x] Proteção BOLA
* [x] Rate limiting
* [x] Redis
* [x] CORS
* [x] Security Headers
* [x] CSP
* [x] HSTS em produção
* [ ] Testes automatizados completos
* [ ] OWASP ZAP
* [ ] Análise final dos findings

### Frontend

* [x] Login
* [x] Dashboard
* [x] Separação CSS/JS
* [x] Filtros
* [x] Indicadores
* [x] Criação de tickets
* [x] Modal de detalhes
* [x] Tratamento seguro de conteúdo

---

# 📋 Próximas etapas

As próximas atividades do TP2 são:

1. Finalizar os testes automatizados de segurança.
2. Executar o OWASP ZAP.
3. Analisar os findings encontrados.
4. Corrigir eventuais vulnerabilidades.
5. Reexecutar o ZAP.
6. Finalizar a análise estatística.
7. Documentar os resultados.
8. Atualizar o relatório acadêmico.
9. Consolidar a documentação no GitHub.

Depois do TP2:

```text
TP3
 ↓
TP4
 ↓
TP5
 ↓
Apresentação final
 ↓
Teste de segurança do agente de IA
```

---

# 📌 Princípios do Projeto

O FintechGuard segue alguns princípios fundamentais:

### Segurança desde o desenvolvimento

A segurança não deve ser adicionada somente no final do projeto.

### Menor privilégio

Um usuário deve acessar somente os recursos necessários para sua função.

### Validação de entrada

Dados externos devem ser considerados não confiáveis.

### Defesa em profundidade

Nenhum mecanismo isolado deve ser considerado suficiente.

Exemplo:

```text
JWT
+
Ownership
+
Validação
+
Sanitização
+
Rate Limiting
+
Security Headers
+
CORS
+
CSP
```

### Separação de responsabilidades

Frontend, API, persistência, autenticação e análise de dados possuem responsabilidades distintas.

---

# 📄 Status do Projeto

**Status atual:** Desenvolvimento — TP2

O projeto encontra-se em evolução acadêmica e não deve ser considerado uma aplicação bancária pronta para produção.

Os mecanismos implementados têm finalidade educacional e de demonstração de práticas de desenvolvimento seguro.

---

# 👨‍🎓 Contexto Acadêmico

**Projeto:** FintechGuard — Atendimento Bancário

**Disciplina:** Análise e Segurança de Agentes de IA [26E3_5]

**Professor:** Ricardo Pires Mesquita

**Alunos:**

* Weslley Soares
* Bruno Santos

---

# 📜 Licença

O dataset utilizado no projeto é disponibilizado sob a licença indicada pela fonte original do conjunto de dados.

O código deste projeto é desenvolvido para fins acadêmicos.

---

# 🔗 Repositório

GitHub:

```text
https://github.com/WeslleySoaresm/FintechGuard
```

---

## FintechGuard

**Atendimento bancário + segurança + análise de dados + Inteligência Artificial**

> Segurança não é uma funcionalidade isolada. É uma característica da arquitetura.

````

### Para colocar no projeto

Salve exatamente como:

```text
FintechGuard/
└── README.md
````

Depois:

```bash
git add README.md
git commit -m "docs: add comprehensive TP2 project documentation"
git push origin main
```

Eu manteria **esse README separado do commit anterior do TP2**. Assim o histórico fica limpo: primeiro você registra as implementações, depois registra a documentação. Isso ajuda bastante quando o professor abrir o GitHub e quiser entender a evolução do projeto.
