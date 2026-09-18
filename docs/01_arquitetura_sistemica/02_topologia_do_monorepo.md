# Documento 02: Topologia do Monorepo e Engenharia de Módulos

*Iniciativa de Pesquisa e Desenvolvimento: CINAS — Grupo de Pesquisa em Computação e Inteligência Artificial em Nuclear e Saúde (IPEN-CNEN/SP)*

## 1. Princípios de Design Modular e Domain-Driven Design (DDD) no Odoo

O desenvolvimento da localização brasileira para a pós-graduação *Stricto Sensu* impõe o uso de padrões avançados de arquitetura de software para mitigar acoplamentos destrutivos. O monorepo `l10n_br_openeducat_capes` adota os princípios do Domain-Driven Design (DDD), dividindo as complexidades de negócio em submódulos independentes e isolados no ecossistema Odoo.

Essa separação cirúrgica de responsabilidades garante que falhas pontuais em integrações de APIs externas ou atualizações de layouts documentais de diplomas não gerem impactos ou indisponibilidades no motor acadêmico central e no livro-razão de créditos. A extensibilidade do framework Odoo é explorada através do mecanismo de herança estrita, permitindo que cada submódulo injete campos, visualizações e lógicas específicas apenas em suas respectivas camadas de domínio.

## 2. Arquitetura Detalhada do Monorepo (`l10n_br_openeducat_capes`)

A árvore de diretórios do ecossistema e o escopo funcional e técnico de cada componente estrutural do monorepo estão descritos a seguir:

```text
l10n_br_openeducat_capes/
├── docs/
│   ├── 01_arquitetura_sistemica/
│   ├── 02_governanca_regimental_e_creditos/
│   ├── 03_dicionarios_de_dados_dav/
│   ├── 04_processos_da_vida_academica/
│   ├── 05_produtos_tecnico_tecnologicos_ptt/
│   ├── 06_titulacao_e_conformidade_documental/
│   └── 07_padroes_de_interoperabilidade_externa/
├── l10n_br_openeducat_capes_core/
├── l10n_br_openeducat_capes_admission/
├── l10n_br_openeducat_capes_academic/
├── l10n_br_openeducat_capes_research/
├── l10n_br_openeducat_capes_thesis/
├── l10n_br_openeducat_capes_ptt/
├── l10n_br_openeducat_capes_integration/
├── l10n_br_openeducat_capes_diploma/
└── l10n_br_openeducat_capes_scholarship/
```

### 2.1. `l10n_br_openeducat_capes_core`

* **Escopo:** Mapeia a ontologia primária e as entidades estáticas fundamentais do Módulo 01 e Módulo 02 do dicionário de dados da DAV, além da integração com entidades curriculares de base do OpenEduCat (`op.academic.year`, `op.academic.term`, `op.department`, `op.program`, `op.course`, `op.batch`, `op.category`).
* **Modelos Estendidos/Criados:** `res.company`, `res.partner`, `op.program.capes`, `op.program.concentration.area`, `op.program.research.line`, `op.faculty`, `op.student`.
* **Responsabilidade Técnica:** Armazenar os códigos SNPG e e-MEC, estruturar os georreferenciamentos de campi, gerenciar áreas de concentração e linhas de pesquisa canônicas, e gerenciar a injeção rígida dos Identificadores Persistentes (PIDs) acadêmicos universais (ORCiD, Lattes, ROR e ISNI). Assegura a unicidade do Registro Acadêmico (RA) perene e inviolável por CPF no âmbito de cada IES (`res.company`), servindo de esteio para a arquitetura multi-vínculo de discentes (Opção B), parsing robusto de prenomes/sobrenomes segundo a onomástica brasileira (`_parse_brazilian_name`) e coleta censitária demográfica completa (filiação, raça/cor, PCD, naturalidade e níveis acadêmicos). Registra a filiação do discente ao programa acadêmico através do campo relacional `program_id` (`Many2one` para `op.program.capes`, indexado), exibido no formulário discente na aba "Vínculo Regimental e Proficiências" (logo abaixo do RA) e sincronizado de forma automática com a Versão Regimental (`curriculum_version_id.program_id`).

### 2.2. `l10n_br_openeducat_capes_admission`

