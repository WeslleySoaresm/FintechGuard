# FintechGuard — Relatório Final de Auditoria de Segurança da API

**Projeto:** FintechGuard — Atendimento Bancário Seguro  
**Disciplina:** Projeto de Bloco — Análise e Segurança de Agentes de IA [26E3_5]  
**Equipe:** Weslley Soares e Bruno Santos  
**Aplicação:** API FastAPI  
**Ferramenta de análise:** OWASP ZAP 2.17.0  
**Tipo de análise realizada:** Passive Scan  
**Alvo:** `http://127.0.0.1:8000`  
**Data da evidência apresentada:** 25 de outubro de 2026  
**Estado da auditoria:** Prontidão condicionada à validação dos controles pendentes

---

## 1. Objetivo

Este documento consolida os resultados disponíveis da análise de segurança do FintechGuard, registra os controles avaliados e define os critérios necessários para autorizar um teste de intrusão (*penetration test* ou pentest).

A avaliação considera os cabeçalhos HTTP, a política CORS, a Content Security Policy (CSP), a autenticação JWT, a exposição de endpoints, a validação de entradas e a necessidade de verificar autorização por usuário.

A análise apresentada é baseada principalmente em uma varredura passiva do OWASP ZAP e em testes manuais com `curl`. Esses procedimentos ajudam a identificar configurações potencialmente inseguras, mas não substituem um pentest autorizado nem comprovam a ausência de vulnerabilidades.

## 2. Sumário executivo

A aplicação foi executada localmente e diversas rotas responderam com HTTP `200 OK`, incluindo `/login`, `/dashboard`, `/auth/token` e `/api/public/settings`.

Os testes manuais anteriores também mostraram que:

- `X-Frame-Options: DENY` é retornado pela API;
- `X-Content-Type-Options: nosniff` é retornado pela API;
- a origem CORS autorizada `http://localhost:5173` recebe permissão;
- a origem externa testada não recebeu `Access-Control-Allow-Origin`;
- o HSTS está condicionado ao ambiente de produção;
- o CDN jsDelivr retorna CORS permissivo para seu CSS público do Swagger UI, comportamento que não comprova uma vulnerabilidade CORS da API.

A captura do ZAP apresenta respostas bem-sucedidas de várias rotas, mas um status HTTP `200` não demonstra, isoladamente, que o controle de acesso está correto.

**Conclusão preliminar:** o projeto possui evidências iniciais suficientes para continuar a preparação do pentest em ambiente local controlado. A autorização definitiva depende da validação dos controles de autenticação, autorização, exposição de dados, paginação, CSP e dos alertas remanescentes do ZAP.

---

## 3. Escopo e metodologia

### 3.1 Escopo observado

A captura fornecida contém as seguintes requisições:

| ID ZAP | Método | Endpoint | Código HTTP | Tamanho do corpo |
|---|---|---|---:|---:|
| 51 | GET | `/` | 200 | 9.385 bytes |
| 53 | GET | `/api/public/settings` | 200 | 507 bytes |
| 56 | GET | `/login` | 200 | 2.129 bytes |
| 57 | POST | `/auth/token` | 200 | 160 bytes |
| 59 | GET | `/dashboard` | 200 | 25.101 bytes |
| 60 | GET | `/tickets?limit=10000` | 200 | 300.452 bytes |
| 61 | GET | `/login` | 200 | 2.129 bytes |

Os tamanhos e códigos acima correspondem à captura fornecida. O significado dos campos `RTT` e `Alerta Máximo` deve ser interpretado conforme a visualização e a versão do ZAP utilizadas; esses valores não representam, por si só, uma classificação de segurança.

### 3.2 Metodologia

A avaliação foi conduzida por meio de:

1. Inicialização local da aplicação FastAPI;
2. Navegação pelas páginas e rotas principais por meio do proxy do OWASP ZAP;
3. Captura de requisições e respostas HTTP;
4. Execução de Passive Scan;
5. Testes manuais dos cabeçalhos HTTP e da política CORS com `curl`;
6. Revisão da configuração de middleware e dos controles implementados;
7. Definição de verificações adicionais antes do pentest.

Não há evidência apresentada de execução de Active Scan. Portanto, este documento não afirma que houve exploração ativa ou que a aplicação passou por um teste de intrusão completo.

---

## 4. Checklist consolidado de segurança

### 4.1 Cabeçalhos HTTP e políticas do navegador

| ID | Controle | Status | Evidência e observação |
|---|---|---|---|
| SEC-01 | `X-Frame-Options` | Resolvido em teste local | Resposta de `/health` contém `DENY`. |
| SEC-02 | `X-Content-Type-Options` | Resolvido em teste local | Resposta de `/health` contém `nosniff`. |
| SEC-03 | HSTS | Parcialmente validado | Teste automatizado simula produção. Falta comprovar o header no ambiente real HTTPS, quando disponível. |
| SEC-04 | CSP — `form-action` | Pendente de revalidação | A diretiva foi incluída na configuração, mas é necessário confirmar o resultado do novo Passive Scan. |
| SEC-05 | CSP — `script-src 'unsafe-inline'` | Pendente de validação | Verificar se a política efetiva ainda permite scripts inline e se isso é necessário. |
| SEC-06 | CSP — `style-src 'unsafe-inline'` | Pendente de validação | Verificar a política efetiva e restringir estilos inline quando possível. |
| SEC-07 | CORS da API | Parcialmente validado | Testes em `/health` mostram comportamento restritivo para a origem externa testada. Falta identificar a instância do alerta original no ZAP. |
| SEC-08 | CORS do CDN jsDelivr | Contextualizado | O CSS público do Swagger UI retorna `Access-Control-Allow-Origin: *`. Isso não demonstra, por si só, falha CORS da API. |

