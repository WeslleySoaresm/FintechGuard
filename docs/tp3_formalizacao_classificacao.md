# TP3 — Tarefa 5: Formalização da Pergunta de Classificação

## 1. Pergunta de classificação

Dado um texto de atendimento ao cliente, qual é a intenção do usuário?

O objetivo é investigar a possibilidade de identificar automaticamente a intenção expressa pelo cliente em um chamado de suporte, utilizando técnicas de aprendizado de máquina supervisionado.

A entrada do modelo será o texto da descrição do chamado, representado pela coluna `Ticket Description`. A saída esperada será a categoria correspondente à coluna `Ticket Type`.

Esse problema é classificado como **classificação multiclasse supervisionada**, pois o modelo deverá prever uma entre cinco categorias possíveis, utilizando exemplos previamente classificados para o treinamento.

## 2. Classes (intenções) que o modelo vai prever

A análise do arquivo `customer_support_tickets_cleaned.csv` identificou cinco classes na coluna `Ticket Type`, após a normalização das diferenças entre letras maiúsculas e minúsculas.

| Classe | Significado |
|---|---|
| `refund request` | Solicitação de reembolso |
| `technical issue` | Relato de problema técnico |
| `cancellation request` | Solicitação de cancelamento |
| `product inquiry` | Consulta ou dúvida sobre um produto |
| `billing inquiry` | Dúvida relacionada a cobrança ou faturamento |

Essas categorias representam as intenções que o modelo deverá aprender a reconhecer a partir do texto fornecido pelo cliente.

## 3. Distribuição das classes no dataset

O dataset analisado possui **8.467 registros e 17 colunas originais**. A distribuição das classes identificadas está apresentada na tabela a seguir.

| Classe | Quantidade de registros | Percentual |
|---|---:|---:|
| `refund request` | 1.751 | 20,68% |
| `technical issue` | 1.749 | 20,66% |
| `cancellation request` | 1.694 | 20,01% |
| `product inquiry` | 1.640 | 19,37% |
| `billing inquiry` | 1.633 | 19,29% |
| **Total** | **8.467** | **100%** |

A distribuição é relativamente equilibrada, pois as classes apresentam frequências próximas. A categoria mais frequente é `refund request`, com 20,68% dos registros, enquanto `billing inquiry` é a menos frequente, com 19,29%.

Esse equilíbrio é relevante para a avaliação do futuro classificador, embora não garanta, por si só, um bom desempenho preditivo.

## 4. Por que a regressão linear não é adequada para esse problema?

A regressão linear é utilizada principalmente para prever valores numéricos contínuos, como preços, custos ou quantidades. Entretanto, neste problema, a saída desejada é uma categoria de intenção, e não um valor numérico.

Atribuir números arbitrários às cinco categorias e utilizar regressão linear poderia introduzir uma ordem e distâncias numéricas artificiais entre classes que não possuem essa relação. Além disso, o modelo poderia produzir previsões intermediárias que não correspondem a nenhuma categoria válida.

Por esse motivo, o problema deve ser tratado como classificação multiclasse. Algoritmos próprios para classificação, como regressão logística multinomial e máquinas de vetores de suporte (SVM), podem ser investigados em etapas posteriores.

## 5. Conclusão

A pergunta de pesquisa foi formalizada como um problema de classificação multiclasse supervisionada, cujo objetivo é prever a intenção do cliente a partir do texto de atendimento.

Foram identificadas cinco classes na coluna `Ticket Type`, com distribuição relativamente equilibrada entre os 8.467 registros analisados. Como a saída representa categorias, a regressão linear não é adequada para resolver diretamente esse problema.

Uma etapa futura poderá avaliar modelos de classificação e métricas como acurácia, precisão, recall e F1-score para verificar a capacidade de identificar corretamente as diferentes intenções.