* **Escopo:** Substitui o fluxo linear de inscrição de alunos nativo do OpenEduCat por uma estrutura de concorrência pública baseada em normas brasileiras.
* **Modelos Estendidos/Criados:** `op.admission.register`, `op.admission.edital`, `op.edital.phase`, `op.student.work_plan`.
* **Responsabilidade Técnica:** Gerenciar editais parametrizáveis com tabelas One2many para fases de seleção com pontuações ponderadas, controle de ações afirmativas (cotas de 20%), ranqueamento eliminatório/classificatório, mecanismo de Aprovação por Soberania do Coordenador (`is_override`), gatilho de evasão precoce (3 semanas de ausência) e submissão/avaliação do Plano de Trabalho Discente com trava ética do CEP. Reconhece discentes previamente cadastrados na IES (ex: ex-alunos especiais), reaproveitando a chave perene de `op.student` e criando novos vínculos regulares sem duplicação de identidade.

### 2.3. `l10n_br_openeducat_capes_academic`

* **Escopo:** Rege a vida estudantil corrente, orquestra a governança colegiada (CPG), implementa a visão 360° integrada de discentes e docentes, e implementa a inteligência de regras curriculares do Módulo 03 da DAV.
* **Modelos Estendidos/Criados:** `op.subject`, `op.batch`, `op.session`, `op.curriculum.version`, `op.student.credit.ledger`, `op.academic.request`, `op.special.credit.incorporation.request`, `op.faculty.program.link`, `op.faculty.category.ledger`, `op.cpg.committee`, `op.cpg.member`, `op.cpg.meeting`, `op.cpg.approval.log`.
* **Responsabilidade Técnica:** Versionamento dinâmico de regulamentos, operação do livro-razão imutável de integralização de créditos (diferenciando disciplinas internas, intra-IES, quarentena de aluno especial, especiais incorporadas e extra-IES), automação de matrículas compulsórias de acompanhamento de pesquisa, trava de carga inicial de calouros (mínimo 24 créditos), fluxo de aproveitamento e incorporação formal de créditos cursados como especial via CPG com controle decadencial de 36 meses, fluxo de ajuste manual retroativo com selo de auditoria, e gestão de pautas/atas QWeb da CPG (colegiado com 6 membros titulares e 4 suplentes, reuniões mensais com pautas abertas, deliberação de requerimentos discentes e aprovação auditável com registro de User ID, Timestamp e IP via `op.cpg.approval.log`). Oferece visão 360° em discentes (smart buttons para vínculos, créditos, trabalhos finais, PTTs, requerimentos, diplomas, tabela de créditos embutida e emissão direta do Histórico Escolar no cabeçalho) e docentes (orientandos ativos e egressos, disciplinas lecionadas, linhas de pesquisa e bancas).

### 2.4. `l10n_br_openeducat_capes_research`

* **Escopo:** Mapeia a estrutura de fomento e atividade de investigação descrita no Módulo 05 da DAV.
* **Modelos Estendidos/Criados:** `capes.research.project`, `capes.project.member`.
* **Responsabilidade Técnica:** Estender as capacidades de gerenciamento de projetos nativas do Odoo para capturar a natureza científica da pesquisa, classificar parcerias interinstitucionais e vincular pesquisadores às entregas operando sob a Taxonomia CRediT.

### 2.5. `l10n_br_openeducat_capes_thesis`

* **Escopo:** Governa as regras acadêmicas de ritos de passagem intermediários e finais do Módulo 04 da DAV.
* **Modelos Estendidos/Criados:** `capes.thesis`, `capes.thesis.committee`.
* **Responsabilidade Técnica:** Orquestrar o fluxo bipartido (Seminário Geral de Área/Qualificação e Defesa com quórum e composição de PhDs parametrizáveis por regimento via `op.curriculum.committee.rule`), auditar pré-requisitos do Plano de Trabalho homologado, gerenciar o processamento de impedimentos éticos e endogenia em comissões julgadoras, registrar cronometria de exposição/arguição (50 min / 40 min) e controlar o prazo limite de 30 dias para depósito da versão eletrônica no DSpace.

### 2.6. `l10n_br_openeducat_capes_ptt`

