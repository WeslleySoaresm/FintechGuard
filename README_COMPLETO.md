# FintechGuard — Plataforma de Atendimento Bancário Inteligente e Seguro

<p align="center">
  <strong>Inteligência Artificial, Machine Learning e segurança no atendimento financeiro.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue?logo=python" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-API-009688?logo=fastapi" alt="FastAPI">
  <img src="https://img.shields.io/badge/Scikit--learn-Machine%20Learning-orange?logo=scikitlearn" alt="Scikit-learn">
  <img src="https://img.shields.io/badge/SQLModel-ORM-blue" alt="SQLModel">
  <img src="https://img.shields.io/badge/JWT-Authentication-black" alt="JWT">
  <img src="https://img.shields.io/badge/OWASP-Security-red" alt="OWASP">
</p>

<p align="center">
  <a href="#-visão-geral">Visão geral</a> •
  <a href="#-arquitetura">Arquitetura</a> •
  <a href="#-análise-de-dados">Análise de dados</a> •
  <a href="#-machine-learning">Machine Learning</a> •
  <a href="#-agente-de-ia">Agente de IA</a> •
  <a href="#-segurança">Segurança</a> •
  <a href="#-instalação">Instalação</a>
</p>

---

# 📚 Sumário — Acesso rápido

Clique em qualquer tópico para acessar diretamente a seção desejada.

