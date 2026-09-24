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
* **Modelos Criados/Estendidos:**
  * Modelos Criados: `op.admission.edital`, `op.edital.phase`, `op.edital.slot.distribution`, `op.admission.candidate`, `op.student.work_plan`, `capes.student.professional.profile`.
  * Modelos Nativos Estendidos: `op.student` (`work_plan_ids`, `work_plan_count`, `action_view_work_plans`).
* **Responsabilidade Técnica:** Gerenciar editais parametrizáveis com tabelas One2many para fases de seleção com pontuações ponderadas, controle de ações afirmativas (cotas de 20%), ranqueamento eliminatório/classificatório, mecanismo de Aprovação por Soberania do Coordenador (`is_override`), conversão de candidato aprovado em aluno regular com verificação de proficiência linguística na admissão (`proficiency_stage == 'admission'`), submissão/avaliação do Plano de Trabalho Discente com trava ética do CEP, e cadastro do perfil profissional do discente (`capes.student.professional.profile`). Reconhece discentes previamente cadastrados na IES (ex: ex-alunos especiais), reaproveitando o RA institucional único e perene em `op.student` e criando novo vínculo regular em `op.student.course` sem duplicação de identidade.

### 2.3. `l10n_br_openeducat_capes_academic`

* **Escopo:** Rege a vida estudantil corrente, orquestra a governança colegiada (CPG), implementa a visão 360° integrada de discentes e docentes, e implementa a inteligência de regras curriculares do Módulo 03 da DAV.
* **Modelos Criados/Estendidos:**
  * Modelos Criados: `op.curriculum.version`, `op.curriculum.subject.rule`, `op.curriculum.committee.rule`, `op.student.credit.ledger`, `op.special.credit.incorporation.request`, `op.academic.request`, `op.faculty.program.link`, `op.faculty.category.ledger`, `op.cpg.committee`, `op.cpg.member`, `op.cpg.meeting`, `op.cpg.approval.log`.
  * Modelos Nativos Estendidos:
    * `op.subject`: créditos sincronizados com `grade_weightage`, ementa (`syllabus`), bibliografia básica/complementar, indicador PHEA, idioma de oferta e governança de alunos especiais (`allow_special_students`, `special_seats_quota`, `special_student_instructor_consent_required`).
    * `op.batch`: chave relacional com o programa PPG (`program_id`).
    * `op.student.course`: multi-vínculo com tipo de curso (`course_type`), programa (`program_id`), versão curricular (`curriculum_version_id`), datas de início e encerramento.
    * `op.student`: campos do livro-razão (`credit_ledger_ids`, `credit_ledger_count`), aproveitamento (`special_request_ids`, `special_req_count`) e totalizadores de créditos (`total_disciplinas_credits`, `total_complementar_credits`, `total_conferred_credits`).
    * `op.faculty`: vínculos credenciados (`program_link_ids`, `accreditation_count`), lista de programas locais (`program_ids`), resumo de filiações (`programs_summary`), contagem de vínculos permanentes (`permanent_programs_count`), conformidade da Portaria CAPES 81/2016 (`capes_program_compliance`) e trava `_check_capes_permanent_limit` (máx. 3 PPGs permanentes).
* **Responsabilidade Técnica:** Versionamento dinâmico de regulamentos, operação do livro-razão imutável de integralização de créditos (diferenciando disciplinas internas, intra-IES, quarentena de aluno especial, especiais incorporadas e extra-IES), automação de matrículas compulsórias de acompanhamento de pesquisa, trava de carga inicial de calouros, fluxo de aproveitamento e incorporação formal de créditos cursados como especial via CPG com controle decadencial de 36 meses, fluxo de ajuste manual retroativo com selo de auditoria append-only, e gestão de pautas/atas QWeb da CPG com registro auditável de User ID, Timestamp e IP via `op.cpg.approval.log`.

### 2.4. `l10n_br_openeducat_capes_research`