* **Escopo:** Internaliza a taxonomia e a engenharia de avaliação qualitativa do Grupo de Trabalho de Produção Técnica (GTPT) e Comitê Medicina II da CAPES para programas profissionais.
* **Modelos Estendidos/Criados:** `capes.ptt.axis`, `capes.ptt.type`, `capes.ptt.product`, `capes.ptt.evaluation`.
* **Responsabilidade Técnica:** Processar o motor de regras do Qualis Tecnológico, validar de forma eliminatória a aderência institucional de produções intelectuais, mapear níveis de Maturidade Tecnológica (TRL 1-9) e computar a média de notas para estratificação em tempo real (T1 a T5 ou TNC) servindo como pré-requisito de defesa e gerador de créditos APO.

### 2.7. `l10n_br_openeducat_capes_integration`

* **Escopo:** Concentra a inteligência de conectividade e o mapeamento semântico de comunicação externa da DAV Módulo 06.
* **Modelos Estendidos/Criados:** `capes.intellectual.production`.
* **Responsabilidade Técnica:** Expor controladores RESTful (rotas HTTP `/api/capes/v1/`) para transmissão de payloads JSON criptografados para a rede RICA|PG, gerenciar as autorizações OAuth 2.0 e atuar como barramento unificado de cruzamento semântico com os esquemas de conversão XSLT do DSpace (`oai_capes`).

### 2.8. `l10n_br_openeducat_capes_diploma`

* **Escopo:** Garante a conformidade jurídica de encerramento de percurso e expedição documental de graus acadêmicos em conformidade com o MEC (Portaria nº 70/2025).
* **Modelos Estendidos/Criados:** `op.student.transcript.br`.
* **Responsabilidade Técnica:** Renderizar relatórios QWeb consolidados de históricos parciais/finais auto-autenticados com Hash SHA-256 e QR Code, gerar arquivos XML estruturados de diplomas de pós-graduação e documentação acadêmica digital, e orquestrar rotinas criptográficas Python para aplicação de assinaturas avançadas XAdES ICP-Brasil (Certificado A3/HSM) com Carimbos de Tempo.

### 2.9. `l10n_br_openeducat_capes_scholarship`

* **Escopo:** Governa o livro de cotas institucionais de bolsas (CAPES, CNPq, CNEN, FAPs), editais de distribuição de bolsas, processos avaliativos com múltiplos revisores docentes em paralelo e ciclo de vida de concessão sem gestão financeira direta (Portaria CAPES nº 133/2023 e IN CNEN nº 07/2024).
* **Modelos Estendidos/Criados:** `capes.scholarship.sponsor`, `capes.scholarship.quota`, `capes.scholarship.rubric`, `capes.scholarship.rubric.item`, `capes.scholarship.edital`, `capes.scholarship.application`, `capes.scholarship.evaluation`, `capes.scholarship.evaluation.line`, `capes.scholarship.assignment`, `op.student` (extensão), `op.faculty` (extensão).
* **Responsabilidade Técnica:** Operar o saldo de cotas de bolsas sem pagamento financeiro direto pela IES; gerenciar editais parametrizados com reserva de cotas (PPI e Ampla Concorrência) e regras de reversão; viabilizar matriz avaliativa em 4 colunas (Autoavaliação, Revisor 1, Revisor 2 e Consolidação pela CPG) com revisores operando em paralelo; aplicar fórmulas lineares e tetos dinâmicos sem hardcode regimental; verificar limites regulamentares de acúmulo temporal (24m ME / 48m DO) e regras de vínculo empregatício sob deliberação da CPG; gerar termos de compromisso digital e auditar frequências e relatórios anuais.

## 3. Matriz de Dependências e Manifestos do Odoo (`__manifest__.py`)

Para assegurar a integridade do monorepo e a correta carga de dados no banco relacional PostgreSQL, a árvore de dependências do Odoo é rigorosamente respeitada. Cada submódulo possui um arquivo descriptor `__manifest__.py` indicando suas dependências obrigatórias de inicialização:

```text
[openeducat_core]
^
|
[l10n_br_openeducat_capes_core] <---------------------------------------+
^                     ^                                          |
|                     |                                          |
[l10n_br_openeducat_capes_admission] <───┐                         |
^                                │                         |
|                                │                         |
[l10n_br_openeducat_capes_academic] <---+│                         |
^          ^                     |│                        |
|          |                     ||                        |
|          +---------------------+│                        |
|                                ||                        |
[l10n_br_openeducat_capes_research]     ||                        |
^                                |│                        |
|                                ||                        |
[l10n_br_openeducat_capes_thesis] ------+┘                        |
^                                ^                         |
|                                |                         |
[l10n_br_openeducat_capes_ptt] ---------+                         |
^                                                          |
|                                                          |
[l10n_br_openeducat_capes_integration]                            |
^                                                          |
|                                                          |
[l10n_br_openeducat_capes_diploma] -------------------------------+
^
|
[l10n_br_openeducat_capes_scholarship] (core + academic + admission)

```

