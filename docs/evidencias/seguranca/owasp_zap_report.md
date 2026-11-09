# Relatório Técnico de Auditoria de Segurança
## FintechGuard — OWASP ZAP Passive Scan

**Projeto:** FintechGuard — Atendimento Bancário Seguro  
**Disciplina:** Projeto de Bloco — Análise e Segurança de Agentes de IA [26E3_5]  
**Equipe:** Weslley Soares e Bruno Santos  
**Alvo da auditoria:** `http://127.0.0.1:8000`  
**Ferramenta:** OWASP ZAP 2.17.0  
**Tipo de análise:** Passive Scan  
**Ambiente:** Desenvolvimento local

---

## 1. Sumário executivo

Este relatório apresenta os resultados da análise passiva de segurança realizada na aplicação FintechGuard com o OWASP ZAP. A avaliação teve como objetivo identificar configurações inseguras de cabeçalhos HTTP, fragilidades na política de segurança de conteúdo (*Content Security Policy* — CSP) e possíveis exposições de informações relacionadas à autenticação.

A análise concentrou-se no tráfego HTTP observado durante a navegação pelas principais funcionalidades da aplicação. Não foi executado *Active Scan*, portanto os resultados não representam uma avaliação intrusiva ou uma comprovação abrangente da ausência de vulnerabilidades.

Os achados foram organizados por severidade, com descrição do risco, impacto potencial, tratamento adotado e recomendações de evolução.

### 1.1 Resumo dos achados

A varredura identificou três alertas de severidade média relacionados à política CSP e um alerta informativo associado ao armazenamento de JWT no `localStorage`.

| Achado | Severidade informada | Tratamento |
|---|---|---|
| CSP: Failure to Define Directive with No Fallback | Medium | Inclusão de `form-action 'self'`, conforme configuração documentada |
| CSP: `script-src` com `unsafe-inline` | Medium | Necessita validação da política efetiva e justificativa técnica |
| CSP: `style-src` com `unsafe-inline` | Medium | Necessita validação da política efetiva e justificativa técnica |
| Information Disclosure — JWT in localStorage | Informational | Risco documentado; migração para armazenamento mais seguro considerada melhoria futura |

> **Nota:** a classificação e o estado de cada achado devem corresponder ao resultado efetivamente observado no OWASP ZAP. A alteração de configuração, por si só, não comprova que um alerta foi resolvido.

---

## 2. Escopo e metodologia

### 2.1 Escopo

A avaliação considerou a aplicação FastAPI em ambiente local, com atenção às seguintes áreas:

- Tela de autenticação (`/login`);
- Painel de controle (`/dashboard`);
- Endpoints relacionados à listagem e criação de tickets (`/tickets`);
- Cabeçalhos HTTP de segurança;
- Política CSP retornada nas respostas;
- Exposição de informações relacionadas ao armazenamento de tokens.

### 2.2 Procedimento de execução

A metodologia foi composta pelas seguintes etapas:

1. Inicialização da API por meio do Uvicorn.
2. Navegação pelas funcionalidades selecionadas através do navegador integrado ao OWASP ZAP.
3. Captura das requisições e respostas HTTP.
4. Execução e análise dos alertas gerados pelo Passive Scan.
5. Inspeção da configuração de segurança da aplicação.
6. Registro dos achados, dos tratamentos adotados e das recomendações.

Comando utilizado para iniciar a aplicação:

```bash
uvicorn main:app --reload
```

A análise passiva observa o tráfego capturado e identifica padrões potencialmente inseguros. Ela não substitui testes de autorização, validação funcional, testes de invasão autorizados ou uma auditoria completa da aplicação.

---

## 3. Resultados consolidados

### 3.1 Achados de severidade média

#### Achado 01 — CSP: Failure to Define Directive with No Fallback

- **Severidade:** Medium
- **Confiança:** High
- **URL observada:** `/login`
- **Área:** Política de segurança de conteúdo
- **Tratamento documentado:** inclusão de `form-action 'self'`

**Descrição**

O alerta indica que a política CSP observada não definia explicitamente uma diretiva de controle do destino dos formulários.

**Risco**

Sem uma política explícita de `form-action`, o navegador pode permitir que formulários sejam enviados para destinos não previstos pela aplicação. Em determinadas condições, isso pode facilitar a exposição de dados submetidos pelo usuário.

A diretiva `default-src` não substitui a necessidade de definir `form-action`, pois ela não funciona como fallback para essa diretiva.

**Medida adotada**

A configuração documentada inclui a seguinte diretiva:

```http
form-action 'self';
```

Ela restringe o envio de formulários à própria origem da aplicação.

**Evidência de validação**