* **Escopo:** Mapeia a estrutura de fomento e atividade de investigação descrita no Módulo 05 da DAV.
* **Modelos Criados/Estendidos:**
  * Modelos Criados: `capes.research.project`, `capes.project.member`.
  * Modelos Nativos Estendidos: `op.faculty` (`project_ids`, `project_count`, `action_view_projects`).
  * Módulos Nativos Odoo Impactados: `project.project` (via `odoo_project_id`).
* **Responsabilidade Técnica:** Estender as capacidades de gerenciamento de projetos nativas do Odoo (`project.project`) para capturar a natureza científica da pesquisa, classificar parcerias interinstitucionais nacionais e estrangeiras (`foreign_ies`, `foreign_country_id`), agências de fomento (`funding_agency`, `funding_process`), e vincular pesquisadores e discentes às entregas operando sob a Taxonomia CRediT (14 papéis padronizados).

### 2.5. `l10n_br_openeducat_capes_thesis`

* **Escopo:** Governa as regras acadêmicas de ritos de passagem intermediários e finais do Módulo 04 da DAV.
* **Modelos Criados/Estendidos:**
  * Modelos Criados: `capes.thesis`, `capes.thesis.committee`.
  * Modelos Nativos Estendidos: `op.student` (`thesis_ids`, `thesis_count`), `op.faculty` (`committee_count`, `action_view_committees`).
* **Responsabilidade Técnica:** Orquestrar o fluxo bipartido (Seminário Geral de Área/Qualificação e Defesa com quórum e composição de PhDs parametrizáveis por regimento via `op.curriculum.committee.rule`), auditar pré-requisitos do Plano de Trabalho homologado e aprovação CEP/CEUA, gerenciar impedimentos éticos e endogenia em comissões julgadoras, registrar cronometria de exposição/arguição (50 min / 40 min), controlar o envio do PDF final corrigido (`final_pdf_file`), conferência pela secretaria (`secretariat_approval`), titulação automática (`capes_status = 'graduated'`), geração do manifesto XML para a Biblioteca Central (`library_manifest_payload`) e averbação do Handle permanente no DSpace (`repository_url`).

### 2.6. `l10n_br_openeducat_capes_ptt`

* **Escopo:** Internaliza a taxonomia e a engenharia de avaliação qualitativa do Grupo de Trabalho de Produção Técnica (GTPT) e Comitê Medicina II da CAPES para programas profissionais.
* **Modelos Criados/Estendidos:**
  * Modelos Criados: `capes.ptt.axis`, `capes.ptt.type`, `capes.ptt.product`, `capes.ptt.evaluation`, `capes.ptt.author`.
  * Modelos Nativos Estendidos: `op.student` (`ptt_ids`, `ptt_count`), `op.faculty` (`ptt_count`, `action_view_faculty_ptts`).
* **Responsabilidade Técnica:** Processar o motor de regras do Qualis Tecnológico, validar de forma eliminatória a aderência institucional de produções intelectuais (`is_adherent`), mapear níveis de Maturidade Tecnológica (TRL 1-9) e computar a média de notas nas 4 dimensões (Impacto 30 pts, Inovação 25 pts, Aplicabilidade 25 pts, Complexidade 20 pts) para estratificação em tempo real (T1 a T5 ou TNC) servindo como pré-requisito de defesa e gerador de créditos APO.

### 2.7. `l10n_br_openeducat_capes_integration`

* **Escopo:** Concentra a inteligência de conectividade e o mapeamento semântico de comunicação externa da DAV Módulo 06.
* **Modelos Criados/Estendidos:** `capes.intellectual.production`.
* **Controllers HTTP e Endpoints RESTful Fonte Prata:**
  * `GET /api/capes/v1/students`: Consulta serializada de discentes (com suporte a filtro `?program_id=...`), sanitizada com Privacy by Design.
  * `GET /api/capes/v1/faculty`: Consulta do corpo docente com histórico do livro-razão de categorias (`category_ledger_ids`).
  * `GET /api/capes/v1/curriculums`: Consulta das matrizes regimentais ativas e regras de disciplinas.
  * `GET /api/capes/v1/projects_and_ptts`: Exportação integrada de projetos científicos e produtos PTTs com estratos consolidados.
