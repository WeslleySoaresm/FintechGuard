# Evidências de testes

## Execução

Na raiz do repositório, com as dependências instaladas:

```bash
pytest -q
```

## Cobertura relevante

A suíte cobre validação dos esquemas, autenticação de rotas protegidas, autorização por usuário (BOLA), limites de requisição, operações de tickets, análise do agente e persistência do histórico. Para o histórico do agente, os casos verificam listagem e abertura de mensagens, rejeição de acesso a conversa alheia, paginação, autenticação e associação de ticket próprio ao retomar uma conversa.

Os testes unitários do agente simulam a autenticação e a resposta do provedor de IA para serem determinísticos. Eles validam a lógica HTTP e a persistência local, não substituindo testes de integração com JWT real, provedor externo ou ambiente de produção.