| Seção | Conteúdo |
|---|---|
| [1. Visão geral](#-visão-geral) | Apresentação e propósito do projeto |
| [2. Objetivos](#-objetivos) | Objetivos gerais e específicos |
| [3. Tecnologias](#-tecnologias-utilizadas) | Linguagens, frameworks e ferramentas |
| [4. Arquitetura](#-arquitetura) | Organização e funcionamento do sistema |
| [5. Dataset](#-dataset) | Fonte e características dos dados |
| [6. TP1 — EDA inicial](#-tp1--análise-exploratória-inicial) | Exploração e hipóteses |
| [7. TP2 — EDA avançada](#-tp2--análise-exploratória-avançada) | Limpeza, gráficos e estatística |
| [8. Machine Learning](#-machine-learning) | Classificador de intenções |
| [9. Agente de IA](#-agente-de-ia) | Atendimento conversacional |
| [10. Backend e API](#-backend-e-api) | FastAPI, rotas e funcionalidades |
| [11. Banco de dados](#-banco-de-dados) | SQLModel, SQLite e Alembic |
| [12. Interface web](#-interface-web) | Templates, CSS e JavaScript |
| [13. Segurança](#-segurança) | Autenticação, autorização e controles |
| [14. OWASP ZAP](#-análise-de-segurança-com-owasp-zap) | Análise passiva e alertas |
| [15. Testes](#-testes-automatizados) | Pytest e evidências |
| [16. CI/CD](#-integração-contínua) | GitHub Actions |
| [17. Estrutura do projeto](#-estrutura-do-projeto) | Organização de diretórios |
| [18. Endpoints](#-endpoints-da-api) | Rotas e métodos HTTP |
| [19. Instalação](#-instalação) | Preparação do ambiente |
| [20. Execução](#-execução-do-projeto) | Inicialização da aplicação |
| [21. Treinamento](#-treinamento-do-classificador) | Execução do modelo |
| [22. Fluxo de atendimento](#-fluxo-de-atendimento) | Funcionamento ponta a ponta |
| [23. Limitações](#-limitações-conhecidas) | Pontos que exigem validação |
| [24. Próximas etapas](#-roadmap) | Evolução do projeto |
| [25. Evidências](#-documentação-e-evidências) | Relatórios e documentação |
| [26. Equipe](#-equipe) | Responsáveis pelo projeto |

---

# 📌 Visão geral

O **FintechGuard** é um projeto acadêmico de desenvolvimento de uma plataforma de atendimento bancário inteligente e seguro, utilizando conceitos de Engenharia de Software, Análise Exploratória de Dados, Machine Learning, Inteligência Artificial e Segurança da Informação.

A plataforma foi concebida para interpretar solicitações de clientes, identificar intenções, organizar chamados, manter históricos de conversas e encaminhar situações que necessitam de intervenção humana.

O sistema utiliza uma API desenvolvida com **FastAPI**, autenticação baseada em **JWT**, persistência de dados com **SQLModel**, classificação de intenções com **Scikit-learn** e um agente conversacional desenvolvido com o **OpenAI Agents SDK**.

O projeto também contempla práticas de desenvolvimento seguro, testes automatizados e análise de vulnerabilidades com **OWASP ZAP**.

## Contexto acadêmico

**Disciplina:** Projeto de Bloco — Análise e Segurança de Agentes de IA [26E3_5]

**Professor:** Ricardo Pires Mesquita

**Equipe:**
- Weslley Soares
- Bruno Santos

**Repositório:** [github.com/WeslleySoaresm/FintechGuard](https://github.com/WeslleySoaresm/FintechGuard)

> **Aviso:** o FintechGuard é um protótipo acadêmico. Não é uma instituição financeira, não movimenta dinheiro e não realiza transferências ou pagamentos reais.

---

# 🎯 Objetivos

## Objetivo geral

Desenvolver uma plataforma de atendimento financeiro capaz de interpretar solicitações dos usuários, classificar intenções e fornecer respostas contextualizadas por meio de Inteligência Artificial, mantendo controles de autenticação, autorização, privacidade e segurança.

## Objetivos específicos

- Explorar e compreender dados de atendimento ao cliente.
- Identificar padrões, distribuições e possíveis anomalias.
- Formular e testar hipóteses estatísticas.
- Desenvolver uma API REST utilizando FastAPI.
- Implementar autenticação e proteção de rotas com JWT.
- Organizar a persistência de dados com SQLModel e SQLite.
- Implementar operações de gerenciamento de tickets.
- Desenvolver um classificador de intenções com Machine Learning.
- Treinar e avaliar modelos com Scikit-learn.
- Integrar um agente conversacional com OpenAI Agents SDK.
- Implementar ferramentas para comunicação entre o agente e a API.
- Manter histórico de conversas.
- Identificar situações que necessitam de atendimento humano.
- Aplicar validação de entradas e controles de acesso.
- Executar testes automatizados.
- Avaliar a segurança da aplicação com OWASP ZAP.

---

# 🛠️ Tecnologias utilizadas

| Tecnologia | Finalidade |
|---|---|
| Python | Linguagem principal |
| FastAPI | Desenvolvimento da API REST |
| Uvicorn | Servidor ASGI |
| SQLModel | Modelagem e persistência |
| SQLite | Banco de dados de desenvolvimento |
| Alembic | Migrações do banco de dados |
| Pydantic | Validação e estruturação dos dados |
| JWT | Autenticação baseada em tokens |
| bcrypt | Hash de senhas |
| Redis | Suporte ao controle de tentativas de autenticação |
| Scikit-learn | Machine Learning |
| TF-IDF | Representação numérica dos textos |
| GridSearchCV | Busca de hiperparâmetros |
| Joblib | Serialização do modelo |
| OpenAI Agents SDK | Desenvolvimento do agente conversacional |
| Jinja2 | Renderização de páginas HTML |
| HTML5 | Estrutura da interface |
| CSS3 | Estilização |
| JavaScript | Interatividade |
| Pandas | Manipulação de dados |
| NumPy | Operações numéricas |
| Matplotlib | Visualização de dados |
| Seaborn | Gráficos estatísticos |
| SciPy | Testes estatísticos |
| Pytest | Testes automatizados |
| OWASP ZAP | Análise de segurança |
| Git e GitHub | Versionamento e colaboração |
| GitHub Actions | Integração contínua |

---

# 🏗️ Arquitetura

O FintechGuard foi organizado em componentes com responsabilidades distintas, permitindo separar a interface, a API, a autenticação, a classificação de intenções, o agente conversacional e a persistência dos dados.

## Visão geral da arquitetura

```text
                         USUÁRIO
                            |
                            v
                   INTERFACE WEB
                    HTML / CSS / JS
                            |
                            v
                       FASTAPI
                            |
             +--------------+--------------+
             |              |              |
             v              v              v
        AUTENTICAÇÃO     TICKETS       ATENDIMENTO
             |              |              |
             v              v              v
            JWT         SQLMODEL       ORQUESTRADOR
                                           |
                            +--------------+--------------+
                            |                             |
                            v                             v
                     CLASSIFICADOR                 REGRAS DE RISCO
                     SCIKIT-LEARN                          |
                            |                             |
                            +--------------+--------------+
                                           |
                                           v
                                    AGENTE DE IA
                                  OPENAI AGENTS SDK
                                           |
                                           v
                                  HISTÓRICO DE CONVERSAS
                                           |
                                           v
                                      SQLITE
```

## Componentes principais

**Interface web:** apresenta a experiência de atendimento e as páginas públicas do sistema.

**FastAPI:** recebe requisições, valida dados e coordena os serviços.

**Autenticação:** utiliza JWT para identificar usuários e proteger recursos privados.

**Gerenciamento de tickets:** organiza e disponibiliza operações relacionadas aos chamados.

**Classificador:** identifica a intenção das mensagens por meio de Machine Learning.

**Orquestrador:** organiza o fluxo de processamento, classificação e avaliação de risco.

**Agente conversacional:** interpreta o contexto e produz respostas utilizando o OpenAI Agents SDK.

**Banco de dados:** mantém usuários, tickets e informações relacionadas às conversas.

---

# 📊 Dataset

O projeto utiliza como referência o dataset **Customer Support Ticket Dataset**, disponibilizado no Kaggle.

**Fonte:** [Customer Support Ticket Dataset — Kaggle](https://www.kaggle.com/datasets/suraj520/customer-support-ticket-dataset)

**Licença informada nos documentos do projeto:** Apache 2.0. Recomenda-se conferir a licença e as condições de redistribuição diretamente na fonte original antes de publicar os dados.

## Informações presentes no dataset

Entre as variáveis utilizadas estão:

- Ticket ID.
- Customer Name.
- Customer Email.
- Customer Age.
- Customer Gender.
- Product Purchased.
- Date of Purchase.
- Ticket Type.
- Ticket Subject.
- Ticket Description.
- Ticket Status.
- Ticket Priority.
- Ticket Channel.
- First Response Time.
- Time to Resolution.
- Resolution.
- Customer Satisfaction Rating.

## Observação sobre as versões dos dados

Os documentos produzidos durante o desenvolvimento registram diferentes contagens de linhas e etapas de limpeza.

Para manter a rastreabilidade, este README apresenta separadamente os resultados documentados em cada etapa, sem tratar todas as contagens como se fossem da mesma versão do arquivo.

---

# 🔎 TP1 — Análise Exploratória Inicial

O primeiro trabalho prático teve como objetivo compreender a estrutura do dataset, identificar problemas de qualidade dos dados e formular hipóteses para análises posteriores.

## 1. Dimensões da base

Uma das versões iniciais documentadas apresentou:

| Informação | Quantidade |
|---|---:|
| Registros originais | 8.483 |
| Colunas | 17 |
| Registros duplicados identificados | 2 |

Os registros duplicados foram tratados durante a preparação da base.

## 2. Valores ausentes

Foram identificados valores ausentes principalmente nas seguintes variáveis:

| Variável | Valores ausentes |
|---|---:|
| Resolution | 5.702 |
| Time to Resolution | 5.702 |
| Customer Satisfaction Rating | 5.702 |
| First Response Time | 2.821 |

Os valores ausentes foram considerados durante a preparação dos dados. Não foram automaticamente classificados como erros, pois podem estar relacionados ao próprio fluxo de atendimento.

## 3. Distribuição dos tipos de chamados

Na versão de dados utilizada em uma das análises, foram registrados:

| Tipo de ticket | Quantidade |
|---|---:|
| Refund Request | 1.752 |
| Technical Issue | 1.750 |
| Cancellation Request | 1.695 |
| Product Inquiry | 1.641 |
| Billing Inquiry | 1.635 |

A distribuição mostra quantidades relativamente próximas entre as cinco categorias.

## 4. Hipóteses formuladas

A partir da análise inicial, foram propostas quatro hipóteses:

**Hipótese 1 — Distribuição dos tipos de chamados**

Os tipos de chamados apresentam uma distribuição relativamente equilibrada, sem uma categoria concentrando a maioria absoluta dos registros.

**Hipótese 2 — Demandas financeiras e cancelamentos**

Solicitações relacionadas a questões financeiras, reembolsos e cancelamentos podem representar uma parcela relevante dos atendimentos.

**Hipótese 3 — Canais e tipos de atendimento**

Os canais de atendimento podem apresentar diferenças na distribuição dos tipos de chamados.

**Hipótese 4 — Primeira resposta e satisfação**

Clientes associados a horários mais tardios de primeira resposta podem apresentar diferenças nos níveis de satisfação.

A quarta hipótese foi selecionada para aprofundamento estatístico no TP2.

## 5. Script de análise inicial

O script `scripts/eda.py` foi utilizado para:

1. Carregar o dataset.
2. Verificar dimensões e tipos de dados.
3. Identificar valores ausentes.
4. Identificar duplicatas.
5. Normalizar categorias.
6. Preparar os dados.
7. Gerar estatísticas descritivas.
8. Criar visualizações iniciais.
9. Salvar os resultados tratados.

---

# 🔬 TP2 — Análise Exploratória Avançada

O TP2 aprofundou a análise realizada anteriormente, incorporando tratamento de anomalias, visualizações estatísticas e teste formal de hipótese.

As principais atividades foram:

- Tratamento de dados inconsistentes.
- Identificação de anomalias estruturais.
- Estatísticas descritivas.
- Heatmap de correlação.
- Scatter plots.
- Conversão da variável de primeira resposta.
- Teste de Mann-Whitney U.
- Interpretação dos resultados.

## 1. Tratamento de anomalias

Durante a análise foram identificados:

- 8 tickets contendo conteúdo potencialmente suspeito.
- 7 registros classificados como anomalias estruturais e removidos da análise final.

Entre os conteúdos suspeitos havia entradas semelhantes a:

```html
<script>alert("ola mundo")</script>
```

Essas entradas foram classificadas como conteúdo potencialmente suspeito. A presença de um texto semelhante a um payload não comprova, isoladamente, que ocorreu um ataque ou que houve execução de código.

Também foram identificadas inconsistências estruturais, como:

- Idade igual a 120 anos.
- Campos textuais contendo literalmente `"string"`.
- Registros com características incompatíveis com a estrutura esperada.

Os registros identificados durante a auditoria foram preservados em:

```text
data/customer_support_tickets_anomalies.csv
```

## 2. Resultado da limpeza

Uma das etapas documentadas apresentou o seguinte fluxo:

| Etapa | Registros |
|---|---:|
| Dataset original | 8.483 |
| Após remoção de linhas vazias e duplicados | 8.480 |
| Após remoção de anomalias estruturais | 8.473 |
| Total utilizado na análise final | **8.473** |

Esses números representam a sequência de limpeza documentada para essa execução.

## 3. Estatísticas descritivas — Customer Age

| Estatística | Valor |
|---|---:|
| Média | 44,02 |
| Desvio padrão | 15,30 |
| Mínimo | 18 |
| Mediana | 44 |
| Máximo | 70 |

## 4. Estatísticas descritivas — Customer Satisfaction

| Estatística | Valor |
|---|---:|
| Média | 2,99 |
| Desvio padrão | 1,41 |
| Mínimo | 1 |
| Mediana | 3 |
| Máximo | 5 |

A média de satisfação ficou próxima de 3 em uma escala de 1 a 5.

## 5. Tratamento de First Response Time

Foi identificado que a variável `First Response Time` contém registros de data/hora, e não uma duração diretamente expressa em minutos.

Para realizar a análise, os horários foram convertidos em minutos desde meia-noite.

**Valores válidos convertidos:** 5.650.

### Limitação metodológica

Essa transformação representa o horário em que ocorreu a primeira resposta, não o tempo efetivamente decorrido entre a abertura do chamado e a resposta.

Portanto, a análise investiga a relação entre **horário da primeira resposta** e satisfação. Ela não demonstra diretamente que um maior tempo de espera causa menor satisfação.

---

# 📈 Visualizações e análise estatística

## 1. Heatmap de correlação

Foi utilizado Seaborn para investigar relações lineares entre:

- Customer Age.
- First Response Minutes.
- Customer Satisfaction Rating.

Resultados documentados:

| Variáveis | Correlação |
|---|---:|
| Customer Age × First Response Minutes | 0,015 |
| Customer Age × Satisfaction | -0,005 |
| First Response Minutes × Satisfaction | **-0,040** |

Arquivo:

```text
graphs/heatmap_correlacao.png
```

### Interpretação

A correlação entre o horário da primeira resposta e a satisfação foi de -0,040, um valor muito próximo de zero.

Na base analisada, não foi observada uma associação linear relevante entre essas variáveis.

A correlação entre idade e satisfação também foi praticamente nula, com valor de -0,005.

Uma correlação próxima de zero não exclui todos os tipos de relação entre variáveis. Ela indica apenas que não foi identificada uma associação linear relevante por essa medida.

## 2. Scatter Plot — Primeira resposta × satisfação

Arquivo:

```text
graphs/scatter_resposta_satisfacao.png
```

O gráfico permite observar a distribuição dos registros e investigar visualmente possíveis tendências entre o horário da primeira resposta e a satisfação.

## 3. Scatter Plot — Idade × satisfação

Arquivo:

```text
graphs/scatter_idade_satisfacao.png
```

O gráfico apresenta a distribuição das avaliações de satisfação em relação à idade dos clientes.

O coeficiente de correlação registrado foi -0,005.

## 4. Boxplot — Primeira resposta × satisfação

Arquivo:

```text
graphs/boxplot_resposta_satisfacao.png
```

O boxplot foi utilizado para comparar a distribuição da satisfação entre dois grupos de horários de primeira resposta.

A visualização permite observar:

- Mediana.
- Quartis.
- Dispersão.
- Possíveis valores extremos.
- Diferenças entre as distribuições.

## 5. Teste de hipótese — Mann-Whitney U

Para aprofundar a quarta hipótese formulada no TP1, foi utilizado o teste estatístico de Mann-Whitney U, disponibilizado pela biblioteca SciPy.

### Hipótese investigada

Verificar se as distribuições de satisfação diferem entre clientes associados a horários de primeira resposta mais cedo e mais tarde.

### Hipótese nula — H0

As distribuições de satisfação dos dois grupos não apresentam diferença estatisticamente significativa.

### Hipótese alternativa — H1

As distribuições de satisfação dos dois grupos apresentam diferença estatisticamente significativa.

### Nível de significância

```text
α = 0,05
```

### Formação dos grupos

A mediana do horário da primeira resposta foi:

```text
710,20 minutos
```

Os grupos documentados foram:

| Grupo | Quantidade |
|---|---:|
| Primeira resposta mais cedo | 1.385 |
| Primeira resposta mais tarde | 1.384 |

Medianas de satisfação:

| Grupo | Mediana |
|---|---:|
| Mais cedo | 3,00 |
| Mais tarde | 3,00 |

### Resultado do teste

| Estatística | Valor |
|---|---:|
| U | 994.174,50 |
| p-value | **0,082766** |
| α | 0,05 |

Como o p-value é maior que o nível de significância adotado, não há evidência estatística suficiente para rejeitar H0.

### Interpretação

O teste não encontrou evidência estatística suficiente, ao nível de 5%, para afirmar que os dois grupos apresentam distribuições de satisfação diferentes.

Isso não comprova que o horário da primeira resposta não tenha qualquer relação com a satisfação.

A conclusão deve ser interpretada considerando a natureza da variável e a forma como os grupos foram construídos.

**Resultado do TP2:** não foi encontrada evidência estatística suficiente de diferença na distribuição da satisfação entre os grupos analisados.

## 6. Arquivos de visualização

| Arquivo | Descrição |
|---|---|
| `graphs/eda_visualizations.png` | Visualizações gerais da EDA |
| `graphs/heatmap_correlacao.png` | Matriz de correlação |
| `graphs/scatter_resposta_satisfacao.png` | Horário da primeira resposta × satisfação |
| `graphs/scatter_idade_satisfacao.png` | Idade × satisfação |
| `graphs/boxplot_resposta_satisfacao.png` | Comparação entre grupos |

---

# 🤖 Machine Learning

O FintechGuard possui um classificador de intenções desenvolvido com Scikit-learn.

O objetivo é identificar o assunto principal de uma mensagem e disponibilizar essa informação para o fluxo de atendimento.

## 1. Classes de classificação

O modelo trabalha com cinco categorias:

| Classe | Descrição |
|---|---|
| Billing Inquiry | Dúvidas sobre cobranças e tarifas |
| Cancellation Request | Solicitações de cancelamento |
| Product Inquiry | Dúvidas sobre produtos e serviços |
| Refund Request | Solicitações de reembolso |
| Technical Issue | Problemas técnicos |

## 2. Processamento de texto com TF-IDF

O TF-IDF transforma os textos em representações numéricas, permitindo que o algoritmo identifique padrões relevantes nas palavras e expressões das mensagens.

Essa representação é utilizada pelo classificador para prever a categoria mais provável.

## 3. Treinamento e busca de hiperparâmetros

O projeto utiliza `GridSearchCV` para avaliar diferentes configurações do modelo.

Entre os parâmetros avaliados estão:

- `C`
- `class_weight`
- `ngram_range`

A configuração registrada como melhor resultado foi:

```python
{
    "C": 10,
    "class_weight": None,
    "ngram_range": (1, 2)
}
```

## 4. Resultados experimentais

Na execução documentada:

| Métrica | Resultado |
|---|---:|
| Amostras de treinamento | 3.933 |
| Combinações avaliadas | 18 |
| Ajustes na validação cruzada | 90 fits |
| F1 Macro médio na validação cruzada | 0,9995 |
| Accuracy na validação | 1,0000 |
| Precision Macro na validação | 1,0000 |
| Recall Macro na validação | 1,0000 |
| F1 Macro na validação | 1,0000 |

A matriz de confusão registrada apresentou valores na diagonal principal naquela execução.

### Limitação dos resultados

As métricas representam uma avaliação experimental com os dados preparados para o projeto.

Parte dos exemplos foi aumentada sinteticamente. Por isso, ainda é necessário avaliar o modelo com mensagens independentes, reais e representativas de clientes.

Resultados perfeitos em uma validação experimental não garantem o mesmo desempenho em produção. Também é necessário investigar possíveis similaridades e vazamento de informação entre os conjuntos de treinamento e validação.

## 5. Arquivos do classificador

```text
fintechguard_agents/
├── intent_classifier.joblib
├── intent_classifier_backup.joblib
├── intent_classifier_v2.joblib
├── predict_intent.py
└── grid_search_intent_classifier.py
```

Arquivos de dados utilizados:

```text
data/
├── fintechguard_train_augmented.csv
└── fintechguard_validation.csv
```

---

# 🧠 Agente de IA

O projeto integra um agente conversacional desenvolvido com o **OpenAI Agents SDK**.

O agente foi concebido para interpretar solicitações de atendimento, utilizar o contexto das conversas e consultar ferramentas disponibilizadas pelo sistema.

## 1. Componentes utilizados

Entre os componentes documentados estão:

- `Agent`
- `Runner.run`
- `@function_tool`

O agente utiliza orientações específicas para o contexto de atendimento financeiro.

## 2. Classificação integrada ao agente

O agente pode utilizar uma ferramenta para consultar a classificação de intenção.

Essa integração permite que o fluxo de atendimento utilize informações do classificador para orientar o tratamento da solicitação.

## 3. Orquestração

O orquestrador organiza o processamento das mensagens considerando:

- Intenção identificada.
- Contexto da conversa.
- Nível de risco.
- Necessidade de atendimento humano.
- Ação recomendada.
- Prioridade da solicitação.

A separação entre classificação, regras de risco e geração de respostas facilita a manutenção e a evolução do sistema.

## 4. Proteção de informações sensíveis

O agente deve evitar solicitar ou expor informações confidenciais desnecessárias, como:

- Senhas.
- CVV.
- Códigos de autenticação enviados por SMS.
- Tokens de autenticação.
- Número completo de cartões.
- Credenciais bancárias.

Solicitações sensíveis devem ser tratadas com cautela e encaminhadas para atendimento humano quando necessário.

## 5. Arquivos relacionados

```text
fintechguard_agents/
├── classifier_tool.py
├── customer_service_agent.py
├── orchestrator.py
├── response_generator.py
└── schemas.py
```

---

# ⚙️ Backend e API

O backend foi desenvolvido utilizando FastAPI, com separação entre rotas, esquemas de validação, autenticação e serviços.

## Funcionalidades documentadas

- Verificação de saúde da aplicação.
- Autenticação e emissão de JWT.
- Gerenciamento de tickets.
- Classificação de intenções.
- Atendimento com agente de IA.
- Consulta de conversas.
- Recuperação do histórico de mensagens.
- Validação dos dados recebidos.
- Paginação de consultas.
- Proteção de recursos por usuário.

---

# 🗄️ Banco de dados

O projeto utiliza SQLModel para modelar as entidades e interagir com o banco de dados.

O SQLite é utilizado no ambiente de desenvolvimento, enquanto Alembic organiza as alterações estruturais por meio de migrações.

## Entidades principais

### User

Representa os usuários do sistema.

Campos documentados incluem:

- `id`
- `name`
- `email`
- `password_hash`
- `role`
- `created_at`

### Ticket

Representa os chamados de atendimento.

Campos documentados incluem:

- `id`
- `user_id`
- `customer_name`
- `customer_email`
- `customer_age`
- `customer_gender`
- `product_purchased`
- `date_of_purchase`
- `ticket_type`
- `subject`
- `description`
- `status`
- `priority`
- `channel`
- `first_response_time`
- `time_to_resolution`
- `resolution`
- `customer_satisfaction_rating`
- `created_at`

### ConversationMessage

Representa as mensagens registradas em uma conversa.

Campos documentados incluem:

- `id`
- `ticket_id`
- `sender_type`
- `message`
- `created_at`

## Relacionamentos

```text
USER
 |
 | 1:N
 |
TICKET
 |
 | 1:N
 |
CONVERSATION MESSAGE
```

O relacionamento entre usuários e tickets permite associar os recursos ao respectivo proprietário.

O relacionamento entre tickets e mensagens permite organizar o histórico de atendimento associado aos chamados, quando aplicável.

> A implementação passou por evolução de identificadores e migrações. O esquema efetivamente utilizado deve ser conferido nos modelos e nas migrations atuais antes de executar alterações manuais no banco.

---

# 🌐 Interface web

A interface utiliza HTML, CSS, JavaScript e templates Jinja2.

## Recursos da interface

- Página inicial.
- Identidade visual do FintechGuard.
- Navegação institucional.
- Indicador de ambiente protegido.
- Acesso à área de login.
- Apresentação do assistente virtual.
- Área de mensagens.
- Sugestões de perguntas.
- Campo para envio de mensagens.
- Aviso sobre informações confidenciais.
- Apresentação dos serviços.
- Páginas de privacidade e segurança.

## Estrutura documentada

```text
templates/
├── home.html
├── login.html
└── agent.html

static/
├── css/
│   └── public.css
└── js/
    └── public.js
```

**Observação:** a interface pública e as rotas privadas de atendimento são componentes distintos. A integração completa do chat com a autenticação do navegador deve ser validada de acordo com a implementação atual.

---

# 🔐 Segurança

A segurança é um dos principais objetivos do FintechGuard.

O projeto considera práticas de desenvolvimento seguro e controles relacionados às recomendações do OWASP.

## 1. Autenticação JWT

A autenticação utiliza JSON Web Token para identificar os usuários e proteger rotas privadas.

Os controles documentados incluem:

- Emissão de token de acesso.
- Verificação de tokens.
- Rejeição de tokens inválidos.
- Proteção de rotas por dependências do FastAPI.
- Identificação do usuário autenticado.

## 2. Hash de senhas

O projeto utiliza bcrypt para proteger senhas armazenadas, evitando manter senhas em texto puro no banco de dados.

## 3. Validação de entradas

Pydantic é utilizado para validar os dados recebidos pela API.

Entre os controles considerados estão:

- Validação de tipos.
- Limites de campos.
- Campos obrigatórios.
- Sanitização de entradas textuais.
- Restrição de campos adicionais quando configurada nos modelos.

Uma configuração utilizada nos modelos Pydantic é:

```python
model_config = ConfigDict(extra="forbid")
```

Essa configuração permite rejeitar campos adicionais não definidos no modelo.

## 4. Autorização e proteção contra BOLA

As consultas de recursos privados devem verificar se o recurso pertence ao usuário autenticado.

Exemplo conceitual:

```python
statement = select(Ticket).where(
    Ticket.id == ticket_id,
    Ticket.user_id == current_user.id
)
```

A consulta restringe o acesso ao ticket pelo identificador e pelo usuário proprietário.

O comportamento esperado para um recurso inexistente ou não pertencente ao usuário é impedir o acesso, conforme a política da API.

Esse controle ajuda a reduzir riscos de BOLA/IDOR.

## 5. Consultas parametrizadas

O acesso ao banco utiliza SQLModel/SQLAlchemy para estruturar consultas, evitando montar comandos SQL por concatenação de entradas fornecidas pelo usuário.

## 6. Cabeçalhos HTTP

Foram implementados testes automatizados para verificar cabeçalhos de segurança.

| Cabeçalho | Finalidade |
|---|---|
| `X-Frame-Options` | Reduzir riscos de clickjacking |
| `X-Content-Type-Options` | Evitar interpretação incorreta de tipos MIME |
| `Strict-Transport-Security` | Orientar navegadores a utilizar HTTPS |
| `Content-Security-Policy` | Restringir fontes de conteúdo da aplicação |

Valores documentados nos testes:

```text
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
Strict-Transport-Security: max-age=31536000; includeSubDomains
```

O HSTS deve ser validado por HTTPS no ambiente real. Um teste de configuração simulada não substitui essa verificação.

## 7. Content Security Policy

A política CSP foi avaliada durante a análise de segurança.

Uma política de produção planejada e mais restritiva foi documentada como:

```text
default-src 'self';
script-src 'self';
style-src 'self';
img-src 'self' data:;
font-src 'self';
connect-src 'self';
frame-ancestors 'none';
```

A política efetivamente aplicada deve ser conferida nas respostas HTTP da aplicação.

## 8. CORS

O projeto documenta o uso de uma lista de origens permitidas para o frontend, incluindo:

```text
http://localhost:3000
http://localhost:5173
```

Não se deve utilizar uma política irrestrita com `*` quando houver credenciais.

## 9. Rate limiting

Foi implementado um mecanismo de limitação de tentativas de autenticação com suporte ao Redis.

Uma configuração documentada posteriormente utiliza:

```text
MAX_ATTEMPTS=5
BLOCK_DURATION_SECONDS=60
```

A implementação deve ser validada quanto à resposta HTTP `429` e ao comportamento quando o Redis estiver indisponível.

Documentos de versões anteriores mencionam configurações diferentes. Por isso, os valores acima devem ser confirmados no código atual.

## 10. Gerenciamento de segredos

As configurações sensíveis devem ser mantidas em variáveis de ambiente.

O arquivo `.env` não deve ser versionado.

Recomenda-se manter um `.env.example` com nomes de variáveis e valores fictícios.

Nunca publicar chaves de API, senhas ou tokens no GitHub.

---

# 🛡️ Análise de segurança com OWASP ZAP

Foi utilizada a ferramenta **OWASP ZAP 2.17.0** para realizar análise passiva da aplicação.

O alvo documentado foi:

```text
http://127.0.0.1:8000
```

A análise passiva observa informações das requisições e respostas sem executar, por si só, um teste ofensivo ativo contra os endpoints.

## Alertas identificados anteriormente

| Alerta | Observação | Tratamento necessário |
|---|---|---|
| CSP sem `form-action` | Diretiva ausente na política observada | Incluir e revalidar |
| `script-src 'unsafe-inline'` | Permite scripts inline | Avaliar remoção ou alternativa segura |
| `style-src 'unsafe-inline'` | Permite estilos inline | Avaliar remoção ou alternativa segura |
| JWT em `localStorage` | Scripts da mesma origem podem acessar o token | Revisar estratégia de armazenamento |

Um alerta externo relacionado a `archive.mozilla.org` também foi observado em documentação anterior. Ele não deve ser atribuído automaticamente à aplicação FintechGuard, pois é necessário confirmar se o recurso está dentro do escopo avaliado.

## Situação da auditoria

Os resultados disponíveis indicam que alguns controles foram testados, mas não comprovam o fechamento de todas as pendências.

O relatório de auditoria documenta os seguintes pontos:

- Cabeçalhos `X-Frame-Options` e `X-Content-Type-Options`: aprovados nos testes compartilhados.
- HSTS: aprovado em configuração simulada; falta validação HTTPS no ambiente real.
- CSP: necessita revalidação.
- Armazenamento de JWT: risco documentado, com aceitação formal ainda pendente.
- Autenticação JWT: validação parcial.
- BOLA: falta evidência final com usuários distintos.
- Rate limiting: falta comprovar o comportamento de `429` e a falha do Redis.
- Segredos e logs: revisão final necessária.
- OWASP ZAP: nova varredura necessária após as correções.
- Ambiente de pentest: isolamento e autorização ainda precisam ser confirmados.

## Critério de prontidão

A classificação registrada na auditoria é:

**Prontidão condicionada à conclusão e comprovação dos itens pendentes.**

O projeto não deve ser declarado aprovado para produção ou pentest definitivo sem a validação dos controles necessários e a autorização do responsável pelo ambiente.

---

# 🧪 Testes automatizados

O projeto utiliza Pytest para executar testes automatizados.

## Execução dos testes

```bash
pytest -v
```

Para executar os testes de cabeçalhos:

```bash
pytest tests/test_security_headers.py -v
```

## Resultado compartilhado

```text
tests/test_security.py::test_headers_em_desenvolvimento PASSED
tests/test_security.py::test_tres_headers_em_producao PASSED
```

Os resultados demonstram aprovação dos testes executados naquela ocasião.

## Cenários importantes para a suíte

| Cenário | Resultado esperado |
|---|---|
| Requisição protegida sem token | 401 |
| Token inválido ou expirado | 401 |
| Token válido | Acesso conforme permissões |
| Acesso a ticket de outro usuário | Bloqueio |
| Campo adicional não permitido | 422 |
| Dados inválidos | 422, quando aplicável |
| Excesso de tentativas de autenticação | 429 |
| Consulta de conversa de outro usuário | Bloqueio |
| Histórico de conversas | Apenas dados autorizados |
| Situação de risco | Encaminhamento conforme regras |

A existência de testes individuais aprovados não equivale a uma certificação de segurança.

---

# 🔄 Integração contínua

O projeto possui documentação de integração contínua com GitHub Actions.

O workflow documentado está em:

```text
.github/workflows/security-tests.yml
```

O objetivo é executar testes automatizados em eventos de push e pull request.

## Evidências documentadas

Foram registradas execuções bem-sucedidas:

- [GitHub Actions — Execução 1](https://github.com/WeslleySoaresm/FintechGuard/actions/runs/40117059228)
- [GitHub Actions — Execução 2](https://github.com/WeslleySoaresm/FintechGuard/actions/runs/40117061770)
- [GitHub Actions — Execução 3](https://github.com/WeslleySoaresm/FintechGuard/actions/runs/40117206491)

Pull request documentado:

[Pull Request #17](https://github.com/WeslleySoaresm/FintechGuard/pull/17)

Esses links representam evidências históricas de execução. O estado atual do workflow deve ser consultado diretamente no GitHub.

---

# 📁 Estrutura do projeto

A organização geral documentada contempla os seguintes componentes:

```text
FintechGuard/
│
├── data/
│   ├── db.py
│   ├── customer_support_tickets.csv
│   ├── customer_support_tickets_anomalies.csv
│   ├── fintechguard_train_augmented.csv
│   └── fintechguard_validation.csv
│
├── graphs/
│   ├── eda_visualizations.png
│   ├── heatmap_correlacao.png
│   ├── scatter_resposta_satisfacao.png
│   ├── scatter_idade_satisfacao.png
│   └── boxplot_resposta_satisfacao.png
│
├── scripts/
│   ├── eda.py
│   └── ...
│
├── fintechguard_agents/
│   ├── classifier_tool.py
│   ├── customer_service_agent.py
│   ├── grid_search_intent_classifier.py
│   ├── orchestrator.py
│   ├── predict_intent.py
│   ├── response_generator.py
│   ├── schemas.py
│   ├── intent_classifier.joblib
│   ├── intent_classifier_backup.joblib
│   └── intent_classifier_v2.joblib
│
├── models/
│   └── model_events.py
│
├── router/
│   ├── auth_router.py
│   ├── ticket_router.py
│   ├── agent_router.py
│   ├── public_router.py
│   └── ...
│
├── schemas/
│   └── auth.py
│
├── static/
│   ├── css/
│   │   └── public.css
│   └── js/
│       └── public.js
│
├── templates/
│   ├── home.html
│   ├── login.html
│   ├── dashboard.html
│   ├── agent.html
│   ├── privacy.html
│   ├── security.html
│   └── services.html
│
├── tests/
│   ├── test_security_headers.py
│   └── ...
│
├── utils/
│   └── auth.py
│
├── alembic/
│   └── ...
│
├── docs/
│   ├── owasp_zap_report.md
│   ├── tp3_formalizacao_classificacao.md
│   └── relatorio_auditoria_final.md
│
├── .github/
│   └── workflows/
│       └── security-tests.yml
│
├── main.py
├── alembic.ini
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

> A árvore representa uma organização consolidada dos componentes documentados ao longo das etapas. Os diretórios e arquivos exatos podem variar conforme a versão atual do repositório.

---

# 🔌 Endpoints da API

A tabela abaixo reúne as rotas documentadas durante o desenvolvimento.

| Método | Endpoint | Finalidade |
|---|---|---|
| GET | `/health` | Verificar a saúde da aplicação |
| POST | `/auth/token` | Autenticação e emissão de JWT |
| GET | `/tickets` | Consultar tickets |
| POST | `/tickets` | Criar ticket |
| GET | `/tickets/{ticket_id}` | Consultar ticket por identificador |
| DELETE | `/tickets/{ticket_id}` | Excluir ticket |
| POST | `/classify/` | Classificar intenção da mensagem |
| GET | `/agent` | Renderizar a interface do agente |
| POST | `/agent` | Enviar mensagem ao agente |
| GET | `/agent/conversations` | Listar conversas do usuário |
| GET | `/agent/conversations/{conversation_id}` | Consultar histórico de uma conversa |

**Importante:** confirme os métodos, prefixos e caminhos na documentação interativa em `/docs`. Os caminhos podem ter sido alterados durante a evolução do projeto.

---

# 💻 Instalação

## 1. Pré-requisitos

Antes de iniciar, tenha instalado:

- Python 3.x compatível com as dependências.
- Git.
- Pip.
- Ambiente virtual Python.
- Chave de API da OpenAI para utilizar o agente.
- Redis, caso a configuração de rate limiting utilizada dependa desse serviço.

## 2. Clonar o repositório

```bash
git clone https://github.com/WeslleySoaresm/FintechGuard.git
```

Entrar na pasta:

```bash
cd FintechGuard
```

## 3. Criar ambiente virtual

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

## 4. Instalar dependências

```bash
pip install -r requirements.txt
```

Se o arquivo `requirements.txt` não estiver atualizado, revise as dependências com base nos imports e nas versões efetivamente utilizadas pelo projeto.

## 5. Configurar variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto.

Exemplo ilustrativo:

```env
SECRET_KEY=SUBSTITUA_POR_UMA_CHAVE_FORTE
OPENAI_API_KEY=SUBSTITUA_PELA_SUA_CHAVE
DATABASE_URL=sqlite:///./fintechguard.db
```

Os nomes das variáveis devem corresponder aos utilizados nos arquivos de configuração da versão atual.

**Nunca publique o `.env` no GitHub.** Mantenha o arquivo no `.gitignore` e utilize `.env.example` com valores fictícios para documentar as configurações necessárias.

---

# 🚀 Execução do projeto

## 1. Executar migrações

Caso o banco esteja configurado com Alembic:

```bash
alembic upgrade head
```

## 2. Iniciar Redis

Se a configuração atual utilizar Redis, inicie o serviço antes de executar a API.

Em instalações que utilizam Docker Compose:

```bash
docker compose up -d redis
```

## 3. Iniciar a API

```bash
uvicorn main:app --reload
```

## 4. Acessar a aplicação

| Recurso | Endereço |
|---|---|
| Aplicação | http://127.0.0.1:8000 |
| Login | http://127.0.0.1:8000/login |
| Documentação Swagger | http://127.0.0.1:8000/docs |
| Documentação ReDoc | http://127.0.0.1:8000/redoc |
| Health check | http://127.0.0.1:8000/health |

---

# 🧠 Treinamento do classificador

O treinamento do classificador é realizado separadamente da inicialização da API.

O projeto possui scripts para busca de hiperparâmetros e previsão de intenções.

Exemplo de execução:

```bash
python fintechguard_agents/grid_search_intent_classifier.py
```

Para utilizar o modelo treinado, a API deve carregar o arquivo `.joblib` correspondente à versão escolhida.

É importante manter consistência entre:

- Dataset de treinamento.
- Dataset de validação.
- Pipeline de pré-processamento.
- Vocabulário TF-IDF.
- Modelo classificador.
- Classes de saída.
- Versão do arquivo carregado pela API.

---

# 🔄 Fluxo de atendimento

O fluxo geral documentado para o FintechGuard é:

1. O usuário envia uma mensagem.
2. A API recebe e valida os dados.
3. O sistema identifica o usuário autenticado quando a rota exigir autenticação.
4. O orquestrador organiza o processamento da solicitação.
5. O classificador identifica a intenção.
6. As regras de risco avaliam a necessidade de atendimento humano.
7. Quando permitido, o agente interpreta o contexto da conversa.
8. O agente pode utilizar ferramentas integradas ao sistema.
9. A mensagem e a resposta podem ser registradas no histórico.
10. A API retorna o resultado ao usuário.

Quando uma solicitação exige intervenção humana, o sistema pode utilizar uma resposta de encaminhamento em vez de continuar o atendimento automatizado.

---

# ⚠️ Limitações conhecidas

O FintechGuard é um protótipo acadêmico em evolução. Algumas funcionalidades precisam de validação adicional antes de serem consideradas prontas para produção.

## Machine Learning

- Resultados experimentais ainda precisam ser avaliados com mensagens reais e independentes.
- É necessário investigar possíveis similaridades entre treinamento e validação.
- O desempenho em mensagens ambíguas ainda precisa ser avaliado.
- É necessário testar erros ortográficos e linguagem informal.
- É importante monitorar erros por classe.

## Agente de IA

- É necessário avaliar robustez contra prompt injection.
- As regras de encaminhamento humano precisam de testes específicos.
- A integração com serviços externos depende da disponibilidade e configuração das APIs.
- Respostas geradas não devem ser tratadas como decisões financeiras autorizadas.

## Interface

- A integração completa do chat público com a API precisa ser validada.
- A estratégia de autenticação do navegador precisa ser definida e testada.
- Estados de carregamento, erro e reconexão podem ser aprimorados.
- A recuperação do histórico deve ser validada pela interface.

## Segurança

- CSP precisa de revalidação.
- Armazenamento de JWT precisa de revisão.
- BOLA precisa de evidências finais com usuários distintos.
- Rate limiting precisa de validação de `429` e falha do Redis.
- Segredos e logs precisam de revisão final.
- Nova varredura OWASP ZAP precisa ser executada.
- Ambiente de pentest precisa de autorização e isolamento comprovados.

## Infraestrutura

- PostgreSQL pode ser avaliado como alternativa ao SQLite.
- É necessário preparar ambiente de homologação.
- Monitoramento e logs estruturados podem ser ampliados.
- Docker e Docker Compose podem ser utilizados para padronizar a execução.
- Backup e recuperação devem ser validados.

---

# 🗺️ Roadmap

As etapas abaixo representam oportunidades de evolução do projeto, não necessariamente funcionalidades já concluídas.

| Área | Próxima evolução |
|---|---|
| Backend | Revisar e completar os endpoints CRUD |
| Banco de dados | Avaliar migração para PostgreSQL |
| Machine Learning | Testar com dados reais e independentes |
| Agente de IA | Aprimorar regras de risco e encaminhamento humano |
| Interface | Finalizar integração do chat com a API |
| Segurança | Revalidar CSP e armazenamento de tokens |
| Testes | Ampliar cobertura de autenticação e autorização |
| OWASP | Executar nova varredura após as correções |
| Infraestrutura | Preparar homologação e recuperação |
| Documentação | Manter relatórios e evidências atualizados |

---

# 📄 Documentação e evidências

A documentação acadêmica e técnica deve ser mantida organizada no repositório.

Entre os materiais produzidos durante o desenvolvimento estão:

- Análise Exploratória de Dados.
- Estatísticas descritivas.
- Visualizações estatísticas.
- Teste de hipótese.
- Treinamento e avaliação do classificador.
- Busca de hiperparâmetros.
- Testes automatizados.
- Testes de cabeçalhos HTTP.
- Relatórios do OWASP ZAP.
- Relatório de auditoria de segurança.
- Documentação de formalização da classificação.
- Evidências de integração contínua.

Arquivos documentados:

```text
docs/
├── owasp_zap_report.md
├── tp3_formalizacao_classificacao.md
└── relatorio_auditoria_final.md
```

Outros documentos de apoio podem estar distribuídos em `scripts/`, `graphs/` e `tests/`.

---

# 🏦 Considerações sobre uso em produção

O FintechGuard não deve ser considerado pronto para uso bancário real apenas por possuir autenticação, classificação de intenções e um agente conversacional.

Uma implantação real exigiria, entre outros requisitos:

- Avaliação independente de segurança.
- Testes de invasão autorizados.
- Proteção adequada de dados pessoais e financeiros.
- Controles de auditoria.
- Gestão de identidade e acesso.
- Monitoramento contínuo.
- Tratamento de incidentes.
- Avaliação de riscos do uso de IA.
- Testes de robustez contra prompt injection.
- Validação de conformidade regulatória aplicável.
- Revisão da arquitetura e da infraestrutura.

A classificação de intenções e as respostas geradas por IA não substituem decisões financeiras ou validações realizadas por sistemas bancários autorizados.

---

# 👨‍💻 Equipe

## Weslley Soares

**Engenharia de Software**

Responsável por atividades de desenvolvimento e integração técnica do FintechGuard, com atuação nas seguintes áreas:

- **Arquitetura e backend:** planejamento da estrutura da aplicação e desenvolvimento da API REST utilizando FastAPI.
- **Banco de dados:** implementação da persistência de dados com SQLModel, SQLite e Alembic.
- **Inteligência Artificial:** integração do OpenAI Agents SDK e desenvolvimento do fluxo de atendimento conversacional.
- **Machine Learning:** desenvolvimento e integração do classificador de intenções com Scikit-learn e TF-IDF.
- **Segurança da aplicação:** implementação de autenticação JWT, controle de acesso, validação de entradas e outros mecanismos de proteção.
- **Testes e integração:** desenvolvimento de funcionalidades, testes da API, integração dos componentes e evolução técnica do sistema.
- **Versionamento:** organização do código-fonte e acompanhamento da evolução do projeto utilizando Git e GitHub.

## Bruno Santos

**Engenharia de Software**

Responsável por atividades de análise, documentação e avaliação de segurança, com atuação nas seguintes áreas:

- **Análise de dados:** desenvolvimento da Análise Exploratória de Dados (EDA), tratamento e interpretação dos dados, elaboração de gráficos e análises estatísticas.
- **Documentação técnica:** elaboração e organização da documentação acadêmica e técnica do FintechGuard.
- **Testes de segurança ofensiva:** participação nos ataques simulados contra outra equipe, dentro das atividades acadêmicas autorizadas, contribuindo para a identificação de vulnerabilidades e avaliação dos controles de segurança.
- **Revisão de código:** análise do código-fonte, identificação de possíveis problemas e contribuição para melhorias na qualidade e segurança da aplicação.
- **Colaboração técnica:** participação no desenvolvimento e na evolução das entregas do projeto.
- **Versionamento:** organização do código-fonte e acompanhamento da evolução do projeto utilizando Git e GitHub.
---

# 📜 Licença e fontes de dados

O FintechGuard foi desenvolvido para fins acadêmicos.

O dataset Customer Support Ticket Dataset foi utilizado como referência para as atividades de análise e desenvolvimento do classificador. A licença informada durante o desenvolvimento foi Apache 2.0. Consulte a página original do dataset e os termos aplicáveis antes de redistribuir os dados ou derivados.

As bibliotecas e ferramentas de terceiros permanecem sujeitas às respectivas licenças.

---

<p align="center">
  <strong>FintechGuard</strong><br>
  Tecnologia, inteligência e segurança no atendimento financeiro.
</p>

<p align="center">
  Projeto acadêmico — Engenharia de Software
</p>

<p align="center">
  Desenvolvido por Weslley Soares e Bruno Santos.
</p>
