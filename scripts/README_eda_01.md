# FintechGuard - Sistema de Atendimento com IA & API FastAPI

## Projeto de Bloco: Análise e Segurança de Agentes de IA — TP1 e TP2

---

## 📌 Sobre o Projeto

O **FintechGuard** é um projeto acadêmico voltado para a análise de dados, segurança e desenvolvimento de sistemas de atendimento utilizando conceitos relacionados à Inteligência Artificial.

O projeto utiliza uma base de dados de chamados de atendimento ao cliente para realizar uma **Análise Exploratória de Dados (EDA)**, buscando identificar padrões, distribuições, possíveis anomalias e relações entre as variáveis.

Além da análise dos dados, o projeto possui uma estrutura de API desenvolvida com **FastAPI**, incluindo mecanismos de autenticação e organização dos chamados.

O desenvolvimento foi dividido em duas etapas principais:

- **TP1 — Análise Exploratória Inicial e Formulação de Hipóteses**
- **TP2 — Aprofundamento da EDA, Visualizações e Teste de Hipótese**

---

# 🎯 Objetivos

O projeto tem como principais objetivos:

- Explorar e compreender uma base de dados de atendimento ao cliente.
- Identificar padrões e distribuições relevantes.
- Investigar possíveis anomalias nos registros.
- Formular hipóteses relacionadas ao comportamento dos dados.
- Utilizar visualizações para facilitar a interpretação dos resultados.
- Aplicar técnicas estatísticas para testar uma hipótese.
- Desenvolver uma estrutura de API utilizando FastAPI.
- Trabalhar conceitos de segurança e autenticação.
- Criar uma base para futuras funcionalidades envolvendo Inteligência Artificial e atendimento automatizado.

---

# 📊 Dataset

O projeto utiliza o dataset **Customer Support Tickets**, disponibilizado no Kaggle.

**Fonte:**
https://www.kaggle.com/datasets/suraj520/customer-support-tickets

**Licença:** Apache 2.0

O dataset original possui:

- **8.483 registros**
- **17 colunas**

Entre as principais informações disponíveis estão:

- ID do chamado
- Nome do cliente
- Idade do cliente
- Tipo de chamado
- Produto
- Canal
- Prioridade
- Status
- Tempo da primeira resposta
- Tempo para resolução
- Avaliação de satisfação

---

# 🔎 TP1 — Análise Exploratória Inicial

A primeira etapa do projeto teve como objetivo compreender a estrutura da base e identificar possíveis padrões que poderiam ser investigados posteriormente.

## 1. Dimensões da base

A base original possui:

| Informação | Quantidade |
| ---------- | ---------: |
| Linhas     |      8.483 |
| Colunas    |         17 |

---

## 2. Valores ausentes

Durante a análise inicial foram identificados valores ausentes principalmente nas seguintes variáveis:

| Variável                     | Valores ausentes |
| ---------------------------- | ---------------: |
| Resolution                   |            5.702 |
| Time to Resolution           |            5.702 |
| Customer Satisfaction Rating |            5.702 |
| First Response Time          |            2.821 |

Esses valores foram considerados durante o processo de preparação dos dados.

No contexto da análise, os valores ausentes foram tratados como parte da estrutura da própria base e não foram automaticamente considerados como erros.

---

## 3. Valores duplicados

Na análise inicial foram encontrados:

**2 registros duplicados.**

Durante a etapa de limpeza, os registros duplicados foram tratados antes da análise estatística final.

---

# 📋 Distribuição dos Tipos de Ticket

Após o processo de limpeza e tratamento das anomalias estruturais, foram utilizados **8.473 registros** na análise final.

A distribuição dos tipos de chamados ficou da seguinte forma:

| Tipo de Ticket       | Quantidade |
| -------------------- | ---------: |
| Refund request       |      1.752 |
| Technical issue      |      1.750 |
| Cancellation request |      1.695 |
| Product inquiry      |      1.641 |
| Billing inquiry      |      1.635 |

A distribuição mostra que os cinco tipos de chamados aparecem em quantidades relativamente próximas na base utilizada para a análise.

---

# 🧠 Hipóteses do TP1

A partir da análise exploratória inicial, foram formuladas as seguintes hipóteses:

