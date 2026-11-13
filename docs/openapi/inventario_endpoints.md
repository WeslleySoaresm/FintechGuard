# Inventário de Endpoints e Schemas - FintechGuard

## 1. Identificação

- Projeto: FintechGuard
- API: FintechGuard API
- Versão: 1.0.0
- Especificação: OpenAPI 3.1.0
- Documentação interativa: `/docs`
- Especificação JSON: `/openapi.json`

## 2. Objetivo

Este documento apresenta o inventário dos endpoints da API FintechGuard, identificando os métodos HTTP, parâmetros de entrada, schemas de requisição, estruturas de resposta e requisitos de autenticação.

## 3. Inventário de endpoints

A especificação exportada apresentou 30 operações HTTP.

| Nº | Método | Endpoint | Entrada / Schema |
|---:|---|---|---|
| 1 | POST | `/auth/token` | LoginRequest |
| 2 | GET | `/tickets/root` | Sem corpo |
| 3 | POST | `/tickets` | TicketCreate |
| 4 | GET | `/tickets` | skip, limit |
| 5 | GET | `/tickets/{ticket_id}` | ticket_id |
| 6 | DELETE | `/tickets/{ticket_id}` | ticket_id |
| 7 | POST | `/predict` | PredictRequest |
| 8 | GET | `/dashboard` | Sem corpo |
| 9 | GET | `/admin/login` | Sem corpo |
| 10 | POST | `/admin/login` | AdminLogin |
| 11 | GET | `/admin` | Sem corpo |
| 12 | GET | `/admin/api/settings` | Sem corpo |
| 13 | PUT | `/admin/api/settings` | SettingsUpdate |
| 14 | POST | `/admin/api/upload` | Multipart/form-data |
| 15 | POST | `/admin/logout` | Sem corpo |
| 16 | GET | `/` | Sem corpo |
| 17 | GET | `/sobre` | Sem corpo |
| 18 | GET | `/seguranca` | Sem corpo |
| 19 | GET | `/servicos` | Sem corpo |
| 20 | GET | `/contato` | Sem corpo |
| 21 | GET | `/privacidade` | Sem corpo |
| 22 | GET | `/api/public/settings` | Sem corpo |
| 23 | GET | `/agent` | Sem corpo |
| 24 | POST | `/agent` | AgentRequest |
| 25 | GET | `/agent/conversations` | limit, offset |
| 26 | GET | `/agent/conversations/{conversation_id}` | conversation_id |
| 27 | POST | `/classify/` | ClassificationRequest |
| 28 | GET | `/health` | Sem corpo |
| 29 | GET | `/login` | Sem corpo |
| 30 | GET | `/diagnostico-interno` | Header de diagnóstico |

## 4. Schemas de entrada e saída identificados

| Endpoint | Entrada | Saída |
|---|---|---|
| POST `/auth/token` | LoginRequest | TokenResponse |
| POST `/tickets` | TicketCreate | TicketResponse |
| GET `/tickets` | skip, limit | Lista de TicketResponse |
| GET `/tickets/{ticket_id}` | ticket_id | TicketResponse |
| DELETE `/tickets/{ticket_id}` | ticket_id | HTTP 204 |
| POST `/predict` | PredictRequest | PredictResponse |
| POST `/admin/login` | AdminLogin | Revisar resposta |
| PUT `/admin/api/settings` | SettingsUpdate | Revisar resposta |
| POST `/admin/api/upload` | Multipart/form-data | Revisar resposta |
| POST `/agent` | AgentRequest | AgentResponse |
| GET `/agent/conversations` | limit, offset | Revisar resposta |
| GET `/agent/conversations/{conversation_id}` | conversation_id | Revisar resposta |
| POST `/classify/` | ClassificationRequest | ClassificationResponse |

## 5. Endpoints sem corpo de requisição

Os endpoints GET e alguns endpoints DELETE não precisam receber um corpo JSON.

Os parâmetros são enviados pela URL ou query string, conforme o contrato de cada operação.

As páginas HTML retornam conteúdo `text/html`, não objetos JSON.

## 6. Pendências de documentação

Algumas respostas aparecem com schema vazio `{}` na especificação exportada.

Isso não significa necessariamente erro de execução. Significa que a estrutura da resposta ainda precisa ser analisada e documentada.

As operações que precisam de revisão são:

- GET `/tickets/root`
- POST `/admin/login`
- GET `/admin/api/settings`
- PUT `/admin/api/settings`
- POST `/admin/api/upload`
- POST `/admin/logout`
- GET `/api/public/settings`
- GET `/agent/conversations`
- GET `/agent/conversations/{conversation_id}`
- GET `/health`
- GET `/diagnostico-interno`

Os contratos definitivos dessas operações devem ser definidos a partir das respostas reais implementadas no código.

## 7. Evidências

- `openapi.json`: especificação exportada.
- `validacao_openapi.txt`: resultado do validador.
- `evidencias/01-swagger-documentacao.png`: documentação interativa.
- `evidencias/02-openapi-validacao.png`: validação estrutural.
- `evidencias/03-testes-pytest.png`: execução dos testes.
- `evidencias/04-endpoints-documentados.png`: inventário de endpoints.

## 8. Conclusão

A API FintechGuard possui especificação OpenAPI 3.1.0 exportada e validada estruturalmente. Foram identificadas 30 operações HTTP, com schemas de entrada e saída definidos para os principais endpoints.

A etapa seguinte consiste em revisar as respostas ainda sem schemas explícitos e assegurar que a documentação represente fielmente o comportamento da aplicação.