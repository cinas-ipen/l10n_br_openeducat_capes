# Dicionário de Dados DAV: Módulo 02 - Pessoas, Papéis Acadêmicos e Governança CPG

**Objetivo:** Mapear a herança biográfica, as extensões de papéis acadêmicos, os status de proficiência linguística, a timeline de credenciamento docente e a infraestrutura de governança colegiada (CPG) baseadas no JSON da CAPES e no GoPG.

## 1. Classe Base: Pessoa (`res.partner`)

| Campo Odoo | Metadado JSON DAV | Tipo de Dado Odoo | Domínio / Validação JSON |
| --- | --- | --- | --- |
| `capes_id` | Identificador na Capes | `Integer` | Numérico. |
| `internal_code` | Identificador na Instituição | `Char` | Alfanumérico. |
| `name` | Nome da pessoa | `Char` | Texto livre (inclui nome social). |
| `fiscal_name` | Nome fiscal da pessoa | `Char` | Texto exato Receita Federal. |
| `cpf` | Número do CPF | `Char` | Numérico (Receita Federal). |
| `mother_name` | Nome da mãe | `Char` | Texto livre. |
| `birth_date` | Data de nascimento | `Date` | AAAA-MM-DD. |
| `gender` | Sexo biológico | `Selection` | Feminino, Masculino, Intersexo, Não declarado. |
| `race_color` | Raça/Cor | `Selection` | Branca, Preta, Parda, Amarela, Indígena, Não declarada. |
| `has_disability` | Pessoa com deficiência | `Boolean` | Sim; Não. |
| `nationality` | Nacionalidade | `Char` | Texto livre. |
| `birth_country` | País de nascimento | `Many2one` | Tabela IBGE. |
| `birth_state` | UF do nascimento | `Selection` | AL, AP, AM, BA... |
| `birth_city` | Município do nascimento | `Many2one` | Tabela IBGE. |
| `email` | Endereço de e-mail | `Char` | Texto livre. |
| `social_url` | URL da Rede Social | `Char` | Alfanumérico. |
| `is_internal` | Pertence ao Quadro da IES | `Boolean` | Computado. Utilizado nas travas de bancas. |

### 1.1. Identificadores (PIDs) e Formação

| Campo Odoo | Metadado JSON DAV | Tipo de Dado Odoo | Domínio / Validação JSON |
| --- | --- | --- | --- |
| `orcid` | Identificador ORCiD | `Char` | Alfanumérico. Obrigatório para GoPG. |
| `lattes_url` | Identificador Lattes | `Char` | Alfanumérico. Obrigatório para GoPG. |
| `researcher_id` | Identificador ResearcherID | `Char` | Alfanumérico. |
| `scopus_id` | Scopus Author ID | `Char` | Numérico. |
| `academic_level` | Nível acadêmico | `Selection` | Ens. Fundamental, Médio, Graduação, Pós. |
| `highest_degree` | Grau acadêmico | `Selection` | Bacharelado, Especialização, Mestrado, Doutorado. |

## 2. Docente (`op.faculty`) e Timeline de Credenciamento GoPG

### 2.1. Cadastro do Docente

| Campo Odoo | Metadado JSON DAV | Tipo de Dado Odoo | Domínio / Validação JSON |
| --- | --- | --- | --- |
| `partner_id` | Vínculo com Pessoa | `Many2one` | FK para `res.partner`. Obrigatório. |
| `work_regime` | Tipo de dedicação | `Selection` | Dedicação exclusiva, Integral, Parcial. |
| `workload` | Carga horária de atuação | `Integer` | Numérico. |
| `status` | Tipo de situação | `Selection` | Ativo, Inativo, Falecido. |
| `is_retired` | Indicação de aposentadoria | `Boolean` | Sim; Não. |
| `degree_area` | Área de Conhec. Titulação | `Many2one` | Tabela CAPES. |
| `degree_level` | Nível acadêmico da titulação | `Selection` | Mestrado, Doutorado. |
| `degree_ies` | IES da titulação | `Char` | Texto livre. |

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

## 3. Discente / Pós-Graduando (`op.student`) e Controle de Proficiência