### Hipótese 1 — Distribuição dos tipos de chamados

Os tipos de chamados apresentam uma distribuição relativamente equilibrada na base, sem uma categoria concentrando a maioria absoluta dos registros.

---

### Hipótese 2 — Foco em demandas financeiras e cancelamento

Demandas relacionadas a questões financeiras e cancelamentos podem representar uma parcela relevante dos atendimentos, indicando possíveis áreas importantes para análise e automação.

---

### Hipótese 3 — Relação entre canais e tipos de atendimento

Os canais de atendimento podem apresentar diferenças na distribuição dos tipos de chamados, indicando possíveis padrões de preferência ou comportamento dos clientes.

---

### Hipótese 4 — Relação entre Primeira Resposta e Satisfação

Clientes associados a valores mais altos de `First Response Time` podem apresentar menores níveis de satisfação, indicando que o momento da primeira resposta pode estar relacionado à experiência do cliente.

Essa quarta hipótese foi selecionada para aprofundamento estatístico no TP2.

---

# 🔬 TP2 — Aprofundamento da Análise Exploratória

O TP2 teve como objetivo aprofundar a análise realizada no TP1 por meio de:

- tratamento de anomalias;
- visualizações avançadas;
- heatmap de correlação;
- scatter plots;
- teste estatístico formal;
- interpretação dos resultados em linguagem acessível.

---

# 🧹 Tratamento e Identificação de Anomalias

Durante a análise foram identificados registros que apresentavam características potencialmente anômalas.

Foram encontrados:

- **8 tickets contendo conteúdo potencialmente suspeito**;
- **7 registros classificados como anomalias estruturais** e removidos da análise final.

Entre os conteúdos identificados havia registros com aparência de payload HTML/JavaScript, como entradas contendo estruturas semelhantes a:

`<script>alert("ola mundo")</script>`

Esses registros foram tratados como **conteúdo potencialmente suspeito**, não sendo classificados automaticamente como ataques confirmados.

Também foram identificados registros com características estruturais incompatíveis com o restante da base, como:

- idade igual a 120 anos;
- múltiplos campos textuais contendo literalmente o valor `"string"`.

Esses critérios foram utilizados para identificar registros estruturais/anômalos.

### Resultado da limpeza

| Etapa                                                    | Registros |
| -------------------------------------------------------- | --------: |
| Dataset original                                         |     8.483 |
| Após remoção de linhas completamente vazias e duplicados |     8.480 |
| Após remoção das anomalias estruturais                   |     8.473 |
| Total utilizado na análise final                         | **8.473** |

Os registros identificados durante a auditoria de anomalias também são preservados em:

`data/customer_support_tickets_anomalies.csv`

---

# 📈 Estatísticas Descritivas

Após a limpeza, algumas estatísticas importantes foram obtidas.

## Customer Age

| Estatística   | Valor |
| ------------- | ----: |
| Média         | 44,02 |
| Desvio padrão | 15,30 |
| Mínimo        |    18 |
| Mediana       |    44 |
| Máximo        |    70 |

---

## Customer Satisfaction Rating

| Estatística   | Valor |
| ------------- | ----: |
| Média         |  2,99 |
| Desvio padrão |  1,41 |
| Mínimo        |     1 |
| Mediana       |     3 |
| Máximo        |     5 |

A avaliação média de satisfação ficou próxima de **3 em uma escala de 1 a 5**.

---

# ⏱️ Tratamento do First Response Time

Um ponto importante identificado durante o aprofundamento da EDA foi a estrutura da variável `First Response Time`.

Os valores disponíveis nessa coluna são registros de data/hora, e não uma medida diretamente expressa como duração de espera.

Por isso, nesta análise foi utilizado o **horário da primeira resposta convertido para minutos desde meia-noite** como uma variável operacional para investigação estatística.

Foram convertidos:

**5.650 valores válidos.**

### ⚠️ Limitação metodológica

Essa transformação representa o **horário do evento**, e não o tempo efetivamente decorrido entre a abertura do chamado e a primeira resposta.

Portanto, os resultados desta análise devem ser interpretados como uma investigação sobre a relação entre o **horário da primeira resposta** e a satisfação, e não como uma demonstração direta de que o tempo de espera causou determinada avaliação.

