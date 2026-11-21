# Relatório de Testes Automatizados de Segurança

## 1. Identificação

- Projeto: FintechGuard
- Arquivo de testes: `tests/test_agent.py`
- Framework: Pytest
- API: FastAPI
- Banco utilizado nos testes: SQLite em memória
- Total de testes executados: 29
- Resultado: 29 aprovados
- Tempo de execução registrado: 2,92 segundos

## 2. Objetivo

Verificar os mecanismos de segurança do agente de atendimento bancário, contemplando autenticação, autorização, proteção contra acesso indevido a dados, validação de entradas, identificação de mensagens suspeitas e integridade das operações no banco de dados.

## 3. Casos de teste

### 3.1 Autenticação JWT

**Teste:** `test_agent_sem_token_deve_retornar_401`

**Objetivo:** verificar se o endpoint do agente impede requisições sem autenticação.

**Procedimento:** enviar uma requisição POST para `/agent` sem token de autenticação.

**Resultado esperado:** HTTP 401.

**Resultado obtido:** aprovado. A API rejeitou a requisição.

### 3.2 Autorização e proteção BOLA

**Teste:** `test_agent_nao_deve_aceitar_ticket_de_outro_usuario`

**Objetivo:** impedir que um usuário acesse tickets pertencentes a outra conta.

**Procedimento:** autenticar o usuário 1 e tentar utilizar um ticket pertencente ao usuário 2.

**Resultado esperado:** HTTP 404, impedindo o acesso ao recurso de outro usuário.

**Resultado obtido:** aprovado.

Teste complementar: `test_agent_nao_deve_salvar_mensagens_em_ticket_de_outro_usuario`.

### 3.3 Validação de entradas

**Testes:**
- `test_agent_nao_deve_aceitar_campo_extra`
- `test_agent_nao_deve_aceitar_mensagem_vazia`

**Objetivo:** impedir o processamento de dados que não respeitem os schemas definidos.

**Procedimento:** enviar campos não permitidos e mensagens vazias.

**Resultado esperado:** HTTP 422.

**Resultado obtido:** aprovado.

### 3.4 Controle de acesso às conversas

**Teste:** `test_historico_nao_expoe_conversa_de_outro_usuario`

**Objetivo:** garantir o isolamento das conversas entre usuários.

**Procedimento:** criar uma conversa pertencente a outro usuário e tentar consultá-la com a conta autenticada.

**Resultado esperado:** a conversa não deve aparecer na listagem e a consulta direta deve retornar HTTP 404.

**Resultado obtido:** aprovado.

Teste complementar: `test_historico_requer_autenticacao`.

### 3.5 Proteção contra Prompt Injection

**Teste:** `test_agente_nao_deve_ser_manipulado_por_prompt_injection`

**Objetivo:** verificar se mensagens que tentam modificar as instruções internas do agente são identificadas e tratadas de acordo com as regras de segurança da aplicação.

**Procedimento:** executar cinco cenários com mensagens que solicitam a revelação de instruções internas ou dados confidenciais.

**Resultado esperado:** as respostas não devem revelar as informações protegidas e a classificação deve seguir os critérios definidos no teste.

**Resultado obtido:** os cinco cenários foram aprovados.

**Limitação:** o executor do agente foi simulado com `monkeypatch`. Portanto, este teste verifica o comportamento da API e das regras locais, não a resistência do modelo real da OpenAI a ataques de Prompt Injection.

### 3.6 Classificação de risco

**Teste:** `test_agent_deve_identificar_nivel_de_risco`

**Objetivo:** verificar a classificação de mensagens de acordo com o nível de risco.

**Procedimento:** testar quatro situações: atendimento comum, cobrança duplicada, compra não reconhecida e solicitação suspeita de senha.

**Resultado esperado:** classificação coerente entre os níveis low, medium, high e critical, com encaminhamento correspondente.

**Resultado obtido:** os quatro cenários foram aprovados.

### 3.7 Integridade transacional

**Teste:** `test_agent_deve_fazer_rollback_quando_commit_falhar`

**Objetivo:** verificar se uma falha na persistência provoca rollback e evita registros incompletos.

**Procedimento:** simular uma falha no commit da transação.

**Resultado esperado:** HTTP 500, execução do rollback e ausência de mensagens parcialmente salvas.

**Resultado obtido:** aprovado.

## 4. Resultado geral

Comando executado:

```bash
pytest tests/test_agent.py -v
```

Resultado:

```text
29 passed, 70 warnings in 2.92s
```

Todos os 29 casos de teste foram aprovados na execução registrada.

Os avisos identificados estão relacionados à utilização de `datetime.utcnow()`, método depreciado nas versões recentes do Python.

## 5. Estratégia de isolamento dos testes

O arquivo utiliza SQLite em memória e fixtures para preparar e limpar o banco de dados durante os testes.

Também utiliza `monkeypatch` para substituir a execução do agente por uma resposta controlada, evitando dependência de chamadas externas à API da OpenAI.

Essa abordagem permite testar de forma reproduzível as regras da aplicação, a autenticação, as autorizações e a persistência.

## 6. Evidências

- `resultado_test_agent.txt`: saída completa da execução do Pytest.
- `evidencias/01-test-agent-pytest.png`: captura dos 29 testes aprovados.
- `evidencias/02-autenticacao-bola.png`: evidência dos testes de autenticação e autorização.
- `evidencias/03-prompt-injection.png`: evidência dos cenários de Prompt Injection.
- `evidencias/04-validacao-e-integridade.png`: evidência dos testes de validação e rollback.

## 7. Conclusão

Os testes automatizados do agente verificam controles importantes de segurança, especialmente autenticação JWT, autorização por usuário, proteção contra acesso indevido a conversas e tickets, validação de entradas e integridade transacional.

A execução registrada apresentou 29 casos aprovados. Os testes simulados do agente devem ser complementados por avaliações específicas do modelo real e por testes das demais camadas de segurança da API.