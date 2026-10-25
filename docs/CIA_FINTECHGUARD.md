# Análise CIA aplicada aos componentes do FintechGuard

A tríade CIA (Confidentiality, Integrity and Availability), composta por Confidencialidade, Integridade e Disponibilidade, constitui um dos fundamentos da segurança da informação. No projeto FintechGuard, esses princípios são aplicados individualmente aos componentes da arquitetura, considerando os dados processados, as ameaças relevantes e os mecanismos de proteção necessários.

## 1. Componente: Autenticação e gerenciamento de sessões JWT

**Confidencialidade:** o sistema deve impedir que usuários não autenticados acessem informações protegidas. Para isso, utiliza autenticação por token JWT e validação das credenciais antes de permitir o acesso às rotas restritas.

**Integridade:** os tokens devem ser validados criptograficamente para impedir alterações não autorizadas nas informações utilizadas para identificar o usuário e suas permissões. A chave de assinatura deve ser mantida em segredo e configurada de forma segura.

**Disponibilidade:** mecanismos de limitação de tentativas de autenticação (*rate limiting*) ajudam a reduzir abusos, tentativas automatizadas de acesso e consumo excessivo de recursos.

**Riscos associados:** roubo ou falsificação de tokens, acesso indevido a contas e ataques de força bruta.

## 2. Componente: API de tickets e dados dos clientes

**Confidencialidade:** os tickets podem conter nomes, endereços de e-mail e descrições de problemas dos clientes. O acesso a esses registros deve respeitar as permissões do usuário autenticado, evitando a exposição de informações de outros clientes.

**Integridade:** os dados recebidos devem ser validados por modelos Pydantic. A aplicação também deve verificar a autorização antes de permitir alterações ou exclusões e utilizar consultas parametrizadas para reduzir o risco de injeção de SQL.

**Disponibilidade:** paginação nas consultas, limites para requisições e tratamento adequado de erros ajudam a evitar sobrecarga da API e melhorar a estabilidade do serviço.

**Riscos associados:** exposição de dados pessoais, vulnerabilidade de autorização em nível de objeto (BOLA), alteração indevida de tickets e negação de serviço.

## 3. Componente: Banco de dados e persistência dos tickets

**Confidencialidade:** o banco de dados deve ser acessível somente por componentes e usuários autorizados. Em ambientes de produção, devem ser considerados privilégios mínimos, proteção de credenciais e criptografia dos dados em trânsito e, quando aplicável, em repouso.

**Integridade:** restrições de unicidade, chaves primárias, validações e transações ajudam a manter a consistência dos registros. Migrações de esquema devem ser controladas e rastreáveis.

**Disponibilidade:** backups periódicos, procedimentos de restauração e monitoramento do armazenamento ajudam a reduzir o impacto de falhas ou perda de dados.

**Riscos associados:** acesso direto não autorizado, corrupção de registros, duplicação de identificadores e perda de dados por falhas operacionais.

## 4. Componente: Endpoint de predição de IA (`POST /predict`)

**Confidencialidade:** as descrições dos tickets enviadas ao endpoint devem ser protegidas contra acesso não autorizado e exposição indevida em logs. Caso os dados sejam enviados a um serviço externo de IA, também será necessário avaliar o compartilhamento de informações pessoais.

**Integridade:** a API deve validar a entrada, restringir campos inesperados quando apropriado e garantir que o resultado retornado siga o esquema de resposta definido. Quando o modelo real for integrado, será necessário controlar a versão do modelo e a origem dos dados utilizados.

**Disponibilidade:** limites de requisições, controle de tamanho das entradas, timeouts e tratamento de falhas do modelo podem impedir que solicitações excessivas ou erros de processamento prejudiquem a API.

**Riscos associados:** exposição de dados sensíveis, entradas malformadas, manipulação de solicitações e indisponibilidade causada por excesso de requisições ou falhas no serviço de IA.

## Síntese da análise

A análise demonstra que a tríade CIA precisa ser aplicada de acordo com as responsabilidades e os riscos de cada componente. A autenticação protege o acesso; a API de tickets controla a exposição e a manipulação de registros; o banco de dados preserva e mantém os dados; e o endpoint de predição protege as entradas e a disponibilidade do processamento de IA.

Os controles descritos representam medidas de projeto ou recomendações de segurança. Sua presença efetiva no sistema deve ser confirmada por meio da inspeção do código, da configuração do ambiente e de testes de segurança. Um controle planejado não deve ser apresentado como implementado sem evidências verificáveis.