---

# 🔥 Heatmap de Correlação

Foi criado um **heatmap de correlação utilizando Seaborn** para investigar relações lineares entre:

- Customer Age
- First Response Time
- Customer Satisfaction Rating

Os coeficientes encontrados foram:

| Variáveis                             | Correlação |
| ------------------------------------- | ---------: |
| Customer Age × First Response Minutes |      0,015 |
| Customer Age × Satisfaction           |     -0,005 |
| First Response Minutes × Satisfaction | **-0,040** |

O gráfico está disponível em:

`graphs/heatmap_correlacao.png`

---

# 📊 Interpretação do Heatmap

A correlação entre **First Response Minutes** e **Customer Satisfaction** foi de:

**-0,040**

Esse valor é muito próximo de zero.

Em termos simples, dentro dos dados analisados, **não foi observada uma relação linear relevante entre o horário da primeira resposta e a avaliação de satisfação**.

A correlação entre idade e satisfação também foi praticamente inexistente:

**-0,005**

Da mesma forma, a relação entre idade e horário da primeira resposta foi muito pequena:

**0,015**

É importante destacar que correlação próxima de zero não significa que uma variável necessariamente não tenha qualquer relação com outra. Significa que não foi observada uma associação linear relevante por meio dessa medida.

---

# 🔵 Scatter Plot — Primeira Resposta × Satisfação

Foi criado um scatter plot relacionando:

- `First Response Time`
- `Customer Satisfaction Rating`

Arquivo:

`graphs/scatter_resposta_satisfacao.png`

O gráfico permite visualizar individualmente a distribuição dos registros e verificar se existe alguma tendência visual entre o horário da primeira resposta e a satisfação.

A visualização acompanha o resultado observado na matriz de correlação, que apresentou uma associação linear muito próxima de zero.

---

# 🔵 Scatter Plot — Idade × Satisfação

Também foi criado um scatter plot relacionando:

- `Customer Age`
- `Customer Satisfaction Rating`

Arquivo:

`graphs/scatter_idade_satisfacao.png`

Esse gráfico apresenta visualmente a distribuição das avaliações de satisfação em relação à idade dos clientes.

O coeficiente de correlação encontrado foi:

**-0,005**

Indicando uma associação linear praticamente nula entre as duas variáveis na base analisada.

---

# 🧪 Teste de Hipótese Formal

Para aprofundar a **Hipótese 4 do TP1**, foi aplicado um teste estatístico formal utilizando o **Mann-Whitney U**, disponibilizado pela biblioteca SciPy.

## Hipótese investigada

> Clientes associados a valores mais altos de `First Response Time` podem apresentar menores níveis de satisfação.

Como a variável representa o horário da primeira resposta, a hipótese foi operacionalizada comparando clientes associados a horários de primeira resposta mais cedo e mais tarde.

---

## H0 — Hipótese nula

**H0:** As distribuições de satisfação dos dois grupos não apresentam diferença estatisticamente significativa.

---

## H1 — Hipótese alternativa

**H1:** As distribuições de satisfação dos dois grupos apresentam diferença estatisticamente significativa.

---

## Nível de significância

Foi adotado:

**α = 0,05**

---

# ⚙️ Formação dos grupos

A mediana do horário da primeira resposta foi:

**710,20 minutos**

Os registros foram divididos em dois grupos:

| Grupo                        | Quantidade |
| ---------------------------- | ---------: |
| Primeira resposta mais cedo  |      1.385 |
| Primeira resposta mais tarde |      1.384 |

As medianas de satisfação foram:

| Grupo      | Mediana da satisfação |
| ---------- | --------------------: |
| Mais cedo  |                  3,00 |
| Mais tarde |                  3,00 |

---

# 📐 Resultado do Teste de Mann-Whitney

Resultado obtido:

| Estatística |        Valor |
| ----------- | -----------: |
| U           |   994.174,50 |
| p-value     | **0,082766** |
| α           |         0,05 |

Como:

**p-value > α**

não há evidência estatística suficiente, ao nível de 5%, para rejeitar a hipótese nula.

---

# 🧠 Interpretação em Linguagem Acessível