Abaixo está a especificação exata das chaves `depends` presentes em cada manifesto de domínio:

| Submódulo Odoo | Módulos Obrigatórios em `depends` | Tipo de Dependência |
| --- | --- | --- |
| `l10n_br_openeducat_capes_core` | `['openeducat_core']` | Extensão Base de Infraestrutura |
| `l10n_br_openeducat_capes_admission` | `['l10n_br_openeducat_capes_core']` | Extensão do Fluxo de Admissão e Plano de Trabalho |
| `l10n_br_openeducat_capes_academic` | `['l10n_br_openeducat_capes_core']` | Motor Curricular, Regimentos e CPG |
| `l10n_br_openeducat_capes_research` | `['l10n_br_openeducat_capes_academic', 'project']` | Integração Odoo Projects e Fomento |
| `l10n_br_openeducat_capes_thesis` | `['l10n_br_openeducat_capes_academic', 'l10n_br_openeducat_capes_admission', 'l10n_br_openeducat_capes_research']` | Ritos Bipartidos, Plano de Trabalho e Qualificação |
| `l10n_br_openeducat_capes_ptt` | `['l10n_br_openeducat_capes_core', 'l10n_br_openeducat_capes_academic', 'l10n_br_openeducat_capes_thesis']` | Qualis, Eixos GTPT e Trava PTT |
| `l10n_br_openeducat_capes_integration` | `['l10n_br_openeducat_capes_core', 'l10n_br_openeducat_capes_ptt']` | Barramento RESTful e OAI-PMH |
| `l10n_br_openeducat_capes_diploma` | `['l10n_br_openeducat_capes_core', 'l10n_br_openeducat_capes_academic', 'l10n_br_openeducat_capes_thesis']` | Conformidade MEC, Teses e Criptografia |
| `l10n_br_openeducat_capes_scholarship` | `['l10n_br_openeducat_capes_core', 'l10n_br_openeducat_capes_academic', 'l10n_br_openeducat_capes_admission']` | Gestão de Cotas, Editais de Bolsa e Pareceres |

## 4. Modelo de Extensibilidade e Herança Estrita (`_inherit`)

A arquitetura baseia-se prioritariamente no mecanismo de herança de tabelas e objetos (`_inherit`) nativo do ORM do Odoo, preservando o núcleo original e injetando modificações nas tabelas relacionais do PostgreSQL sem corromper a integridade dos dados originais.

* **Herança Clássica (`_inherit = 'res.partner'`):** Adotada para embutir de maneira transparente as extensões de PIDs biográficos e civis sem alterar as capacidades originais de faturamento, CRM ou contabilidade associadas à classe de contatos nativa do Odoo.
* **Onomástica Brasileira e Higienização de Nomes (`_parse_brazilian_name`):** Algoritmo inteligente que particiona nomes completos garantindo a presença do `first_name`, `middle_name` e `last_name` sem deixar campos nulos na presença de sobrenomes compostos, e garantindo a unicidade nominal de 100% dos discentes e docentes em nível de coorte/turma.
* **Alinhamento com a Configuração Nativa OpenEduCat:** Total compatibilidade e preenchimento dos menus do módulo base (`op.academic.year`, `op.academic.term`, `op.department`, `op.program.level`, `op.program`, `op.course`, `op.batch`, `op.category`), permitindo que a secretaria e a coordenação operem a suíte acadêmica em harmonia com as extensões da CAPES.
* **Herança Funcional de Workflow:** Submódulos avançados estendem as máquinas de estado originais reescrevendo métodos Python em instâncias como `op.admission.register`, injetando decoradores `@api.constrains` para bloquear transições de estado lineares caso inconsistências com regulamentos ou ausência de validação de proficiências sejam detectadas no banco de dados.

## 5. Arquitetura Técnica de Isolamento Multiprograma e Contexto Ativo (Opção B)