A correção deve ser confirmada inspecionando o cabeçalho CSP retornado pela rota `/login` e executando novamente o Passive Scan. O achado só deve ser marcado como resolvido após essa verificação.

#### Achado 02 — CSP: `script-src` com `unsafe-inline`

- **Severidade:** Medium
- **Confiança:** High
- **URL observada:** `/login`
- **Área:** Execução de JavaScript

**Descrição**

A política CSP de desenvolvimento permite `'unsafe-inline'` na diretiva `script-src`.

**Risco**

Essa permissão reduz a eficácia da CSP contra determinadas formas de Cross-Site Scripting (XSS), pois permite a execução de scripts inline que, em uma política mais restritiva, seriam bloqueados.

**Tratamento e justificativa**

A configuração de desenvolvimento foi mantida permissiva para compatibilidade com os recursos utilizados pela interface e pela documentação interativa. A documentação do projeto registra a intenção de adotar uma política mais restritiva em produção.

A afirmação de que não existem scripts inline deve ser sustentada pela inspeção dos templates e arquivos JavaScript. Além disso, se a aplicação realmente não necessita de scripts inline, a remoção de `'unsafe-inline'` é preferível a manter a permissão sem necessidade.

**Recomendação**

- Remover `'unsafe-inline'` de `script-src` sempre que possível;
- Hospedar os recursos necessários na própria origem;
- Se scripts inline forem indispensáveis, avaliar *nonces* criptograficamente aleatórios por resposta ou hashes CSP;
- Executar novamente o Passive Scan após as alterações.

#### Achado 03 — CSP: `style-src` com `unsafe-inline`

- **Severidade:** Medium
- **Confiança:** High
- **URL observada:** `/login`
- **Área:** Aplicação de estilos CSS

**Descrição**

A política CSP permite estilos inline por meio de `'unsafe-inline'` na diretiva `style-src`.

**Risco**

A permissão reduz o rigor da política CSP sobre a origem dos estilos e pode ampliar as possibilidades de exploração em cenários específicos de injeção de conteúdo.

**Tratamento e justificativa**

A configuração de desenvolvimento permite estilos inline para compatibilidade com a interface e com os recursos de documentação. O projeto prevê o endurecimento da política em produção.

A utilização de arquivos CSS externos deve ser confirmada pela inspeção dos templates e dos recursos estáticos. A ausência de estilos inline não elimina automaticamente todos os riscos relacionados a CSS, mas pode permitir uma política mais restritiva.

**Recomendação**

- Remover `'unsafe-inline'` de `style-src` quando não for necessário;
- Priorizar arquivos CSS externos;
- Avaliar hashes ou nonces quando houver necessidade legítima de estilos inline;
- Validar visualmente a aplicação após o endurecimento da CSP.

---

## 4. Achado informativo — JWT armazenado no localStorage

- **Severidade:** Informational
- **Área:** Gerenciamento de sessão e autenticação
- **Local observado:** `localStorage` do navegador, conforme alerta reportado

### 4.1 Descrição

O alerta indica que o token JWT de acesso é armazenado no `localStorage` do navegador.

Esse mecanismo permite que o JavaScript da aplicação leia o token. Consequentemente, caso exista uma vulnerabilidade XSS explorável na origem, um atacante poderá tentar acessar o token e utilizá-lo indevidamente.

### 4.2 Impacto potencial

O comprometimento do token pode permitir que um atacante realize requisições autenticadas em nome do usuário enquanto o token permanecer válido, respeitando as permissões associadas a ele.

O risco depende de fatores como duração do token, escopo das permissões, proteção contra XSS e mecanismos de revogação.

### 4.3 Tratamento atual

O uso de `localStorage` foi documentado como uma decisão da implementação acadêmica atual, e não como a opção preferencial para um ambiente bancário de produção.

A decisão não elimina o risco. Ela registra uma limitação conhecida que deve ser considerada na evolução da arquitetura.

### 4.4 Recomendação

Avaliar uma arquitetura de sessão baseada em cookies com os atributos:

- `HttpOnly`, para impedir o acesso direto ao cookie pelo JavaScript;
- `Secure`, para restringir o envio a conexões HTTPS;
- `SameSite`, com política adequada ao fluxo da aplicação.

A adoção de cookies exige também uma avaliação de proteção contra CSRF e de como os tokens serão gerados, renovados, expirados e invalidados. Cookies `HttpOnly` não eliminam o XSS nem todos os riscos de sequestro de sessão.

---

## 5. Configuração dos cabeçalhos HTTP de segurança

O middleware do FintechGuard configura cabeçalhos de segurança nas respostas da aplicação.