### 4.2 Autenticação, autorização e dados

| ID | Controle | Status | Evidência e observação |
|---|---|---|---|
| SEC-09 | Requisição protegida sem token | Testado anteriormente | O teste automatizado reportado espera `401`. |
| SEC-10 | Token inválido | Testado anteriormente | O teste automatizado reportado espera `401`. |
| SEC-11 | JWT válido com usuário existente | Pendente de evidência de integração | Teste com `verify_token` simulado não comprova a integração real com JWT e banco de dados. |
| SEC-12 | Autorização por recurso (BOLA/IDOR) | Pendente de validação final | Executar testes com dois usuários e tickets distintos. |
| SEC-13 | Validação de entrada | Parcialmente validado | Existem testes de validação, mas é necessária revisão das rotas e dos modelos. |
| SEC-14 | Rate limiting | Pendente de evidência final | Demonstrar o limite, o código `429` e o comportamento diante de falhas do Redis, se utilizado. |
| SEC-15 | Paginação e limites | Pendente | A rota `/tickets?limit=10000` retornou `200` e um corpo de aproximadamente 300 KB. Verificar o limite máximo permitido e se o acesso exige autenticação. |
| SEC-16 | Exposição de dados | Pendente de revisão | Inspecionar os campos retornados por `/tickets` e confirmar que informações pessoais ou internas não são expostas indevidamente. |
| SEC-17 | Segredos e configuração | Pendente de revisão final | Confirmar que não existem segredos padrão inseguros no ambiente avaliado e que arquivos de configuração sensíveis não estão versionados. |
| SEC-18 | Tratamento de erros e logs | Pendente de revisão final | Verificar ausência de stack traces, tokens e dados pessoais desnecessários nas respostas e logs. |
| SEC-19 | Nova varredura OWASP ZAP | Pendente | Executar o Passive Scan após as alterações e preservar o relatório exportado. |
| SEC-20 | Isolamento do ambiente de pentest | Pendente de confirmação | Definir escopo autorizado, dados fictícios, credenciais de teste e procedimento de recuperação. |

**Nota sobre status:** “Resolvido em teste local” se aplica somente ao controle e ao cenário efetivamente testados. “Pendente” não significa que a vulnerabilidade foi comprovada, mas que ainda não há evidência suficiente para aprovar o controle.

---

## 5. Análise dos principais pontos de atenção

### 5.1 Endpoint `/tickets?limit=10000`

A requisição registrada pelo ZAP retornou HTTP `200 OK`, com corpo de aproximadamente 300 KB.

Esse resultado não comprova uma vulnerabilidade. Entretanto, justifica verificar:

- Se a rota exige autenticação;
- Se cada usuário acessa apenas os tickets autorizados;
- Se o parâmetro `limit` possui um limite máximo no servidor;
- Se os dados retornados incluem e-mail, nomes ou outros dados pessoais desnecessários;
- Se a paginação é eficiente e resistente a consultas excessivamente grandes.

**Critério de aprovação:** a API deve impor limites no servidor, validar a autorização de cada consulta e retornar somente os dados necessários ao usuário autorizado.

### 5.2 Endpoint `/auth/token`

O registro mostra um `POST` com status `200 OK` e corpo de 160 bytes.

Isso é compatível com uma resposta de autenticação bem-sucedida, mas o registro resumido não demonstra se:

- Credenciais incorretas são rejeitadas;
- Tokens expirados são recusados;
- As tentativas são limitadas;
- O token contém somente as informações necessárias;
- Os segredos de assinatura são adequados e protegidos.

Esses cenários devem ser verificados em testes controlados, utilizando contas fictícias.

### 5.3 Endpoint `/dashboard`

A rota respondeu `200 OK` e retornou aproximadamente 25 KB. Como o dashboard pode conter dados associados à sessão, é necessário verificar se o conteúdo está protegido contra acesso não autenticado e se a autorização está corretamente aplicada.

O código HTTP, isoladamente, não permite concluir se o acesso foi legítimo ou indevido. A conclusão depende do fluxo de autenticação da rota e do conteúdo efetivo da resposta.

### 5.4 CORS e recurso externo

O CSS do Swagger UI hospedado no jsDelivr retornou:

```http
Access-Control-Allow-Origin: *
```

Esse comportamento é comum para recursos públicos distribuídos por CDN. Os testes realizados diretamente contra `/health` não reproduziram esse cabeçalho para a origem externa utilizada.

