# Evidências do FintechGuard

Este diretório reúne os artefatos entregáveis de análise, segurança, arquitetura e treinamento. Relatórios e imagens ficam junto ao grupo de evidência correspondente.

## EDA e classificação

- [Relatório de EDA](eda/EDA_REPORT.md) — problema, dados, análise, insights e próximos passos para o TP3.
- [Notebook executável](eda/eda_tp2.ipynb) — heatmap Seaborn e teste Mann–Whitney com SciPy.
- [Gráficos exportados](eda/graficos/) e [métricas/auditorias do dataset](eda/) — saídas reproduzíveis da análise e treinamento.
- [Evidências do classificador](01_classificador/) — imagens e registro do treinamento V2.

## Segurança e arquitetura

- [Relatório final da auditoria](seguranca/relatorio_auditoria_final.md) — controles, estado e plano de validação.
- [Relatório narrativo OWASP ZAP](seguranca/owasp_zap_report.md) — análise passiva e tratamento dos alertas previamente documentados.
- [Capturas do ZAP](seguranca/img/) — imagens de apoio.
- [Diagrama de fluxo de dados](arquitetura/DiagramaDeFluxoDeDados.png).

- [Escopo dos testes automatizados](testes.md).

## Limite das evidências do ZAP

O arquivo CSV recebido em 9 de novembro de 2026 é um histórico de tráfego HTTP do proxy; não contém a exportação de alertas com IDs, descrições e severidades. Portanto, os relatórios narrativos não substituem o export HTML/JSON do ZAP. Esse artefato permanece pendente para fechar a rastreabilidade dos findings.