O teste comparou dois grupos de clientes:

- aqueles associados a horários de primeira resposta mais cedo;
- aqueles associados a horários de primeira resposta mais tarde.

As medianas de satisfação dos dois grupos foram iguais:

**3,0**

Além disso, o teste estatístico apresentou:

**p = 0,082766**

Como esse valor é maior que 0,05, **não foi encontrada evidência estatística suficiente para afirmar que os dois grupos apresentam distribuições de satisfação diferentes ao nível de significância de 5%**.

Isso não significa que está comprovado que o horário da primeira resposta não tenha nenhuma relação com a satisfação.

Significa apenas que, **com os dados disponíveis e com a forma como a variável foi operacionalizada nesta análise, o teste não encontrou evidência estatística suficiente para rejeitar a hipótese nula**.

---

# 📦 Boxplot — Primeira Resposta × Satisfação

Para complementar o teste estatístico, foi criado um boxplot comparando a distribuição da satisfação entre os grupos de primeira resposta mais cedo e mais tarde.

Arquivo:

`graphs/boxplot_resposta_satisfacao.png`

O boxplot permite visualizar:

- mediana;
- dispersão;
- quartis;
- possíveis valores extremos;
- diferenças na distribuição entre os grupos.

---

# 📌 Conclusão do TP2

A análise aprofundada permitiu avaliar a hipótese relacionada à primeira resposta e à satisfação utilizando diferentes técnicas.

Os principais resultados foram:

### Correlação

A correlação entre `First Response Minutes` e `Customer Satisfaction Rating` foi:

**-0,040**

Esse valor representa uma associação linear muito próxima de zero.

### Teste estatístico

O teste de Mann-Whitney apresentou:

**p = 0,082766**

Com α = 0,05, não houve evidência estatística suficiente para rejeitar H0.

### Interpretação

Dentro das limitações da análise realizada, **não foi encontrada evidência estatística suficiente de diferença na distribuição da satisfação entre os grupos de horários de primeira resposta mais cedo e mais tarde**.

A análise também demonstra a importância de compreender corretamente as variáveis antes de aplicar um teste estatístico. Como `First Response Time` está armazenado como horário/data, ele não representa diretamente a duração do atendimento ou o tempo de espera do cliente.

---

# 📊 Visualizações Geradas

Durante a execução da EDA foram gerados os seguintes gráficos:

| Arquivo                                  | Descrição                                  |
| ---------------------------------------- | ------------------------------------------ |
| `graphs/eda_visualizations.png`          | Visualizações gerais da EDA                |
| `graphs/heatmap_correlacao.png`          | Heatmap das correlações                    |
| `graphs/scatter_resposta_satisfacao.png` | Primeira resposta × satisfação             |
| `graphs/scatter_idade_satisfacao.png`    | Idade × satisfação                         |
| `graphs/boxplot_resposta_satisfacao.png` | Comparação dos grupos de primeira resposta |

---

# 🛠️ Tecnologias Utilizadas

## Análise de Dados

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- SciPy

## Backend

- FastAPI
- Uvicorn
- Pydantic
- JWT

## Banco de Dados

- Estrutura preparada para integração com banco de dados.

## Segurança

- Autenticação baseada em JWT.
- Separação entre rotas de autenticação e rotas relacionadas aos tickets.

---

# 📁 Estrutura do Projeto

```text
FintechGuard/
│
├── data/
│   ├── customer_support_tickets.csv
│   └── customer_support_tickets_anomalies.csv
│
├── graphs/
│   ├── eda_visualizations.png
│   ├── heatmap_correlacao.png
│   ├── scatter_resposta_satisfacao.png
│   ├── scatter_idade_satisfacao.png
│   └── boxplot_resposta_satisfacao.png
│
├── scripts/
│   └── eda.py
│
├── router/
│   ├── auth_router.py
│   └── ticket_router.py
│
├── schemas/
│   └── auth.py
│
├── templates/
│   ├── dashboard.html
│   └── login.html
│
├── utils/
│   └── auth.py
│
├── main.py
├── README.md
└── requirements.txt
```

---

# 🚀 Como Executar o Projeto

## 1. Clonar o repositório

