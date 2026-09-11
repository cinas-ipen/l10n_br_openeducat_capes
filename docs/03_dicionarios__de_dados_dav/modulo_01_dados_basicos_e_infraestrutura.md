# Dicionário de Dados DAV: Módulo 01 - Dados Básicos e Infraestrutura

**Objetivo:** Mapear a ontologia primária (IES, Endereços, Programas, Versionamento Curricular, Regras de Disciplinas, Áreas e Linhas) baseada na extração JSON da CAPES para o esquema relacional do Odoo.

## 1. Instituição de Ensino Superior (IES) e Campus (`res.company` / `res.partner`)

| Campo Odoo | Metadado JSON DAV | Tipo de Dado Odoo | Domínio / Validação JSON |
| --- | --- | --- | --- |
| `name` | Nome da IES / Campus | `Char` | Obrigatório. Texto livre. |
| `name_en` | Nome da IES em inglês | `Char` | Texto livre. |
| `isni_code` | ISNI | `Char` | Validação: [https://isni.org/](https://isni.org/) |
| `ror_id` | Registro de Org. de Pesquisa (ROR) | `Char` | Validação: [https://ror.org/](https://ror.org/) |
| `cnpj` | CNPJ da IES / Campus | `Char` | Numérico. Módulo 11. |
| `capes_code` | Código da IES na Capes | `Char` | Numérico. Fonte Ouro: Cadastro de IES. |
| `emec_code` | Código e-MEC da IES | `Char` | Alfanumérico. Fonte Ouro: E-MEC. |
| `acronym` | Sigla da IES | `Char` | Redução do nome completo. |
| `admin_category` | Categoria administrativa | `Selection` | Pública (Municipal, Estadual, Federal), Privada (com/sem fins lucrativos), Especial. |
| `sub_category` | Sub-categoria (Privadas) | `Selection` | Comunitárias, Confessionais, Filantrópicas. |
| `academic_org` | Organização Acadêmica | `Selection` | Faculdades, Centros Univ., Universidades, IFs, Escola de governo. |
| `pro_rector_name` | Nome do Pró-Reitor de Pós | `Char` | Texto livre. |
| `pro_rector_start` | Início atuação do Pró-Reitor | `Date` | AAAA-MM-DD. |
| `pro_rector_end` | Fim atuação do Pró-Reitor | `Date` | AAAA-MM-DD. |

## 2. Georreferenciamento e Endereço Institucional

| Campo Odoo | Metadado JSON DAV | Tipo de Dado Odoo | Domínio / Validação JSON |
| --- | --- | --- | --- |
| `street` | Logradouro do endereço | `Char` | Texto livre. |
| `street_number` | Número do logradouro | `Char` | Numérico. |
| `street2` | Complemento do endereço | `Char` | Texto livre. |
| `district` | Bairro do endereço | `Char` | Texto livre. |
| `zip` | CEP do endereço | `Char` | Numérico. |
| `city_id` | Município do endereço | `Many2one` | Tabela Municípios IBGE. |
| `state_id` | Unidade Federativa do endereço | `Many2one` | Tabela UFs Brasil. |
| `country_id` | País do endereço | `Many2one` | Tabela Países IBGE. |
| `po_box` | Caixa postal do endereço | `Char` | Numérico. |
| `ibge_code` | Código do município no IBGE | `Char` | 7 dígitos numéricos. |
| `siafi_code` | Código do município no SIAFI | `Char` | Tabela SIAFI. |
| `mesoregion_id` | Identificador da mesorregião | `Char` | Numérico. |
| `microregion_id` | Identificador da microrregião | `Char` | Numérico. |
| `latitude` | Latitude do endereço | `Float` | Graus decimais. |
| `longitude` | Longitude do endereço | `Float` | Graus decimais. |

## 3. Programa de Pós-Graduação (PPG) (`op.program.capes`)

*Nota de Arquitetura:* O modelo `op.program.capes` mantém a identidade cadastral e regulatória fixa do programa perante o SNPG e MEC. As regras dinâmicas e mutáveis de integralização de créditos e prazos são delegadas para a entidade `op.curriculum.version`.

| Campo Odoo | Metadado JSON DAV | Tipo de Dado Odoo | Domínio / Validação JSON |
| --- | --- | --- | --- |
| `capes_id` | Identificador do Programa | `Integer` | Numérico. |
| `snpg_code` | Código do PPG no SNPG | `Char` | Numérico (8+5 dígitos). Obrigatório. |
| `name` | Nome do Programa | `Char` | Tabela Sucupira. |
| `lang` | Idioma do Nome do PPG | `Selection` | Tabela ISO 639. |
| `phone` | Telefone do Programa | `Char` | Numérico. |
| `website` | Site do Programa | `Char` | Texto livre (URL). |
| `modality` | Modalidade do Programa | `Selection` | Acadêmica, Profissional. |
| `teaching_modal` | Modalidade de ensino | `Selection` | Ensino presencial, Ensino a distância. |
| `operation_form` | Forma de atuação | `Selection` | Singular, Assoc. Interinstitucional, Assoc. Intrainstitucional. |
| `ies_role` | Atuação da IES/Campus | `Selection` | Coordenadora, Associada, Nucleadora, Colaboradora. |
| `school_term` | Regime Letivo do Programa | `Selection` | Bimestral, Trimestral, Quadrimestral, Semestral, Anual. |
| `status` | Situação do Programa | `Selection` | Em projeto, Em funcionamento, Em desativação, Desativado, Perda de eficácia, Suspensão. |
| `start_date` | Data de Início do Programa | `Date` | AAAA-MM-DD. |
| `end_date` | Data de Encerramento | `Date` | AAAA-MM-DD. |
| `recommend_date` | Data de recomendação | `Date` | AAAA-MM-DD. |
| `recognize_date` | Data de reconhecimento | `Date` | AAAA-MM-DD. |
| `general_coord` | Coordenador do Programa | `Many2one` | FK para Docente (`op.faculty`). |
| `local_coord` | Coordenador Local do PPG | `Many2one` | FK para Docente (`op.faculty`). |

### 3.1. Áreas de Avaliação e Classificação CAPES

| Campo Odoo | Metadado JSON DAV | Tipo de Dado Odoo | Domínio / Validação JSON |
| --- | --- | --- | --- |
| `evaluation_area` | Código da área de avaliação | `Char` | Tabela de Áreas Capes (Ex: Medicina II). |
| `broad_area` | Cód. grande área (Nível 1) | `Char` | Tabela Capes. |
| `basic_area` | Cód. área básica (Nível 2) | `Char` | Tabela Capes. |
| `subarea` | Cód. subárea (Nível 3) | `Char` | Tabela Capes. |
| `specialty` | Cód. especialidade (Nível 4) | `Char` | Tabela Capes. |
| `capes_grade` | Nota do curso | `Selection` | 1, 2, 3, 4, 5, 6, 7, A. |
| `grade_year` | Ano base atribuição da nota | `Integer` | AAAA. |


## 4. O Versionamento Curricular (`op.curriculum.version`)

*Entidade Centralizadora das Regras Dinâmicas do Curso (Ato Jurídico Perfeito).*

| Campo Odoo | Descrição / Regra de Negócio | Tipo de Dado Odoo | Domínio / Validação JSON |
| --- | --- | --- | --- |
| `name` | Nome da Versão Regimental | `Char` | Ex: "Regimento IPEN 2024", "Regimento CDTN 2026", "Regimento UPM 2024". |
| `program_id` | Programa de Pós-Graduação | `Many2one` | FK para `op.program.capes`. Obrigatório. |
| `max_months_defense` | Prazo Máximo Titulação (meses) | `Integer` | Ex: 24 (Mestrado), 48 (Doutorado). |
| `max_trancamento_days` | Prazo Máximo de Trancamento Contínuo (dias) | `Integer` | Ex: 365 (MPTRCS Art. 22º, §3º). |
| `block_first_semester_trancamento` | Trava Bloqueio Trancamento 1º Semestre | `Boolean` | True ou False (False no MPTRCS, Art. 22º §1º). |
| `retorno_rule` | Regra de Retorno e Estrutura Curricular | `Selection` | current_matrix (Vinculação à matriz vigente no retorno, preservando o Ato Jurídico Perfeito no Ledger). |
| `max_extension_days` | Teto Máximo Prorrogação (dias) | `Integer` | Ex: 90 (IPEN), 180 (CDTN/Mackenzie). |
| `max_days_post_defense_deposit` | Prazo Depósito Final Pós-Defesa (dias) | `Integer` | Ex: 30 dias (IPEN/Mackenzie) vs. 90 dias (CDTN Art. 50). |
| `min_credits` | Créditos Totais Exigidos | `Integer` | Ex: 100 (IPEN), 50/60 (Mackenzie), 24/47 (CDTN). |
| `credit_hour_ratio` | Horas por Unidade de Crédito | `Integer` | Ex: 15 (IPEN/CDTN), 12 (Mackenzie Computação), 10 (Mackenzie ADN). |
| `grading_scale_type` | Escala de Conceitos e Corte | `Selection` | `scale_abc_r` (A,B,C Aprovados; R Reprovado), `scale_abcd_rf` (A,B,C,D Aprovados - CDTN Art. 38/42). |
| `teaching_internship_mode` | Regra de Estágio de Docência (Portaria 221/2025) | `Selection` | `not_applicable` (Cursos Profissionais/Isentos), `scholarship_only` (Apenas Bolsistas), `mandatory_all` (Todos), `flexible_equivalence` (Permite Estágio Supervisionado / Equivalentes). |
| `ptt_validation_mode` | Modo de Validação do PTT | `Selection` | `cpg_checklist` (Checklist + Anuência Orientadores + CPG), `qualis_prior` (Avaliação Qualis Prévia), `none` (Sem PTT). |
| `proficiency_stage` | Momento Exigência Proficiência | `Selection` | `admission` (Na Admissão - IPEN), `qualification` (Na Qualificação), `defense` (Na Defesa). |
| `defense_location_policy` | Política de Presença da Defesa | `Selection` | `onsite_mandatory` (Presencial), `hybrid_allowed` (Presença física aluno/presidente), `fully_remote_allowed` (100% remota autorizada - CDTN Art. 49). |
| `presentation_max_minutes` | Tempo Máximo Exposição (min) | `Integer` | Ex: 50 min (IPEN), 45 min (CDTN Art. 48 §2º). |
| `arguing_max_minutes_per_member` | Tempo Máximo Arguição p/ Membro | `Integer` | Ex: 40 min por examinador. |
| `subject_rule_ids` | Regras de Disciplinas Obrigatórias | `One2many` | Relação com `op.curriculum.subject.rule`. |
| `committee_rule_ids` | Regras de Composição de Bancas | `One2many` | Relação com `op.curriculum.committee.rule`. |
| `is_active` | Versão Vigente para Novas Matrículas | `Boolean` | Utilizada pelos novos Editais de Seleção. |

### 4.1. Regras de Disciplinas Obrigatórias por Currículo (`op.curriculum.subject.rule`)

| Campo Odoo | Descrição / Regra de Negócio | Tipo de Dado Odoo | Domínio / Validação JSON |
| --- | --- | --- | --- |
| `curriculum_version_id` | Versão do Currículo | `Many2one` | FK para `op.curriculum.version`. Mandatory. |
| `subject_id` | Disciplina | `Many2one` | FK para `op.subject`. Mandatory. |
| `scope` | Escopo da Obrigatoriedade | `Selection` | `program` (Geral do Programa), `area` (Específica da Área de Concentração). |
| `area_id` | Área de Concentração | `Many2one` | FK para `capes.area.concentracao`. Exigido se `scope = 'area'`. |

### 4.2. Regras de Composição de Comissões Julgadoras (`op.curriculum.committee.rule`)

| Campo Odoo | Descrição / Regra de Negócio | Tipo de Dado Odoo | Domínio / Validação JSON |
| --- | --- | --- | --- |
| `curriculum_version_id` | Versão do Currículo | `Many2one` | FK para `op.curriculum.version`. Mandatory. |
| `academic_level` | Nível de Formação | `Selection` | `master` (Mestrado), `phd` (Doutorado). |
| `stage` | Rito Acadêmico | `Selection` | `qualification` (Qualificação), `seminar` (Seminário de Área), `defense` (Defesa Final). |
| `min_titular_count` | Mínimo de Examinadores Titulares | `Integer` | Ex: 3 (Mestrado geral), 5 (Doutorado CDTN). |
| `suplente_mode` | Regra de Suplentes | `Selection` | `fixed_pair` (Mínimo 2: 1 int / 1 ext - Mackenzie), `one_per_titular` (1 por titular), `custom` (Quantidade fixa). |
| `advisor_vote_role` | Papel e Voto do Orientador | `Selection` | `voting_president` (Preside e Vota - IPEN/Mackenzie), `non_voting_president` (Preside sem voto - CDTN Art. 44 §4º), `examiner_only` (Membro votante sem presidência). |
| `coadvisor_participation` | Participação do Coorientador | `Selection` | `non_voting_additional` (Membro adicional sem voto), `forbidden_with_advisor` (Proibido se Orientador presente - IPEN Art. 10 §3º), `full_voting_member` (Membro Votante). |
| `external_rule` | Exigência de Membros Externos | `Selection` | `min_one_external` (Mínimo 1 externo ao PPG/IES), `min_two_external` (Mínimo 2 externos - CDTN Doutorado), `majority_external` (Maioria externa ao PPG). |
| `allow_non_phd_member` | Permite Especialista sem Doutorado | `Boolean` | Em Mestrados Profissionais, aceita notória especialização de mercado. |
| `non_phd_approval_level` | Alçada de Aprovação de Não-Doutor | `Selection` | `cpg_simple` (CPG simples), `cpg_qualified` (2/3 da CPG - IPEN Art. 46 §3º), `superior_council` (CPG + Conselho Superior). |
