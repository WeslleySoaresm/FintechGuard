# Tarefa 6 — Documento de Planejamento T2

## 1. Objetivo

Este documento apresenta o planejamento inicial para o desenvolvimento de um modelo de classificação de texto no projeto FintechGuard e identifica as informações necessárias para a preparação das atividades de segurança previstas para o TP4/TP5.

O planejamento contempla a escolha do modelo candidato, a estratégia de transformação dos textos em características numéricas, a identificação do colega adversário e a definição da API que será utilizada nos testes autorizados.

## 2. Modelo candidato

**Modelo candidato: Regressão Logística multiclasse (*Logistic Regression*).**

A Regressão Logística será utilizada como modelo candidato para classificar tickets de atendimento de clientes de acordo com a intenção expressa na descrição textual.

O problema possui cinco classes:

- **Billing inquiry:** dúvidas relacionadas a cobranças e faturamento.
- **Cancellation request:** solicitações de cancelamento.
- **Product inquiry:** dúvidas e solicitações de informações sobre produtos.
- **Refund request:** solicitações de reembolso.
- **Technical issue:** problemas ou dificuldades técnicas.

A escolha da Regressão Logística considera sua aplicação em problemas de classificação, sua capacidade de trabalhar com representações numéricas esparsas de textos e sua utilização como modelo inicial para estabelecer uma referência de desempenho.

Como alternativa, poderá ser avaliada uma SVM (*Support Vector Machine*), que também é utilizada em tarefas de classificação textual.

A comparação entre os modelos poderá ser realizada posteriormente, utilizando as mesmas divisões de treino e teste para garantir uma avaliação consistente.

## 3. Estratégia de feature engineering para texto

**Estratégia escolhida: TF-IDF (*Term Frequency–Inverse Document Frequency*).**

O TF-IDF será utilizado para transformar as descrições textuais dos tickets em representações numéricas que possam ser processadas pelo modelo de classificação.

Essa técnica atribui pesos aos termos de acordo com sua frequência no documento e sua distribuição no conjunto de documentos. Dessa forma, termos informativos podem receber maior relevância do que palavras muito comuns no corpus.

### 3.1. Etapas planejadas

1. Identificar a coluna que contém a descrição textual dos tickets e a coluna correspondente à intenção ou categoria.
2. Verificar valores ausentes, registros inválidos e possíveis inconsistências nos dados.
3. Separar o conjunto de dados em treino e teste, utilizando divisão estratificada quando aplicável.
4. Ajustar o `TfidfVectorizer` exclusivamente com os textos de treino.
5. Transformar os textos de treino e teste usando o vetor ajustado.
6. Treinar a Regressão Logística com os vetores produzidos pelo TF-IDF.
7. Avaliar os resultados utilizando acurácia, precisão, recall, F1-score e matriz de confusão.
8. Registrar os resultados, limitações e possíveis melhorias do modelo.
9. Se necessário, comparar o resultado com uma SVM utilizando o mesmo procedimento de avaliação.

O ajuste do TF-IDF deverá ocorrer somente nos dados de treino, evitando o vazamento de informações do conjunto de teste.

### 3.2. Ferramentas previstas

- Python.
- Pandas para manipulação dos dados.
- Scikit-learn para transformação textual, treinamento e avaliação.
- `TfidfVectorizer` para extração de características.
- `LogisticRegression` como modelo candidato.
- Métricas de classificação e matriz de confusão para avaliação.

Os parâmetros finais do vetor e do modelo serão definidos durante a implementação experimental.

## 4. Identificação do colega adversário

**Status: pendente de definição pela turma.**

- **Nome do colega adversário:** a confirmar.
- **Equipe ou identificação acadêmica:** a confirmar, se exigida pela atividade.
- **Confirmação da participação:** pendente.

A identificação será atualizada após a definição do colega adversário pelo professor ou pela organização da atividade.

Nenhum nome será registrado como definitivo antes dessa confirmação.

## 5. API adversária para o TP4/TP5

**Status: pendente de identificação e confirmação do endereço.**

- **URL ou IP da API:** a confirmar.
- **Responsável pela API:** a confirmar após a identificação do colega adversário.
- **Endpoints autorizados:** a confirmar.
- **Escopo e limites dos testes:** a confirmar conforme as regras da atividade acadêmica.

A API deverá ser identificada e confirmada antes da realização dos testes. As atividades serão limitadas ao ambiente explicitamente autorizado, respeitando os endpoints, limites e condições estabelecidos para o exercício.

Nenhuma requisição de teste será direcionada a uma API de terceiros sem autorização explícita.

## 6. Critérios de avaliação e conclusão

O planejamento será considerado integralmente preenchido quando:

- [ ] O modelo candidato estiver documentado.
- [ ] A estratégia de feature engineering estiver definida.
- [ ] O colega adversário estiver identificado.
- [ ] A URL ou o IP da API alvo estiver confirmado.
- [ ] Os endpoints e os limites autorizados para os testes estiverem documentados.

Após a conclusão desses itens, o documento será revisado e atualizado no repositório do projeto.

## 7. Próximas etapas

1. Confirmar o colega adversário com a turma ou com o professor.
2. Obter e validar o endereço da API disponibilizada para a atividade.
3. Registrar o escopo autorizado e os limites dos testes.
4. Implementar e avaliar o modelo de classificação textual conforme o planejamento.
5. Atualizar este documento com as informações confirmadas.
6. Versionar as alterações no Git e publicá-las no repositório FintechGuard.

## 8. Considerações finais

Este documento estabelece as decisões técnicas iniciais para a classificação textual e organiza as informações necessárias para o planejamento das atividades de segurança do TP4/TP5.

A Regressão Logística com TF-IDF será a abordagem inicial proposta para o problema de classificação. A escolha poderá ser comparada com uma SVM durante a experimentação.

A identificação do colega adversário e o endereço da API permanecem pendentes, devendo ser preenchidos somente após confirmação pela turma ou pelo professor.