* **Responsabilidade Técnica:** Expor controladores RESTful para transmissão de payloads JSON tipados para a rede RICA|PG / Plataforma Sucupira com sanitização de campos privados (Privacy by Design), gerar payloads XML formatados sob o namespace `oai_capes` (`action_generate_oai_payload`) para crosswalk com o DSpace, e manter a guarda centralizada de produções intelectuais.

### 2.8. `l10n_br_openeducat_capes_diploma`

* **Escopo:** Garante a conformidade jurídica de encerramento de percurso e expedição documental de graus acadêmicos em conformidade com o MEC (Portaria nº 70/2025) e suporte à dualidade de emissão física/digital (IPEN/USP).
* **Modelos Criados/Estendidos:**
  * Modelos Criados: `capes.digital.diploma`, `capes.diploma.signature.log`.
  * Modelos Nativos Estendidos: `op.student` (`diploma_ids`, `diploma_count`, `action_print_transcript`).
  * Relatórios QWeb: `action_report_student_transcript_br` (`report_student_transcript_br_document`).
  * Controller Público: `GET /valida-documento?hash=...` (`CapesPublicValidationController`).
* **Responsabilidade Técnica:** Renderizar relatórios QWeb consolidados de históricos escolares oficiais com QR Code e chave de validação pública, compilar o Pacote de Titulação com cálculo do Hash SHA-256 de auto-autenticação, gerar os XMLs estruturados do Diploma Digital e do Dossiê Acadêmico (Portaria MEC nº 70/2025), aplicar envelopes criptográficos XAdES ICP-Brasil com Carimbo de Tempo e gerenciar o livro de registro físico/híbrido para IES registradoras externas (USP para o IPEN).

### 2.9. `l10n_br_openeducat_capes_scholarship`

* **Escopo:** Governa o livro de cotas institucionais de bolsas (CAPES, CNPq, CNEN, FAPs), editais de distribuição de bolsas, processos avaliativos com múltiplos revisores docentes em paralelo e ciclo de vida de concessão sem gestão financeira direta (Portaria CAPES nº 133/2023 e IN CNEN nº 07/2024).
* **Modelos Criados/Estendidos:**
  * Modelos Criados: `capes.scholarship.sponsor`, `capes.scholarship.quota`, `capes.scholarship.rubric`, `capes.scholarship.rubric.item`, `capes.scholarship.edital`, `capes.scholarship.application`, `capes.scholarship.evaluation`, `capes.scholarship.evaluation.line`, `capes.scholarship.assignment`.
  * Modelos Nativos Estendidos: `op.student` (`scholarship_assignment_ids`, `scholarship_application_ids`, `active_scholarship_count`, `has_active_scholarship`, `scholarship_status_badge`), `op.faculty` (`scholarship_evaluation_ids`, `assigned_scholarship_reviews_count`).
* **Responsabilidade Técnica:** Operar o saldo de cotas de bolsas sem desembolso financeiro pela IES; gerenciar editais parametrizados com reserva de cotas (PPI e Ampla Concorrência) e reversão de vagas; viabilizar matriz avaliativa em 4 colunas (Autoavaliação, Revisor 1, Revisor 2 e Consolidação pela CPG) operando em paralelo; aplicar fórmulas lineares e tetos dinâmicos sem hardcode regimental; verificar limites regulamentares de acúmulo temporal (24m ME / 48m DO) e regras de vínculo empregatício sob deliberação da CPG; gerar termos de compromisso digital e auditar frequências e relatórios anuais.

## 3. Matriz de Dependências e Manifestos do Odoo (`__manifest__.py`)