**Tratamento:** localizar a URL e a resposta exatas da instância de CORS no OWASP ZAP. Não classificar o alerta como vulnerabilidade da API enquanto não houver evidência de que a própria API está autorizando origens indiscriminadamente.

### 5.5 CSP

A configuração inclui `form-action 'self'`, mas o estado final deve ser confirmado na resposta HTTP e em uma nova varredura.

As permissões `unsafe-inline` em `script-src` ou `style-src`, caso ainda estejam presentes, devem ser justificadas e reduzidas sempre que possível. Uma política de desenvolvimento não deve ser apresentada como prova de que a política de produção está endurecida.

---

## 6. Evidências reproduzíveis

### 6.1 Cabeçalhos HTTP

Comando utilizado:

```bash
curl -i http://127.0.0.1:8000/health
```

Resultado observado: HTTP `200 OK`, com `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff` e CSP.

### 6.2 CORS — origem externa

Comando utilizado:

```bash
curl -i \
  -H "Origin: https://site-nao-autorizado.example" \
  http://127.0.0.1:8000/health
```

Resultado observado: a resposta não contém `Access-Control-Allow-Origin`.

### 6.3 CORS — origem permitida

Comando utilizado:

```bash
curl -i \
  -H "Origin: http://localhost:5173" \
  http://127.0.0.1:8000/health
```

Resultado observado:

```http
Access-Control-Allow-Origin: http://localhost:5173
Vary: Origin
```

### 6.4 CORS — CDN

Comando utilizado:

```bash
curl -I \
  "https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css"
```

Resultado observado: o CDN respondeu `HTTP/2 200` e `Access-Control-Allow-Origin: *`.

Essa evidência pertence ao recurso externo consultado e não comprova uma configuração CORS permissiva na API local.

### 6.5 Testes automatizados

A suíte de testes deve ser executada e os resultados completos preservados:

```bash
pytest tests -v
```

Os testes que simulam dependências devem ser identificados como testes de rota. Para comprovar a integração real de autenticação, são necessários testes adicionais com JWT válido e usuário existente no banco de dados de teste.

---

## 7. Plano de ação antes do pentest

| Prioridade | Ação | Critério de conclusão |
|---|---|---|
| Alta | Validar autenticação e autorização das rotas protegidas | Requisições sem autenticação são rejeitadas e usuários não acessam recursos alheios. |
| Alta | Revisar paginação e conteúdo de `/tickets` | Limite máximo aplicado e dados retornados restritos ao necessário. |
| Alta | Validar segredos e configuração do ambiente | Nenhum segredo padrão inseguro no ambiente avaliado. |
| Alta | Definir escopo e isolamento do pentest | Autorização documentada, dados fictícios e procedimento de recuperação definidos. |
| Média | Revalidar CSP e alertas do ZAP | Nova varredura e evidências arquivadas. |
| Média | Confirmar CORS na instância original do alerta | URL identificada e comportamento reproduzido ou alerta contextualizado. |
| Média | Verificar rate limiting | Testes de limite e falha de dependência documentados. |
| Média | Revisar logs e erros | Ausência de exposição indevida de informações. |

---

## 8. Critérios de prontidão

A API poderá ser considerada pronta para iniciar o pentest autorizado quando:

1. O escopo, o ambiente e a autorização estiverem documentados;
2. Os testes de autenticação e autorização tiverem resultados satisfatórios;
3. O acesso aos tickets estiver corretamente isolado por usuário;
4. Os limites de paginação e os campos retornados tiverem sido validados;
5. Os alertas CSP e CORS estiverem reavaliados com evidências;
6. Os segredos e as configurações de produção estiverem revisados;
7. Os testes automatizados e o relatório final do ZAP estiverem preservados;
8. Os riscos residuais estiverem corrigidos ou formalmente aceitos por um responsável.

O teste deve ser executado exclusivamente contra o ambiente autorizado, preferencialmente isolado, com contas e dados fictícios.

---

## 9. Conclusão final

A evidência disponível demonstra que o FintechGuard está em uma fase adequada para continuar a preparação de seu pentest. A configuração CORS observada nos testes manuais é restritiva para as origens testadas, e os cabeçalhos `X-Frame-Options` e `X-Content-Type-Options` estão presentes nas respostas verificadas.

Entretanto, a captura do OWASP ZAP não comprova, por si só, a segurança de autenticação, autorização, exposição de dados ou limites de paginação. A resposta de `/tickets?limit=10000`, em particular, exige validação adicional antes de considerar a API aprovada para a avaliação ofensiva.

**Resultado da auditoria: prontidão condicionada.**

A autorização definitiva para o pentest depende do fechamento dos itens prioritários, da revalidação dos alertas e do registro das evidências de segurança.

---

## 10. Registro de aprovação

| Campo | Valor |
|---|---|
| Responsável pela revisão | A preencher |
| Data de aprovação | A preencher |
| Ambiente autorizado | A identificar |
| Resultado | Prontidão condicionada |
| Aprovação para pentest | Pendente de validação final |
| Evidências anexadas | Captura do ZAP e testes manuais; relatório exportado a anexar |
