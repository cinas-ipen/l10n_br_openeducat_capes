# Dicionário de Dados DAV: Módulo 02 - Pessoas, Papéis Acadêmicos, Visões 360°, Governança CPG e Perfis de Acesso

**Objetivo:** Mapear a herança biográfica, as extensões de papéis acadêmicos, a higienização onomástica brasileira (`_parse_brazilian_name`), as visões integradas 360° de discentes e docentes, os status de proficiência linguística, a timeline de credenciamento docente, a infraestrutura de governança colegiada (CPG) e a matriz de perfis de usuários com base no JSON da CAPES, no GoPG e no Odoo 19.

## 1. Classe Base: Pessoa (`res.partner`) & Censo Demográfico CAPES

A criação ou importação de contatos adota o algoritmo inteligente de parsing onomástico brasileiro (`_parse_brazilian_name`), que divide o nome completo preservando obrigatoriamente `first_name`, `middle_name` e `last_name` sem gerar campos nulos na presença de sobrenomes múltiplos, garantindo ainda a unicidade nominal estrita de 100% dos registros.

| Campo Odoo | Metadado JSON DAV | Tipo de Dado Odoo | Domínio / Validação JSON |
| --- | --- | --- | --- |
| `capes_id` | Identificador na Capes | `Integer` | Numérico. |
| `internal_code` | Identificador na Instituição | `Char` | Alfanumérico. |
| `name` | Nome da pessoa | `Char` | Texto livre (inclui nome social). |
| `first_name` | Primeiro Nome | `Char` | Derivado pelo algoritmo onomástico. |
| `middle_name` | Nome do Meio | `Char` | Preenchido com sobrenomes intermediários. |
| `last_name` | Sobrenome Final | `Char` | Sobrenome de família final. |
| `fiscal_name` | Nome fiscal da pessoa | `Char` | Texto exato Receita Federal. |
| `cpf` | Número do CPF | `Char` | Numérico (Receita Federal, validação Módulo 11). |
| `mother_name` | Nome da mãe (Filiação) | `Char` | Texto livre. Mandatório para Censo/MEC. |
| `birth_date` | Data de nascimento | `Date` | AAAA-MM-DD. |
| `gender` | Sexo biológico | `Selection` | `male` (Masculino), `female` (Feminino), `other` (Outro). |
| `race_color` | Raça/Cor | `Selection` | `white` (Branca), `black` (Preta), `brown` (Parda), `yellow` (Amarela), `indigenous` (Indígena), `not_declared` (Não declarada). |
| `has_disability` | Pessoa com deficiência (PCD) | `Boolean` | Sim (`True`); Não (`False`). |
| `nationality` | Nacionalidade | `Many2one` | FK para `res.country` (Ex: `base.br`). |
| `birth_country_id` | País de nascimento | `Many2one` | FK para `res.country`. |
| `birth_state` | UF do nascimento | `Selection` | AL, AP, AM, BA, CE, DF, ES, GO, MA, MT, MS, MG, PA, PB, PR, PE, PI, RJ, RN, RS, RO, RR, SC, SP, SE, TO. |
| `birth_city_name` | Município do nascimento | `Char` | Nome oficial do município de nascimento. |
| `email` | Endereço de e-mail | `Char` | Texto livre com formato de e-mail válido. |
| `social_url` | URL da Rede Social | `Char` | Alfanumérico. |
| `is_internal` | Pertence ao Quadro da IES | `Boolean` | Computado. Utilizado nas travas de bancas. |

### 1.1. Identificadores Persistentes (PIDs) e Formação

| Campo Odoo | Metadado JSON DAV | Tipo de Dado Odoo | Domínio / Validação JSON |
| --- | --- | --- | --- |
| `orcid` | Identificador ORCiD | `Char` | Formato `0000-0000-0000-0000`. Obrigatório GoPG. |
| `lattes_url` | Identificador Lattes | `Char` | Link canônico ou ID de 16 dígitos. Obrigatório GoPG. |
| `researcher_id` | Identificador ResearcherID | `Char` | Alfanumérico. |
| `scopus_id` | Scopus Author ID | `Char` | Numérico. |
| `academic_level` | Nível acadêmico | `Selection` | `elem` (Fundamental), `sec` (Médio), `grad` (Graduação), `post` (Pós-Graduação). |
| `highest_degree` | Grau acadêmico máximo | `Selection` | `bachelor` (Bacharelado/Licenciatura), `spec` (Especialização), `master` (Mestrado), `phd` (Doutorado). |

## 2. Docente (`op.faculty`), Visão 360° e Timeline GoPG

### 2.1. Cadastro e Visão 360° do Docente
A ficha do docente centraliza todas as interações e indicadores acadêmicos por meio de smart buttons e campos computados dinâmicos:

| Campo / Smart Button | Descrição / Regra de Negócio | Tipo de Dado Odoo | Domínio / Origem |
| --- | --- | --- | --- |
| `partner_id` | Vínculo com Pessoa Física | `Many2one` | FK para `res.partner`. Obrigatório. |
| `work_regime` | Regime de dedicação | `Selection` | Dedicação exclusiva, Integral, Parcial. |
| `workload` | Carga horária de atuação | `Integer` | Horas semanais. |
| `status` | Situação funcional | `Selection` | Ativo, Inativo, Falecido. |
| `is_retired` | Indicação de aposentadoria | `Boolean` | Sim; Não. |
| `degree_area` | Área de Conhec. Titulação | `Many2one` | Tabela CAPES. |
| `degree_level` | Nível acadêmico da titulação | `Selection` | Mestrado, Doutorado. |
| `degree_ies` | IES da titulação | `Char` | Texto livre (Ex: "Universidade de São Paulo"). |
| `advisees_count` *(Smart Button)* | Orientandos Ativos | `Integer` | Computado de `op.student` com status ativo. |
| `alumni_count` *(Smart Button)* | Orientandos Egressos / Titulados | `Integer` | Computado de `op.student` com categoria `alumni`. |
| `courses_count` *(Smart Button)* | Disciplinas Lecionadas | `Integer` | Computado de turmas/disciplinas sob responsabilidade do docente. |
| `research_lines_count` *(Smart Button)*| Linhas de Pesquisa Ativas | `Integer` | Computado de `research_line_ids`. |
| `theses_committee_count` *(Smart Button)*| Bancas Examinadoras | `Integer` | Computado de comissões julgadoras em `capes.thesis`. |
| `research_line_ids` | Linhas de Pesquisa Vinculadas | `Many2many` | Relação com `op.program.research.line`. |

### 2.2. Vínculo com Programa (`op.faculty.program.link`)

| Campo Odoo | Descrição / Regra GoPG | Tipo de Dado Odoo | Domínio / Validação JSON |
| --- | --- | --- | --- |
| `faculty_id` | Docente | `Many2one` | FK para `op.faculty`. |
| `program_id` | Programa de Pós-Graduação | `Many2one` | FK para `op.program.capes`. |
| `active_advisees_count` | Número Orientandos Ativos | `Integer` | Computado. Trava teto (ex: máx 8 no IPEN). |

### 2.3. Livro-Razão de Categorias Docentes (`op.faculty.category.ledger`)

*Estrutura Append-Only para o "filme" de credenciamento exigido pela CAPES.*

| Campo Odoo | Metadado JSON DAV / GoPG | Tipo de Dado Odoo | Domínio / Validação JSON |
| --- | --- | --- | --- |
| `program_link_id` | Vínculo Docente-Programa | `Many2one` | FK para `op.faculty.program.link`. |
| `category` | Categoria de Atuação | `Selection` | Permanente, Colaborador, Visitante, Assistente. |
| `start_date` | Início do Credenciamento | `Date` | AAAA-MM-DD. Obrigatório. |
| `end_date` | Fim do Credenciamento | `Date` | AAAA-MM-DD (Validade máx 2 anos no IPEN). |
| `document_ref` | Portaria / Ata da CPG | `Char` | Referência formal do ato de credenciamento. |

## 3. Discente / Pós-Graduando (`op.student`), Visão 360° e Vínculos

A entidade `op.student` representa a Pessoa Acadêmica Soberana perante a IES (`res.company`), possuindo Registro Acadêmico (RA) único e perene ancorado no CPF.

### 3.1. Visão 360° do Discente na Ficha Cadastral
A partir do formulário do discente, a secretaria e a coordenação possuem visão global e imediata de toda a vida acadêmica:
* **Ação no Cabeçalho (*Header Action*):** Botão **"Imprimir Histórico Escolar"**, gerando o Histórico Oficial em QWeb PDF instantaneamente.
* **Smart Buttons Integrados:**
  * **Vínculos de Curso** (`course_count`): Total de percursos do discente (`op.student.course`).
  * **Livro-Razão** (`credit_ledger_count`): Acesso rápido aos lançamentos de créditos.
  * **Trabalhos Finais / Defesas** (`thesis_count`): Ritos de Qualificação e Defesa (`capes.thesis`).
  * **Produtos PTT** (`ptt_count`): Acervo de produção técnica tecnológica do aluno (`capes.ptt.product`).
  * **Requerimentos** (`request_count`): Processos acadêmicos autuados (`op.academic.request`).
  * **Diplomas Digitais** (`diploma_count`): Dossiês de diplomação vinculados (`op.student.transcript.br`).
* **Aba Integrada de Livro-Razão:** O notebook da ficha exibe a tabela completa de lançamentos com colunas para Disciplina, Natureza do Crédito, Créditos, Horas, Conceito Final, Data e Situação de Aprovação.

