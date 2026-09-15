

# 📊 Análise Exploratória e Gráfica de Dados (EDA)

Esta documentação analisa os resultados obtidos a partir dos scripts de visualização do dataset `customer_support_tickets.csv` ($8.469$ registros).

---

## 📈 Análise dos Gráficos Compilados do Código

### 1. Tipo de Ticket (`ticket_type.png`)

* **Descrição Visual:** Gráfico de barras na horizontal/vertical ordenando a frequência das categorias de intenção.
* **Métricas Extraídas:**
* `Refund request` (Solicitação de Reembolso): $1.752$ chamados ($20,69\%$)
* `Technical issue` (Problema Técnico): $1.747$ chamados ($20,63\%$)
* `Cancellation request` (Cancelamento): $1.695$ chamados ($20,01\%$)
* `Product inquiry` (Dúvida sobre Produto): $1.641$ chamados ($19,38\%$)
* `Billing inquiry` (Dúvida de Cobrança): $1.634$ chamados ($19,29\%$)


* **Diagnóstico Técnico:** A variável apresenta um **balanceamento quase perfeito** entre as 5 classes (variação inferior a $1,4\%$). Isso garante que o modelo de IA de classificação não sofrerá de viés (*bias*) por desproporção de amostras.

---

### 2. Prioridade do Ticket (`ticket_priority.png`)

* **Descrição Visual:** Gráfico de barras dividindo os volumes pelas faixas de severidade.
* **Métricas Extraídas:**
* `Medium` (Média): $2.192$ chamados ($25,88\%$)
* `Critical` (Crítica): $2.129$ chamados ($25,14\%$)
* `High` (Alta): $2.085$ chamados ($24,62\%$)
* `Low` (Baixa): $2.063$ chamados ($24,36\%$)


* **Diagnóstico Técnico:** A distribuição uniforme entre as prioridades sugere um processo de triagem inicial aleatório ou sintético no dataset original. Mais de $49,7\%$ dos tickets exigem atenção prioritária (Alta ou Crítica).

---

### 3. Canal de Atendimento (`ticket_channel.png`)

* **Descrição Visual:** Comparativo de volume de entrada pelos canais de comunicação.
* **Métricas Extraídas:**
* `Email`: $2.143$ chamados ($25,30\%$)
* `Phone` (Telefone): $2.132$ chamados ($25,17\%$)
* `Social media` (Redes Sociais): $2.121$ chamados ($25,04\%$)
* `Chat`: $2.073$ chamados ($24,48\%$)


* **Diagnóstico Técnico:** O comportamento do consumidor é **omnichannel equilibrado**. A IA precisará processar textos vindos de múltiplos formatos de entrada com a mesma eficiência.

---

### 4. Distribuição da Idade dos Clientes (`customer_age.png`)

* **Descrição Visual:** Histograma continuo de frequências de idade divididas em $20$ bins.
* **Métricas Extraídas:**
* **Faixa Etária:** $18$ a $70$ anos.
* **Média:** $44,03$ anos | **Mediana:** $44,00$ anos.
* **Desvio Padrão:** $15,30$ anos.


* **Diagnóstico Técnico:** A distribuição é estritamente **uniforme/plana**, abrangendo adultos de todas as idades de forma uniforme, sem concentração em faixas jovens ou idosas.

---

### 5. Avaliação de Satisfação (`customer_satisfaction.png`)

* **Descrição Visual:** Histograma discreto em 5 barras cobrindo a pontuação de 1 a 5.
* **Métricas Extraídas:**
* **Média:** $2,99$ (escala 1 a 5).
* **Distribuição das Avaliações válidas:** Nota 1 ($553$), Nota 2 ($549$), Nota 3 ($580$), Nota 4 ($543$), Nota 5 ($544$).
* **Valores Ausentes (NaN):** $5.700$ registros nulos.


* **Diagnóstico Técnico:** A média de satisfação está neutra ($2,99 \approx 3,0$). Os $5.700$ valores nulos representam chamados em aberto que não passaram por pesquisa de CSAT, sendo mantidos como nulos estruturais.

---

## 🖼️ Análise Especial para:  ![Visualizações da EDA](graphs/eda_visualizations.png)

A imagem revela uma tentativa de plotagem comparativa tripla utilizando a paleta `viridis`, `magma` e `mako`:

1. **Inconsistências no Gráfico de Tipo de Ticket (Esquerda):**
* As barras principais (`Refund request`, `Technical issue`, `Cancellation request`, `Product inquiry`, `Billing inquiry`) apresentam contagens normais de $1.600$ a $1.750$ registros.
* Na parte inferior, identificam-se **sujeiras e valores fantasma no dataset**, como a string isolada `"string"`, `"Suporte Técnico"` e `"Billing Inquiry"` com valores zerados ou irrelevantes.
* **Ação Recomendada:** Aplicar filtragem no pipeline para remover ou substituir *strings* de teste antes da vetorização do modelo.


2. **Formatação da Prioridade e Canais (Centro e Direita):**
* O gráfico do meio demonstra ordenação correta das prioridades (`Low`, `Medium`, `High`, `Critical`).
* O gráfico da direita exibe os canais principais e indica rótulos extras não populados (`string`, `App Mobile`) no eixo horizontal, confirmando que o schema do arquivo original continha colunas genéricas preenchidas durante testes.



---



## 📊 Análise Detalhada dos Gráficos do Projeto

### 1. Tipo de Ticket (`ticket_type.png`)
* **Métricas:** Reembolso (1.752), Problemas Técnicos (1.747), Cancelamentos (1.695), Dúvidas de Produtos (1.641) e Cobrança (1.634).
* **Conclusão:** O dataset possui classes totalmente balanceadas (~20% cada), eliminando a necessidade de técnicas de reamostragem (como SMOTE).

### 2. Prioridade dos Atendimentos (`ticket_priority.png`)
* **Métricas:** Média (2.192), Crítica (2.129), Alta (2.085) e Baixa (2.063).
* **Conclusão:** Quase 50% dos chamados estão classificados em prioridade Alta ou Crítica, demandando automação de resposta rápida para reduzir o SLA.

### 3. Canais de Comunicação (`ticket_channel.png`)
* **Métricas:** E-mail (2.143), Telefone (2.132), Redes Sociais (2.121) e Chat (2.073).
* **Conclusão:** Distribuição omnichannel homogênea. O agente de IA deve estar preparado para processar textos vindos de qualquer ponto de contato.

### 4. Perfil Etário (`customer_age.png`)
* **Métricas:** Intervalo de 18 a 70 anos, com média de 44 anos e desvio padrão de 15,3 anos.
* **Conclusão:** Distribuição uniforme sem concentração específica, indicando uma base de clientes diversificada.

### 5. Avaliação de Satisfação / CSAT (`customer_satisfaction.png`)
* **Métricas:** Média de 2,99 estrelas. Existem 5.700 registros nulos.
* **Conclusão:** Os valores ausentes correspondem a chamados em aberto (nulos estruturais). A nota neutra reflete oportunidades de melhoria no suporte automatizado.

```