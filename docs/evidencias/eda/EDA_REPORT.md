# Relatório de EDA — FintechGuard (TP2)

## Problema

O TP1 formulou a hipótese de que clientes associados a valores maiores de `First Response Time` poderiam apresentar menor satisfação. O TP2 aprofunda essa hipótese com análise descritiva, correlação e teste de hipótese. A variável representa o **horário** da primeira resposta, não a duração do tempo de espera; por isso, os resultados são interpretados como associação e não como efeito causal.

## Dados

A análise usa `data/customer_support_tickets.csv`. A fonte contém 8.484 linhas e 20 colunas. Após remover linhas totalmente vazias e duplicatas exatas, sete registros estruturais que continham pelo menos três campos textuais iguais a `string` e idade igual a 120 foram excluídos. A amostra final tem 8.473 registros. O notebook registra a limpeza e calcula as métricas diretamente da fonte.

As categorias `Cobrança` e `Suporte Técnico` são normalizadas para `Billing inquiry` e `Technical issue`. O notebook sinaliza oito registros com texto semelhante a HTML ou JavaScript para inspeção; eles permanecem na análise, pois esse padrão textual, isoladamente, não comprova um ataque.

## Análise

### Distribuição do target

| Tipo de ticket | Registros |
|---|---:|
| Refund request | 1.752 |
| Technical issue | 1.750 |
| Cancellation request | 1.695 |
| Product inquiry | 1.641 |
| Billing inquiry | 1.635 |

As cinco classes têm frequências relativamente próximas. Essa distribuição ajuda a planejar a avaliação multiclasse e reduz o risco de uma classe dominar as métricas globais.

### Correlação

O heatmap produzido com Seaborn no notebook `eda/eda_tp2.ipynb` apresenta as correlações entre idade, horário da primeira resposta em minutos desde meia-noite e avaliação de satisfação. A correlação entre `First Response Minutes` e satisfação é **−0,040**; entre idade e satisfação, **−0,005**. Ambos os valores indicam associação linear muito fraca nesta amostra.

### Teste de hipótese

- **H0:** as distribuições de satisfação dos grupos com horário da primeira resposta abaixo e acima da mediana não diferem.
- **H1:** as distribuições diferem.
- **Teste:** Mann–Whitney U bilateral, SciPy.
- **Nível de significância:** α = 0,05.
- **Mediana do horário:** 710,20 minutos desde 00:00.
- **Tamanhos dos grupos:** 1.385 e 1.384 registros.
- **Mediana de satisfação em cada grupo:** 3,00.
- **Estatística U:** 994.174,50.
- **p-valor:** 0,082766.

Como p > 0,05, não rejeitamos H0. Em linguagem simples, os dados não fornecem evidência suficiente para afirmar que as distribuições de satisfação diferem entre os grupos definidos pelo horário da resposta. Isso não prova que sejam iguais. Como a variável registra horário e não duração, o resultado não demonstra que esperar mais ou menos cause uma alteração na satisfação.

## Insights

As classes de `Ticket Type` estão relativamente equilibradas, o que favorece uma avaliação por classe no problema de classificação. As associações lineares entre satisfação e as variáveis numéricas examinadas são pequenas. O teste formal também não encontrou evidência suficiente de diferença entre os grupos de horário ao nível de 5%. A principal cautela metodológica é preservar a semântica de `First Response Time`: ela não mede diretamente o tempo de espera do cliente.

## Próximos passos

Para o TP3, formular a classificação como previsão de `Ticket Type` a partir do texto do atendimento. Usar `Ticket Subject` e `Ticket Description` como features textuais, com TF‑IDF como representação inicial, e `Ticket Type` como target. Remover registros sem target, dividir treino e validação de forma estratificada, impedir duplicatas entre partições e comparar um baseline com classificadores usando F1 macro, matriz de confusão e métricas por classe. Não usar campos que só existem depois do atendimento — como `Resolution` e satisfação — como features de previsão.

## Artefatos relacionados

- Notebook executável da análise: [`eda_tp2.ipynb`](eda_tp2.ipynb).
- Script original de EDA, mantido: [`scripts/eda.py`](../../../scripts/eda.py).
- Formalização do problema de classificação do TP3: [`tp3_formalizacao_classificacao.md`](../../tp3_formalizacao_classificacao.md).