```bash
git clone https://github.com/WeslleySoaresm/FintechGuard.git
```

Entrar na pasta:

```bash
cd FintechGuard
```

---

# 🐍 2. Criar ambiente virtual

No Windows:

```powershell
python -m venv venv
```

Ativar o ambiente:

```powershell
.\venv\Scripts\Activate.ps1
```

Caso o PowerShell bloqueie a execução do ambiente virtual, pode ser necessário ajustar a política de execução do usuário.

---

# 📦 3. Instalar as dependências

```powershell
pip install -r requirements.txt
```

As principais bibliotecas utilizadas na etapa de EDA incluem:

```text
pandas
numpy
matplotlib
seaborn
scipy
```

---

# 📊 4. Executar a Análise Exploratória

O script da EDA está localizado em:

```text
scripts/eda.py
```

Para executar:

```powershell
python scripts/eda.py
```

A execução realiza:

1. carregamento do dataset;
2. análise das dimensões;
3. identificação de valores ausentes;
4. identificação de duplicados;
5. normalização de categorias;
6. identificação de possíveis anomalias;
7. remoção de anomalias estruturais;
8. geração de estatísticas descritivas;
9. tratamento do `First Response Time`;
10. geração do heatmap;
11. geração dos scatter plots;
12. aplicação do teste de Mann-Whitney;
13. geração do boxplot;
14. salvamento dos resultados na pasta `graphs/`.

---

# 🌐 5. Executar a API

Para iniciar a aplicação FastAPI:

```powershell
uvicorn main:app --reload
```

Depois, acesse:

### Login

```text
http://127.0.0.1:8000/login
```

### Documentação da API

```text
http://127.0.0.1:8000/docs
```

---

# 🔐 Segurança

O projeto também possui uma estrutura voltada para autenticação e segurança da API.

A autenticação utiliza **JWT (JSON Web Token)** para controlar o acesso às rotas protegidas.

A organização do projeto separa responsabilidades em diferentes módulos:

```text
router/
schemas/
utils/
main.py
```

Essa estrutura facilita a manutenção e evolução futura do sistema.

---

# 🤖 Próximas Evoluções

O FintechGuard possui espaço para evolução além da análise exploratória atual.

Possíveis próximos passos incluem:

- integração com banco de dados;
- persistência dos tickets;
- criação de endpoints completos de CRUD;
- autenticação e autorização por níveis de acesso;
- integração com modelos de Inteligência Artificial;
- criação de um agente de atendimento;
- classificação automática dos chamados;
- detecção de conteúdos potencialmente suspeitos;
- análise automática de satisfação;
- criação de dashboards;
- monitoramento de métricas;
- implementação de mecanismos adicionais de segurança;
- integração entre a análise estatística e o sistema de atendimento.

---

# 📚 Resultados dos Trabalhos Práticos

## TP1

O TP1 concentrou-se na:

- compreensão do dataset;
- análise das dimensões;
- identificação de valores ausentes;
- identificação de duplicados;
- análise das categorias;
- formulação de hipóteses.

## TP2

O TP2 aprofundou a análise por meio de:

- tratamento de anomalias;
- heatmap de correlação;
- scatter plots;
- teste estatístico formal;
- interpretação dos resultados;
- documentação das limitações metodológicas.

---

# 📌 Principais Resultados do TP2

```text
Dataset original: 8.483 registros

Dataset utilizado na análise: 8.473 registros

Valores de First Response Time convertidos:
5.650

Correlação:
First Response Minutes × Satisfaction = -0,040

Mann-Whitney U:
994.174,50

p-value:
0,082766

Nível de significância:
0,05

Mediana da satisfação — grupo mais cedo:
3,00

Mediana da satisfação — grupo mais tarde:
3,00
```

---

# 👨‍💻 Projeto

**FintechGuard**

Projeto acadêmico desenvolvido para explorar conceitos de:

- Análise Exploratória de Dados;
- Estatística;
- Segurança;
- APIs;
- FastAPI;
- Inteligência Artificial;
- Atendimento ao cliente.

---

## 📄 Licença

Este projeto utiliza um dataset disponibilizado sob licença Apache 2.0, conforme informado na fonte utilizada para a base de dados.