| Campo Odoo | Metadado JSON DAV | Tipo de Dado Odoo | Domínio / Validação JSON |
| --- | --- | --- | --- |
| `partner_id` | Vínculo com Pessoa | `Many2one` | FK para `res.partner`. |
| `student_category` | Categoria Discente | `Selection` | Regular, Especial / Não-Vinculado. |
| `curriculum_version_id` | Regimento Ativo (Ato Perfeito) | `Many2one` | FK para `op.curriculum.version`. Obrigatório. |
| `status` | Situacao do Discente | `Selection` | Matriculado, Abandono, Desligado, pending_dismissal, Titulado, Falecido. |
| `admission_date` | Data de ingresso oficial | `Date` | AAAA-MM-DD. Inicia o relógio de 24 meses. |
| `status_date` | Data da situação | `Date` | AAAA-MM-DD. |
| `advisor_id` | Orientador Principal | `Many2one` | FK para `op.faculty`. |
| `coadvisor_id` | Coorientador | `Many2one` | FK para `op.faculty`. |
| `english_proficiency_status` | Status Proficiência Inglês | `Selection` | `pending` (Pendente), `approved` (Aprovado), `exempt` (Isento). Trava de matrícula/qualificação. |
| `portuguese_proficiency_status` | Status Proficiência Português | `Selection` | `not_applicable` (N/A), `pending` (Pendente), `approved` (Aprovado). Exigido para estrangeiros. |

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

| Campo Odoo | Descrição da Entidade | Tipo de Dado Odoo | Domínio / Validação |
| --- | --- | --- | --- |
| `name` | Identificação da Gestão | `Char` | Ex: "Gestão CPG 2024-2027". |
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

| Campo Odoo | Descrição | Tipo de Dado Odoo | Domínio / Validação |
| --- | --- | --- | --- |
| `name` | Número/Ano da Reunião | `Char` | Ex: "3ª Reunião Ordinária CPG/2026". |
| `committee_id` | Composição CPG Responsável | `Many2one` | FK para `op.cpg.committee`. |
| `meeting_date` | Data da Reunião | `Datetime` | Data e Horário. |
| `meeting_type` | Tipo de Reunião | `Selection` | Ordinária, Extraordinária. |
| `state` | Estado do Workflow | `Selection` | Rascunho, Pauta_Aberta, Em_Aprovação, Publicada, Cancelada. |
| `agenda_request_ids` | Requerimentos Pautados | `One2many` | Requerimentos da esteira vindos do Portal. |
| `minutes_pdf` | PDF da Ata Gerado (QWeb) | `Binary` | Documento final da Ata. |
| `approval_log_ids` | Cliques Auditáveis de Aprovação | `One2many` | Registro de User_ID, Timestamp e IP dos votantes. |

### 6. Perfil Profissional e Declaração de Impacto (Baseline de Egressos - CAPES)

**Objetivo:** Capturar a linha de base (*baseline*) profissional do discente no momento do ingresso, atendendo às exigências da CAPES para avaliação do impacto da titulação na carreira, especialmente em Mestrados Profissionais.

| Campo Odoo | Descrição / Regra de Negócio | Tipo de Dado Odoo | Domínio / Opções / Validação |
| --- | --- | --- | --- |
| `student_id` | Vínculo com o Discente | `Many2one` | FK para `op.student`. Obrigatório. |
| `company_name` | Nome da Empresa / Empregador | `Char` | Nome empresarial da organização empregadora. Obrigatório. |
| `company_city` | Cidade da Empresa | `Char` | Município da sede/filial onde o aluno atua. |
| `company_sector` | Setor de Atuação da Empresa | `Selection` | `tech` (Tecnologia, Inovação e P&D), `health` (Saúde e Biotecnologia), `industry` (Indústria e Manufatura), `gov` (Setor Público / Órgão Regulador), `education` (Educação e Pesquisa), `services` (Serviços Especializados). |
| `company_size` | Porte da Empresa (Funcionários) | `Selection` | `micro` (Até 19), `small` (20 a 99), `medium` (100 a 499), `large` (500 a 999), `enterprise` (Mais de 1.000). |
| `current_role` | Cargo / Função Atual | `Char` | Cargo ou função exercida na organização. Obrigatório. |
| `professional_area` | Área de Atuação Específica | `Char` | Departamento ou área técnica de lotação na empresa. |
| `mp_alignment` | Alinhamento com o Mestrado Prof. | `Selection` | `yes` (Sim, alinhamento estratégico direto), `partial` (Parcialmente alinhado), `no` (Não alinhado / Transição). |
| `tenure_range` | Tempo na Empresa | `Selection` | `lt_1` (Menos de 1 ano), `1_3` (1 a 3 anos), `3_5` (3 a 5 anos), `gt_5` (Mais de 5 anos). |
| `salary_range` | Faixa Salarial Atual | `Selection` | `r1` (Até 5 salários mín.), `r2` (5 a 10), `r3` (10 a 15), `r4` (15 a 20), `r5` (Acima de 20). *Protegido por sigilo estatístico.* |
| `capes_terms_accepted` | Aceite Termos CAPES e Programa | `Boolean` | **Obrigatório (`True`)**: Concordância com o compartilhamento de dados estatísticos anonimizados para a CAPES. |
| `acceptance_timestamp` | Data e Hora do Aceite Digital | `Datetime` | Carimbo de tempo e IP gerados automaticamente na submissão. |
