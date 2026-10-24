

# 🛡️ FintechGuard - Documentação dos Testes de Segurança

Esta suite de testes valida os mecanismos críticos de segurança da API do **FintechGuard**, cobrindo autenticação, autorização (BOLA), validação estrita de esquemas e proteção contra uso excessivo.

---

## 🚀 Como Executar os Testes

Certifique-se de que o seu ambiente virtual está ativado e que as dependências estão instaladas. Para executar todos os testes de segurança com detalhe no terminal, utilize o comando:

```bash
pytest tests/ -v

```

---

## 🧩 O Que Cada Função e Fixture Faz

Abaixo encontra-se o mapeamento técnico de cada componente presente no ficheiro `tests/test_security.py`:

### ⚙️ Fixtures de Suporte

* **`setup_database()`**:
* *O que faz*: Uma fixture com `autouse=True` que inicializa uma base de dados SQLite em memória limpa antes de cada teste e a destrói no final (`SQLModel.metadata.create_all` / `drop_all`), garantindo total isolamento entre os testes.


* **`client()`**:
* *O que faz*: Cria uma instância do `TestClient` do FastAPI aplicando `dependency_overrides` temporários para simular um utilizador autenticado (`user_id: 1`) e injetar a base de dados de teste.



---

### 🧪 Testes de Segurança Implementados

1. **`test_acesso_sem_token_deve_retornar_401()`**
* **Objetivo**: Validar a **Autenticação**.
* **O que faz**: Remove temporariamente os overrides de autenticação e tenta aceder a um endpoint protegido sem enviar nenhum token JWT no cabeçalho. Verifica se a API retorna corretamente o código `401 Unauthorized`.


2. **`test_invalid_token_access()`**
* **Objetivo**: Validar a **Robustez do Token**.
* **O que faz**: Utiliza um cliente limpo para enviar um token falsificado ou malformado (`Bearer token_falsificado_ou_invalido`). Garante que a API rejeita o acesso e retorna `401 Unauthorized`.


3. **`test_usuario_nao_deve_acessar_ticket_de_outro_usuario()`**
* **Objetivo**: Validar a proteção contra **BOLA (Broken Object Level Authorization)**.
* **O que faz**: Cria dinamicamente um ticket associado ao `user_id = 2` na base de dados de testes e tenta aceder a esse mesmo ticket utilizando o contexto do `user_id = 1`. Verifica se o acesso é bloqueado de forma segura (`403 Forbidden` ou `404 Not Found`).


4. **`test_body_nao_deve_aceitar_campo_extra()`**
* **Objetivo**: Validar a **Integridade e Validação de Entradas**.
* **O que faz**: Envia um pedido `POST /tickets` contendo um campo não mapeado no schema Pydantic (`campo_inventado`), testando a diretiva `ConfigDict(extra='forbid')`. Garante que a API rejeita o payload inválido com o código `422 Unprocessable Entity`.


5. **`test_rate_limiting_behavior()`**
* **Objetivo**: Validar o comportamento sob **Carga e Limitação de Requisições**.
* **O que faz**: Dispara uma sequência rápida de múltiplos pedidos consecutivos contra a API para avaliar o comportamento de resposta sob stress e garantir a estabilidade do servidor.



---