| Campo Odoo | Metadado JSON DAV | Tipo de Dado Odoo | Domínio / Validação JSON |
| --- | --- | --- | --- |
| `student_id` | Registro Acadêmico (RA) | `Char` | Alfanumérico. **Imutável e Único por CPF e IES (`res.company`)**. |
| `partner_id` | Vínculo com Pessoa Física | `Many2one` | FK para `res.partner` (âncora soberana por CPF). Obrigatório. |
| `company_id` | Instituição de Ensino (IES) | `Many2one` | FK para `res.company`. Escopo de governança institucional. |
| `student_category` | Categoria Discente Atual | `Selection` | `regular` (Regular), `special` (Especial / Não-Vinculado), `alumni` (Egresso/Titulado). |
| `curriculum_version_id` | Regimento Ativo (Ato Perfeito) | `Many2one` | FK para `op.curriculum.version` do vínculo acadêmico principal ativo. |
| `course_detail_ids` | Histórico de Vínculos/Cursos | `One2many` | Relação com `op.student.course` (Múltiplos Vínculos Acadêmicos - Opção B). |
| `status` | Situação do Discente | `Selection` | Matriculado, Abandono, Desligado, pending_dismissal, Titulado, Falecido. |
| `admission_date` | Data de ingresso oficial | `Date` | AAAA-MM-DD. Inicia o relógio de prazos do curso regular. |
| `status_date` | Data da situação | `Date` | AAAA-MM-DD. |
| `advisor_id` | Orientador Principal | `Many2one` | FK para `op.faculty` (aplicável a alunos regulares). |
| `coadvisor_id` | Coorientador | `Many2one` | FK para `op.faculty`. |
| `english_proficiency_status` | Status Proficiência Inglês | `Selection` | `pending` (Pendente), `approved` (Aprovado), `exempt` (Isento). Trava de matrícula/qualificação. |
| `portuguese_proficiency_status` | Status Proficiência Português | `Selection` | `not_applicable` (N/A), `pending` (Pendente), `approved` (Aprovado). Exigido para estrangeiros. |

### 3.2. Entidade de Vínculo Acadêmico (`op.student.course`)
* **Campos Principais:** `student_id`, `course_id`, `batch_id` (Turma / Lote de Ingresso), `curriculum_version_id`, `course_type` (`regular` / `special`), `state` (`running`, `finished`, `canceled`), `admission_date`, `completion_date`.

## 4. Gestão de Afastamentos (`capes.leave_of_absence`)

| Campo Odoo | Metadado JSON DAV | Tipo de Dado Odoo | Domínio / Validação JSON |
| --- | --- | --- | --- |
| `student_id` | Discente Afastado | `Many2one` | FK para `op.student`. |
| `faculty_id` | Docente Afastado | `Many2one` | FK para `op.faculty`. |
| `leave_type` | Tipo de afastamento | `Selection` | Saúde própria, Doença família, Maternidade, Paternidade, Serviço Militar. |
| `cid_code` | Código CID Médico | `Char` | Obrigatório se motivo de saúde. |
| `start_date` | Data início afastamento | `Date` | AAAA-MM-DD. |
| `end_date` | Data encerramento | `Date` | AAAA-MM-DD. Trava de teto de 365 dias. |
| `attachment_ids` | Atestados / Comprovantes | `Many2many` | Documentos em PDF anexados ao chamado. |

## 5. Governança do Colegiado CPG (Macroprocesso 10)

### 5.1. Composição do Conselho (`op.cpg.committee` e `op.cpg.member`)
A comissão deliberativa colegiada opera sob mandato formal (trienal) com quórum regimental estrito composto por:
* **6 Membros Titulares:**
  1. Coordenador do Programa (Presidente Nato)
  2. Vice-Coordenador do Programa (Vice-Presidente)
  3. Três Docentes Permanentes Titulares
  4. Um Representante Discente Titular
* **4 Membros Suplentes:**
  1. Três Docentes Permanentes Suplentes
  2. Um Representante Discente Suplente

| Campo Odoo | Descrição da Entidade | Tipo de Dado Odoo | Domínio / Validação |
| --- | --- | --- | --- |
| `name` | Identificação da Gestão | `Char` | Ex: "Mandato CPG MPTRCS 2025-2028". |
| `start_date` | Início do Mandato | `Date` | AAAA-MM-DD. |
| `end_date` | Término do Mandato | `Date` | AAAA-MM-DD (Mandato de 3 anos). |
| `status` | Situação da Gestão | `Selection` | Ativa, Encerrada. |

### 5.2. Membros da CPG (`op.cpg.member`)

