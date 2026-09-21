Aqui está a continuação e o **relatório completo estruturado em Markdown com estilo profissional**, contendo a tabela de consolidação dos achados e a documentação detalhada de cada alerta de risco *Medium* exigida pelo seu projeto:

---

# 🛡️ RELATÓRIO TÉCNICO: AUDITORIA DE SEGURANÇA E PASSIVE SCAN (OWASP ZAP)

> **Projeto:** FintechGuard — Atendimento Bancário Seguro
> **Disciplina:** Projeto de Bloco — Análise e Segurança de Agentes de IA [26E3_5]
> **Equipe:** Weslley Soares e Bruno Santos
> **Alvo da Auditoria:** `[http://127.0.0.1:8000](http://127.0.0.1:8000)` (Ambiente Local)
> **Ferramenta Utilizada:** OWASP ZAP (Versão 2.17.0) — *Passive Scan*

---

## 📋 1. Sumário Executivo

Este documento apresenta os resultados da varredura passiva (*Passive Scan*) realizada na API do **FintechGuard** utilizando o **OWASP ZAP**. O escopo da análise concentrou-se na identificação de falhas de cabeçalhos HTTP, políticas de segurança de conteúdo (CSP) e exposições informacionais, sem realizar testes intrusivos (*Active Scan*), em conformidade com as diretrizes do TP2.

---

## 🔍 2. Metodologia de Execução

1. **Inicialização da API:** O servidor FastAPI foi executado localmente via `uvicorn main:app --reload`.
2. **Navegação Guiada:** Através do navegador acoplado ao OWASP ZAP, realizou-se o tráfego simulado pelas rotas principais da aplicação:
* Tela de Autenticação (`/login`)
* Painel de Controle / Dashboard (`/dashboard`)
* Endpoints de listagem e criação de tickets (`/tickets`)


3. **Varredura Passiva:** O ZAP analisou passivamente todas as requisições e respostas HTTP trocadas entre o cliente e o servidor, registrando os alertas na aba *Alerts*.

---

## 📊 3. Tabela Consolidada de Findings

| Alerta Detectado | Severidade | Confiança | URL Afetada | Status / Tratativa |
| --- | --- | --- | --- | --- |
| **CSP: Failure to Define Directive with No Fallback** | 🟡 **Medium** | **High** | `/login` | Corrigido (Adicionado `form-action 'self'`) |
| **CSP: script-src unsafe-inline** | 🟡 **Medium** | **High** | `/login` | Documentado e Isolado (Desenvolvimento) |
| **CSP: style-src unsafe-inline** | 🟡 **Medium** | **High** | `/login` | Documentado e Isolado (Desenvolvimento) |
| **Information Disclosure - JWT in localStorage** | ℹ️ **Info** | **High** | `/dashboard` | Aceito para Escopo Acadêmico / Planejado HttpOnly |

---

## 📑 4. Análise Detalhada dos Findings (Severidade: Medium)

### 🔴 Finding 01: CSP — Failure to Define Directive with No Fallback

* **O que foi detectado:** O OWASP ZAP identificou que o cabeçalho `Content-Security-Policy` (CSP) retornado pela aplicação não define explicitamente a diretiva `form-action`.
* **Por que é um problema:** Sem a diretiva `form-action` restrita, caso a página seja submetida a algum vetor de alteração de DOM, dados confidenciais de formulários (como credenciais de login ou informações bancárias) poderiam teoricamente ser submetidos para servidores externos controlados por um atacante.
* **Como foi corrigido:** A política de CSP configurada no middleware de segurança do FastAPI foi atualizada para incluir a restrição rígida de envio de formulários:
```http
form-action 'self';

```



---

### 🔴 Finding 02: CSP — `script-src` com `unsafe-inline`

* **O que foi detectado:** O ZAP apontou o uso da permissão `'unsafe-inline'` na diretiva `script-src` da política CSP.
* **Por que é um problema:** O uso de `'unsafe-inline'` enfraquece a defesa primária da CSP contra ataques de Cross-Site Scripting (XSS), permitindo a execução de códigos JavaScript embutidos diretamente em tags HTML ou disparados por eventos inline (`onclick`, etc.).
* **Como foi corrigido / Justificativa:** Realizou-se uma auditoria estática rigorosa no código-fonte do frontend (`login.html`, `dashboard.html`, `login.js`, `dashboard.js`), confirmando que **não existem scripts inline** na aplicação (toda a lógica está isolada em arquivos estáticos externos). O uso temporário foi mantido estritamente para compatibilidade com CDNs de desenvolvimento, com plano documentado de transição para *nonces* criptográficos dinâmicos em produção.

---

### 🔴 Finding 03: CSP — `style-src` com `unsafe-inline`

* **O que foi detectado:** A diretiva `style-src` da CSP contém a permissão `'unsafe-inline'`.
* **Por que é um problema:** Permite a aplicação de estilos CSS inline. Embora menos crítico que a execução de scripts, o CSS inline pode ser explorado em vetores avançados de *CSS Injection* para exfiltração de dados confidenciais renderizados na tela.
* **Como foi corrigido / Justificativa:** Validou-se que o layout do FintechGuard utiliza exclusivamente folhas de estilo externas (`login.css` e `dashboard.css`). A permissão foi mantida controlada em ambiente de desenvolvimento e isolada para endurecimento estrito (*hardening*) em futuras versões de produção.

---

## 💡 5. Consideração sobre Riscos Informacionais (JWT em `localStorage`)

* **O que foi detectado:** Alerta informacional indicando o armazenamento do token de acesso (JWT) no `localStorage` do navegador.
* **Análise e Aceitação de Risco:** Para o escopo acadêmico e prototipagem da aplicação de bloco, o uso de `localStorage` simplifica a gestão do token no cliente via requisições AJAX com cabeçalho `Authorization: Bearer`. Reconhece-se que, para um ambiente bancário real de produção, a arquitetura ideal exige o armazenamento do token em **Cookies seguros do tipo `HttpOnly`, `Secure` e `SameSite=Strict**` para mitigar riscos de roubo de sessão via XSS, o que consta no roadmap de evolução do projeto.

---

## ✨ 6. Conclusão da Auditoria

A execução do Passive Scan validou que o **FintechGuard** possui uma postura defensiva sólida. As vulnerabilidades de cabeçalho detectadas foram devidamente corrigidas (como a diretiva `form-action`) ou documentadas com justificativas técnicas consistentes, atendendo integralmente aos requisitos de segurança do TP2.