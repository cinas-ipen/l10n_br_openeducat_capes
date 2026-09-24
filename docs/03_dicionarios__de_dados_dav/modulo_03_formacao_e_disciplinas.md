# Dicionário de Dados DAV: Módulo 03 - Formação, Disciplinas e Turmas

**Objetivo:** Mapear o catálogo de disciplinas, ofertas e instâncias de turmas baseadas no JSON DAV.

## 1. Disciplina (`op.subject`)
| Campo Odoo | Metadado JSON DAV | Tipo de Dado Odoo | Domínio / Validação JSON |
| :--- | :--- | :--- | :--- |
| `id` | Identificador da disciplina | `Integer` | Numérico (PK Odoo / CAPES). |
| `code` | Código da disciplina no PPG | `Char` | Alfanumérico. |
| `name` | Nome da disciplina | `Char` | Texto livre. |
| `syllabus` | Ementa da disciplina | `Text` | Texto explicativo. |
| `basic_bibliography` | Bibliografia Básica | `Text` | Referências essenciais. |
| `complementary_bibliography` | Bibliografia Complementar | `Text` | Referências complementares. |
| `phea_indicator` | Processos Híbridos (PHEA) | `Boolean` | Sim; Não. |
| `teaching_language` | Idioma de Oferta | `Selection` | Português (`pt`), Inglês (`en`), Espanhol (`es`), Outro (`other`). |
| `grade_weightage` | Carga horária / Peso da disciplina | `Float` | Numérico. |
| `credits` | Créditos da Disciplina | `Float` | Numérico (campo armazenado relacionado a `grade_weightage`). |
| `type` | Natureza didática | `Selection` | Teórica (`theory`), Prática (`practical`), Teórico-Prática (`both`). |
| `subject_type` | Indicador de obrigatoriedade | `Selection` | Obrigatória (`compulsory`), Eletiva (`elective`). |
| `program_id` | Programa Ofertante | `Many2one` | FK para `op.program.capes`. |
| `allow_special_students` | Permite Alunos Especiais | `Boolean` | Sim; Não. Configuração por disciplina. |
| `special_student_instructor_consent_required` | Exige Anuência do Docente | `Boolean` | Sim; Não. Bloqueia matrícula sem aceite do professor. |
| `special_seats_quota` | Cota de Vagas Alunos Especiais | `Integer` | Limite numérico de vagas avulsas na disciplina. |
| `active` | Situação de atividade no catálogo | `Boolean` | Ativo / Inativo. |

## 2. Turma (`op.batch` / `op.session`)
| Campo Odoo | Metadado JSON DAV | Tipo de Dado Odoo | Domínio / Validação JSON |
| :--- | :--- | :--- | :--- |
| `capes_id` | Identificador da turma | `Integer` | Numérico. |
| `batch_code` | Código da turma | `Char` | Alfanumérico. |
| `academic_year` | Ano de oferta da turma | `Integer` | AAAA. |
| `academic_term` | Período letivo da turma | `Selection` | 1°, 2°, 3°, 4°, 5°, 6°. |
| `language` | Idioma da turma | `Selection` | Tabela Idiomas Capes. |
| `phea_indicator`| Utilização de PHEA (Híbrido)| `Boolean` | Sim; Não. |
| `allow_special_students` | Admite Aluno Especial na Oferta | `Boolean` | Herda da disciplina ou ajusta por turma. |
| `special_seats_quota` | Cota Máxima de Alunos Especiais | `Integer` | Teto de matriculados em regime especial na turma. |
| `prog_content` | Conteúdo Programático | `Text` | Temas e unidades de estudo. |
| `complem_biblio`| Bibliografia Complementar | `Text` | Obras adicionais. |

### 2.1 Ministrantes da Turma
| Campo Odoo | Metadado JSON DAV | Tipo de Dado Odoo | Domínio / Validação JSON |
| :--- | :--- | :--- | :--- |
| `faculty_id` | Ministrante da turma | `Many2one` | Docente vinculado. |
| `is_responsible`| Responsável pela turma | `Boolean` | Sim; Não. |

## 3. Requerimento de Aproveitamento de Créditos de Aluno Especial (`op.special.credit.incorporation.request`)
Entidade de workflow para homologação de disciplinas cursadas em regime especial e sua transferência do estado de quarentena para o histórico regular do discente.

| Campo Odoo | Descrição da Regra | Tipo de Dado Odoo | Validação / Regra de Negócio |
| :--- | :--- | :--- | :--- |
| `student_id` | Discente Requerente | `Many2one` | FK para `op.student`. |
| `target_program_id` | Programa de Destino (Regular) | `Many2one` | FK para `op.program.capes` (ex: MPTRCS). |
| `target_curriculum_version_id` | Versão Curricular Ativa | `Many2one` | FK para `op.curriculum.version`. |
| `quarantine_ledger_ids` | Disciplinas Selecionadas | `Many2many` | Filtro estrito: apenas linhas de `credit_type = 'subject_special_quarantine'`. |
| `state` | Estado do Workflow | `Selection` | `draft` (Rascunho), `submitted` (Submetido), `advisor_approved` (Parecer Orientador), `cpg_approved` (Deferido CPG), `rejected` (Indeferido). |
| `is_within_validity` | Verificação de Prazo Decadencial | `Boolean` | Computado. Trava: data de conclusão da disciplina $\le$ 36 meses da admissão regular. |
| `is_within_subject_limit` | Verificação do Teto de Disciplinas | `Boolean` | Computado. Trava: total de disciplinas $\le$ `max_special_subjects_limit`. |
| `cpg_resolution_number` | Número do Ato / Resolução CPG | `Char` | Obrigatório para transição ao estado `cpg_approved`. |
| `cpg_resolution_date` | Data da Reunião / Deliberação | `Date` | Data oficial de homologação do aproveitamento. |
| `advisor_opinion` | Parecer do Orientador | `Text` | Justificativa de aderência à pesquisa da dissertação. |

## 4. Extensões nos Modelos Nativos do OpenEduCat

### 4.1. Vínculo Acadêmico de Curso (`op.student.course`)
Estendido em `l10n_br_openeducat_capes_academic` para suportar a coexistência de percursos regulares e vínculos de aluno especial sob o mesmo discente soberano:
* `course_type`: `regular` (Curso Regular Stricto Sensu) ou `special` (Aluno Especial - Disciplinas Isoladas).
* `program_id`: Many2one `op.program.capes`, programa CAPES responsável pelo curso.
* `curriculum_version_id`: Many2one `op.curriculum.version`, regimento específico associado a esta matrícula.
* `admission_date`: Date, data de início formal do vínculo.
* `completion_date`: Date, data de encerramento/titulação.

### 4.2. Turmas e Coortes de Ingresso (`op.batch`)
Estendido para ancorar cada turma ao seu respectivo programa de pós-graduação:
* `program_id`: Many2one `op.program.capes`, programa CAPES da turma ofertada.