| Campo Odoo | Descrição | Tipo de Dado Odoo | Domínio / Validação |
| --- | --- | --- | --- |
| `committee_id` | Gestão CPG | `Many2one` | FK para `op.cpg.committee`. |
| `partner_id` | Membro da CPG | `Many2one` | FK para `res.partner`. |
| `role` | Cargo na Mesa / Conselho | `Selection` | Coordenador, Vice-Coordenador, Titular, Suplente, Repres. Discente. |
| `mandate_origin` | Origem do Mandato | `Selection` | Eleito pelos Pares, Indicado Reitoria/Conselho, Eleição Discente. |
| `document_ref` | Número da Portaria / Ata | `Char` | Documento de indicação/eleição. |

### 5.3. Reuniões e Deliberações da CPG (`op.cpg.meeting`)
O sistema gerencia o calendário mensal de reuniões ordinárias da CPG, controlando o fluxo pauta-aberta $\rightarrow$ em-aprovação $\rightarrow$ publicada:
* **Atas QWeb PDF (`minutes_pdf`):** Compilação automática das deliberações com histórico de pauta.
* **Assinatura Eletrônica por Clique Auditável (`op.cpg.approval.log`):** Cada homologação registra de forma imutável o `user_id`, `timestamp`, `action` ("Aprovação da Ata") e `ip_address` do votante.
* **Deliberação de Processos (`agenda_request_ids`):** Requerimentos acadêmicos pautados e resolvidos diretamente em sessão colegiada.

## 6. Perfil Profissional e Declaração de Impacto (Baseline de Egressos - CAPES)

**Objetivo:** Capturar a linha de base (*baseline*) profissional do discente no momento do ingresso, atendendo às exigências da CAPES para avaliação do impacto da titulação na carreira, especialmente em Mestrados Profissionais.

| Campo Odoo | Descrição / Regra de Negócio | Tipo de Dado Odoo | Domínio / Opções / Validação |
| --- | --- | --- | --- |
| `student_id` | Vínculo com o Discente | `Many2one` | FK para `op.student`. Obrigatório. |
| `company_name` | Nome da Empresa / Empregador | `Char` | Nome empresarial da organização empregadora. Obrigatório. |
| `company_city` | Cidade da Empresa | `Char` | Município da sede/filial onde o aluno atua. |
| `company_sector` | Setor de Atuação da Empresa | `Selection` | `tech`, `health`, `industry`, `gov`, `education`, `services`. |
| `company_size` | Porte da Empresa (Funcionários) | `Selection` | `micro`, `small`, `medium`, `large`, `enterprise`. |
| `current_role` | Cargo / Função Atual | `Char` | Cargo ou função exercida na organização. Obrigatório. |
| `professional_area` | Área de Atuação Específica | `Char` | Departamento ou área técnica de lotação na empresa. |
| `mp_alignment` | Alinhamento com o Mestrado Prof. | `Selection` | `yes`, `partial`, `no`. |
| `tenure_range` | Tempo na Empresa | `Selection` | `lt_1`, `1_3`, `3_5`, `gt_5`. |
| `salary_range` | Faixa Salarial Atual | `Selection` | `r1` a `r5`. *Protegido por sigilo estatístico.* |
| `capes_terms_accepted` | Aceite Termos CAPES e Programa | `Boolean` | **Obrigatório (`True`)**. |
| `acceptance_timestamp` | Data e Hora do Aceite Digital | `Datetime` | Carimbo de tempo e IP gerados na submissão. |

## 7. Perfis de Usuários e Controle de Acesso no Odoo 19 (`res.users`)

Para operação do sistema em ambientes de produção e homologação, os seguintes perfis e privilégios são configurados:

| Login | Papel Institucional | Grupo de Segurança Odoo 19 | Vínculo de Domínio | Atribuições Principais |
| --- | --- | --- | --- | --- |
| `admin` | Administrador de TI / Sistema | `base.group_system`, `group_op_back_office_admin` | - | Configuração de módulos, parametrizações globais e auditoria do stack. |
| `secretaria` | Secretaria de Pós-Graduação | `openeducat_core.group_op_back_office_admin` | Secretaria do PPG | Cadastros discentes, matrículas, lançamentos de créditos, emissão de históricos e diplomas. |
| `coordenador` | Coordenador do PPG | `openeducat_core.group_op_back_office_admin` | FK Docente Coordenador + CPG | Presidência da CPG, homologação de bancas, acompanhamento de prazos e deliberações. |
| `vicecoordenador` | Vice-Coordenador do PPG | `openeducat_core.group_op_back_office_admin` | FK Docente Vice-Coord. + CPG | Substituição da coordenação e deliberações na CPG. |
| `professor` | Docente e Orientador | `openeducat_core.group_op_faculty` | FK `op.faculty` | Diário de classe, notas, pareceres sobre planos de trabalho e requerimentos de orientandos. |

