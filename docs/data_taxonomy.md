
# FintechGuard - Taxonomia de Tickets

## Objetivo

Padronizar as categorias de atendimento utilizadas
na preparação dos dados e no classificador de intenção.

## Categorias oficiais

| Código | Categoria | Definição |
|---|---|---|
| ACC | Account Access | Login, senha e acesso à conta |
| BIL | Billing | Cobranças, faturas e valores |
| CAN | Cancellation | Cancelamento de serviços |
| CAR | Card | Problemas operacionais com cartões |
| FRD | Fraud | Relatos de possíveis fraudes |
| LOA | Loan | Empréstimos e parcelas |
| PIN | Product Inquiry | Dúvidas sobre produtos bancários |
| REF | Refund | Solicitações de reembolso |
| SEC | Security | Alertas e verificações de segurança |
| TEC | Technical Issue | Falhas técnicas em sistemas |
| TRA | Transaction | Transferências e transações |

## Mapeamento de categorias originais

- Billing -> Billing
- Billing inquiry -> Billing
- Cobrança -> Billing
- Technical issue -> Technical Issue
- Suporte Técnico -> Technical Issue

As demais categorias válidas mantêm seu significado,
com padronização de nomenclatura.

## Categorias não mapeadas

- V string
- string
- credito
- Account
- CREDITO
- Sem classificação

Esses registros exigem exclusão da base derivada
ou revisão manual. Os dados originais não devem
ser apagados.

## Regras de classificação

1. Fraud representa suspeita relatada, não fraude confirmada.
2. Security não significa necessariamente fraude.
3. Billing reúne dúvidas e problemas relacionados a cobranças.
4. A categoria principal não substitui uma futura subcategoria.
5. A origem e a classificação original devem ser preservadas.

## Limitações do dataset

As descrições são predominantemente genéricas e repetitivas.
O dataset não deve ser utilizado como evidência de fraude
transacional confirmada.
