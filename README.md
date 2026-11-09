# FintechGuard

API FastAPI de atendimento financeiro com autenticação, tickets e conversa com agente de IA. O projeto acadêmico também inclui análise exploratória do dataset de suporte, classificador de intenções e controles de segurança.

## Começar

Requisitos: Python 3.11+ e Docker Compose (a configuração do projeto usa API e Redis).

```bash
cp .env.example .env
docker compose up --build
```

A API local fica em `http://localhost:8000`; a documentação OpenAPI fica em `/docs`. Para testes locais: `pip install -r requirements.txt` e `pytest -q`.

## Recursos principais

- `POST /auth/token`: autenticação e rate limit.
- `GET/POST /tickets`: consulta e gestão dos tickets do usuário autenticado.
- `POST /agent`: conversa autenticada, opcionalmente associada a um ticket próprio.
- `GET /agent/conversations`: lista paginada do histórico do usuário.
- `GET /agent/conversations/{conversation_id}`: abre mensagens de uma conversa própria.

As rotas de histórico e a ligação da conversa a tickets validam a identidade do usuário. O backend rejeita IDs de ticket e conversas que não pertencem ao usuário.

## Documentação e evidências

- [Índice de evidências](docs/evidencias/README.md) — EDA, auditoria ZAP, testes, treinamento e diagrama.
- [Formalização da classificação TP3](docs/tp3_formalizacao_classificacao.md).
- [Taxonomia dos dados](docs/data_taxonomy.md).
- [Planejamento TP2](docs/t2_planejamento.md).
- [Modelo CIA](docs/CIA_FINTECHGUARD.md).
- [Evidências e escopo dos testes](docs/evidencias/testes.md).

O export de alertas do OWASP ZAP ainda não está no repositório; o CSV de proxy disponível é somente histórico de requisições. Consulte o [índice de evidências](docs/evidencias/README.md) para o estado e os limites dos artefatos.

## Estrutura

```text
router/                 Rotas FastAPI
models/                 Modelos SQLModel
fintechguard_agents/    Agentes e classificador
static/ templates/      Interface web
tests/                  Testes automatizados
docs/evidencias/        Evidências e relatórios consolidados
data/                   Dados usados no projeto
```