Para atender a universidades descentralizadas mantendo uma única pessoa jurídica soberana (`res.company`), o monorepo adota o isolamento multiprograma na camada de segurança e contexto da aplicação.

### 5.1. Extensão de Usuários e Sessão (`res.users`)
* `allowed_program_ids` (Many2many com `op.program.capes`): define o conjunto de programas de pós-graduação sobre os quais o usuário tem credenciais de acesso autorizadas.
* `current_program_id` (Many2one com `op.program.capes`): programa ativo na sessão corrente do usuário.
* `is_central_admin` (Boolean): indica perfil de Pró-Reitoria / TI Central, com visão consolidada e sem restrição de filtros.
* `action_switch_program(program_id)`: método RPC que valida permissões, atualiza `current_program_id` e recarrega o contexto da interface web sem logout.
* `_get_session_info()`: estendido para injetar `current_program_id`, `allowed_program_ids` e `is_central_admin` no payload inicial da sessão web do Odoo.

### 5.2. Grupos de Segurança Hierárquicos
* **Administrador Central de Pós-Graduação (`group_capes_central_admin`):** Pertence à Pró-Reitoria de Pós-Graduação ou administração central da IES. Visualiza e administra todos os programas, unidades e relatórios integrados.
* **Coordenador de Programa de Pós-Graduação (`group_capes_program_coordinator`):** Gestão acadêmica e colegiada estrita ao seu programa (ou programas permitidos).
* **Secretaria de Programa de Pós-Graduação (`group_capes_program_secretary`):** Operação cotidiana de matrículas, turmas, requerimentos e cadastros. Pode ter permissão para um ou mais programas, alternando entre eles pelo seletor de contexto.
* **Corpo Docente (`openeducat_core.group_op_faculty`):** Visualiza discentes sob sua orientação, disciplinas atribuídas e bancas examinadoras.
* **Corpo Discente (`base.group_portal`):** Isolamento absoluto estrito à sua própria identidade e histórico via chave de discente (`user.id == student_id.user_id`).

### 5.3. Camada de Frontend OWL e Interfaces de Alternância de Programa
* **Componente `ProgramMenu` (Systray):** Widget JavaScript OWL registrado na barra superior do Odoo (`web.systray`).
  * Para usuários multiprograma: exibe o badge do programa ativo e menu dropdown com a lista de programas autorizados. A seleção invoca `action_switch_program` e recarrega a visualização ativa.
  * Para instituições de programa único (ex: MPTRCS / IPEN): exibe o badge estático com o nome do programa, sem abrir dropdown e sem exigir cliques adicionais, garantindo 100% de transparência operacional.
  * Para administradores centrais: inclui a opção "Todos os Programas (Consolidado)".
* **Alternância Integrada em `op.program.capes` (Views XML):**
  * **Visualização em Lista (`tree view`):** Coluna com status badge (`Programa Ativo` / `Disponível`), botão inline direto de alternância (`fa-exchange`) e ação coletiva *"Alternar para esse Programa"* no menu **Ações (Actions)**.
  * **Visualização em Formulário (`form view`):** Botão primário no cabeçalho `<header>` *"Alternar para este Programa"* para programas não ativos e selo gráfico em fita `web_ribbon` (**"Programa Ativo"**) quando o programa em exibição coincide com a sessão de trabalho.

### 5.4. Regras de Registro (`ir.rule`) e Indexação Relacional
* Todo modelo de dados operacional possui chave relacional para `program_id` (direta ou computada e armazenada com `index=True`):
  * `op.batch`, `op.course`, `op.curriculum.version`, `op.student.credit.ledger`, `op.academic.request`, `op.cpg.meeting`, `op.admission.register`, `op.admission.edital`, `capes.thesis`, `capes.ptt.product`, `capes.scholarship.edital`, `capes.scholarship.quota`, etc.
* As regras de registro aplicam filtros restritivos:
  * Administrador Central: `[(1, '=', 1)]` (irrestrito).
  * Coordenação e Secretaria: `['|', ('program_id', '=', False), ('program_id', 'in', user.allowed_program_ids.ids)]` com filtro contextual prioritário em `user.current_program_id.id`.
  * Discente: `[('student_id.user_id', '=', user.id)]` ou `[('user_id', '=', user.id)]`.