| Cabeçalho | Finalidade | Comportamento esperado |
|---|---|---|
| `X-Frame-Options` | Reduz o risco de clickjacking por enquadramento da página | Presente nas respostas |
| `X-Content-Type-Options` | Impede a interpretação de conteúdo com tipo diferente do declarado | Presente nas respostas |
| `Strict-Transport-Security` | Instrui o navegador a utilizar HTTPS para o domínio | Presente nas respostas HTTPS de produção |
| `Content-Security-Policy` | Restringe origens e tipos de recursos permitidos | Política ajustada ao ambiente |

O HSTS é condicionado à configuração `ENVIRONMENT == "production"`. Por isso, sua ausência em desenvolvimento local usando HTTP é esperada. Essa ausência, isoladamente, não comprova uma falha na configuração de produção.

Para demonstrar a configuração completa, os três cabeçalhos exigidos devem ser verificados simultaneamente no ambiente avaliado. Os testes automatizados devem ser complementados por evidência coletada em HTTPS no ambiente de produção, quando esse ambiente estiver disponível.

---

## 6. Testes automatizados e evidências reproduzíveis

Além do Passive Scan, o projeto dispõe de testes automatizados para validar comportamentos da API e cabeçalhos de segurança.

Os testes de headers devem comprovar os seguintes comportamentos:

| Cenário | Resultado esperado |
|---|---|
| Desenvolvimento | `X-Frame-Options` e `X-Content-Type-Options` presentes; HSTS ausente |
| Configuração de produção simulada | Os três cabeçalhos presentes na mesma resposta |
| Produção real via HTTPS | Os três cabeçalhos confirmados na resposta efetiva |

Os testes automatizados de produção simulada validam o comportamento do middleware, mas não comprovam que o servidor está acessível por HTTPS ou que a infraestrutura de produção preserva os cabeçalhos.

Para tornar a auditoria reproduzível, devem ser mantidos:

- O código dos testes;
- O resultado da execução do `pytest`;
- A configuração relevante do middleware;
- A evidência dos cabeçalhos na resposta HTTP;
- O relatório exportado pelo OWASP ZAP, quando disponível.

---

## 7. Plano de tratamento dos riscos

| Item | Ação | Critério de conclusão |
|---|---|---|
| CSP `form-action` | Confirmar a diretiva nas respostas | Cabeçalho validado e alerta reavaliado pelo ZAP |
| CSP `script-src` | Reduzir permissões desnecessárias | Política restritiva validada sem quebrar a interface |
| CSP `style-src` | Remover permissões inline desnecessárias | Política validada e interface funcional |
| JWT em `localStorage` | Avaliar migração para cookies seguros | Arquitetura documentada e controles de sessão testados |
| Cabeçalhos de segurança | Testar desenvolvimento e produção | Testes automatizados aprovados e evidência HTTPS coletada |

O estado de cada item deve ser atualizado com base nas evidências. Itens planejados não devem ser classificados como corrigidos.

---

## 8. Limitações da auditoria

Esta avaliação possui as seguintes limitações:

1. Foi realizada uma varredura passiva, sem Active Scan.
2. Os resultados dependem das requisições e respostas efetivamente capturadas.
3. A auditoria não demonstra, por si só, a ausência de vulnerabilidades.
4. As conclusões sobre produção dependem da validação do ambiente real, e não apenas da configuração local.
5. A classificação de severidade e confiança deve ser preservada conforme o relatório original do OWASP ZAP.
6. As correções precisam ser verificadas por meio de novos testes após sua implementação.

---

## 9. Conclusão

A análise passiva do FintechGuard identificou pontos de atenção relacionados à política CSP e ao armazenamento de tokens de autenticação. A inclusão de `form-action 'self'` representa uma medida de endurecimento da política de formulários, enquanto as permissões `unsafe-inline` e o uso de `localStorage` devem permanecer documentados como aspectos que exigem avaliação e, quando viável, mitigação.

A configuração dos cabeçalhos HTTP também deve ser validada em cada ambiente. Os testes automatizados confirmam o comportamento esperado do middleware, mas a comprovação da configuração de produção depende da verificação das respostas HTTPS reais.

Assim, o relatório registra os achados, suas implicações e as medidas de tratamento, mantendo a distinção entre correções verificadas, limitações conhecidas e melhorias futuras. A conclusão definitiva sobre o estado de segurança depende da execução dos testes de confirmação e da atualização dos resultados do OWASP ZAP.

---

**Projeto:** FintechGuard — Atendimento Bancário Seguro  
**Equipe:** Weslley Soares e Bruno Santos  
**Ferramenta de auditoria:** OWASP ZAP 2.17.0  
**Tipo de análise:** Passive Scan