Para assegurar a integridade do monorepo e a correta carga de dados no banco relacional PostgreSQL, a árvore de dependências do Odoo é rigorosamente respeitada. Cada submódulo possui um arquivo descriptor `__manifest__.py` indicando suas dependências obrigatórias de inicialização:

```text
[openeducat_core]
^
|
[l10n_br_openeducat_capes_core] <-----------------------------------------------------+
^                     ^                                                        |
|                     |                                                        |
|                     +───────────────────────────────┐                        |
|                                                     │                        |
[l10n_br_openeducat_capes_academic] (+ mail) <────────┼──────────┐             |
^          ^                     ^                    │          │             |
|          |                     │                    │          │             |
|          |         [l10n_br_openeducat_capes_admission]       │             |
|          |                     ^                    ^          │             |
|          |                     │                    │          │             |
[l10n_br_openeducat_capes_research] (+ project)       │          │             |
^                                │                    │          │             |
|                                │                    │          │             |
+────────────────────────────────┴────────────────────┼──────────┤             |
                                                      │          │             |
[l10n_br_openeducat_capes_thesis] ────────────────────┘          │             |
^                                ^                               │             |
|                                │                               │             |
[l10n_br_openeducat_capes_ptt] ──+                               │             |
^                                                                │             |
|                                                                │             |
[l10n_br_openeducat_capes_diploma] ──────────────────────────────┘             |
^                                                                              |
|                                                                              |
[l10n_br_openeducat_capes_integration] (core + ptt)                            |
^                                                                              |
|                                                                              |
[l10n_br_openeducat_capes_scholarship] (core + academic + admission + mail) ───+

```

Abaixo está a especificação exata das chaves `depends` presentes em cada manifesto de domínio:

| Submódulo Odoo | Módulos Obrigatórios em `depends` | Tipo de Dependência |
| --- | --- | --- |
| `l10n_br_openeducat_capes_core` | `['openeducat_core']` | Extensão Base de Infraestrutura e PIDs |
| `l10n_br_openeducat_capes_academic` | `['l10n_br_openeducat_capes_core', 'mail']` | Motor Curricular, Regimentos, Livro-Razão e CPG |
| `l10n_br_openeducat_capes_admission` | `['l10n_br_openeducat_capes_core', 'l10n_br_openeducat_capes_academic']` | Editais de Ingresso, Cotas e Planos de Trabalho |
| `l10n_br_openeducat_capes_research` | `['l10n_br_openeducat_capes_academic', 'project']` | Integração Odoo Projects, Fomento e CRediT |
| `l10n_br_openeducat_capes_thesis` | `['l10n_br_openeducat_capes_academic', 'l10n_br_openeducat_capes_admission', 'l10n_br_openeducat_capes_research']` | Ritos Bipartidos, Qualificação e Defesa |
| `l10n_br_openeducat_capes_ptt` | `['l10n_br_openeducat_capes_core', 'l10n_br_openeducat_capes_academic', 'l10n_br_openeducat_capes_thesis']` | Qualis Tecnológico, Eixos GTPT e Trava PTT |
| `l10n_br_openeducat_capes_diploma` | `['l10n_br_openeducat_capes_core', 'l10n_br_openeducat_capes_academic', 'l10n_br_openeducat_capes_thesis']` | Histórico Consolidado, Diploma Digital MEC 70/2025 e Validação Pública |
| `l10n_br_openeducat_capes_integration` | `['l10n_br_openeducat_capes_core', 'l10n_br_openeducat_capes_ptt']` | Barramento RESTful (/api/capes/v1/) e Crosswalk DSpace |
| `l10n_br_openeducat_capes_scholarship` | `['l10n_br_openeducat_capes_core', 'l10n_br_openeducat_capes_academic', 'l10n_br_openeducat_capes_admission', 'mail']` | Gestão de Cotas, Baremas Parametrizados e Termos de Bolsas |

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
