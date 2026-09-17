# Dicionário de Esqueletos CSV de Importação e Ordem de Carga
## Ecossistema l10n_br_openeducat_capes (Odoo 19.0 / OpenEduCat 19.0)

Este diretório contém os **modelos padronizados de planilhas CSV** para importação oficial de dados em lote no Odoo 19.0.

---

## 1. Ordem Estrita de Carga de Arquivos

Para garantir que todas as Chaves Estrangeiras (*Foreign Keys*) sejam resolvidas sem falhas de integridade referencial, os arquivos devem ser importados rigorosamente na seguinte ordem numérica:

1. `01_ies_instituicao_res_company.csv` (Empresa Mantenedora / IES)
2. `02_programas_capes_op_program.csv` (Programas de Pós-Graduação CAPES — modelo: `op.program.capes`)
3. `03_versao_curricular_op_curriculum_version.csv` (Regimentos Curriculares e Matrizes)
4. `04_areas_concentracao_op_curriculum_subject_rule.csv` (Áreas de Concentração)
5. `05_docentes_orientadores_op_faculty.csv` (Corpo Docente e PIDs)
6. `06_credenciamento_docente_cpg_op_faculty_accreditation.csv` (Credenciamento na CPG)
7. `07_disciplinas_catalogo_op_subject.csv` (Catálogo de Disciplinas e PHEA)
8. `08_editais_selecao_op_admission_edital.csv` (Editais de Admissão por Turma)
9. `09_discentes_identidade_op_student.csv` (Identidade Soberana Discente e RA Perene)
10. `10_vinculos_curso_op_student_course.csv` (Vínculos de Curso - Multi-Vínculo)
11. `11_livro_razao_historico_op_student_credit_ledger.csv` (Livro-Razão Acadêmico Imutável)
12. `12_bancas_defesas_capes_thesis.csv` (Trabalhos Finais, Defesas e Handles DSpace)
13. `13_produtos_ptt_capes_ptt_product.csv` (Produtos Técnico-Tecnológicos e Qualis)

---

## 2. Dicionário Exaustivo de Campos e Seleções por Arquivo

### `01_ies_instituicao_res_company.csv` (Modelo: `res.company`)
* `id`: Identificador XML ID único da IES (ex: `comp_ies_xyzq`). **Obrigatório**.
* `name`: Nome oficial por extenso da IES (ex: `Universidade XYZQ`). **Obrigatório**.
* `cnpj`: CNPJ formatado (`XX.XXX.XXX/XXXX-XX`). Módulo 11 obrigatório.
* `emec_code`: Código institucional no e-MEC.
* `street`, `city`, `zip`: Endereço físico e CEP.
* `country_id/code`: Código ISO do país (`BR`).

### `02_programas_capes_op_program.csv` (Modelo: `op.program.capes`)
* `id`: Identificador único do PPG (ex: `prog_33001010001P1`). **Obrigatório**.
* `name`: Nome oficial completo do PPG. **Obrigatório**.
* `short_name`: Sigla do programa (ex: `PPGCC`, `MPTRCS`).
* `snpg_code`: Código oficial SNPG da CAPES (ex: `33001010001P1`). **Obrigatório**.
* `modality`: Modalidade: `academic` (Acadêmico) ou `professional` (Profissional). **Obrigatório**.
* `capes_grade`: Nota da avaliação quadrienal da CAPES (`3`, `4`, `5`, `6`, `7`). **Obrigatório**.
* `school_term`: Regime letivo: `bimestral`, `trimestral`, `quadrimestral`, `semestral`, `anual`. **Obrigatório**.
* `company_id/id`: FK referenciando a IES em `res.company` (ex: `comp_ies_xyzq`). **Obrigatório**.

### `03_versao_curricular_op_curriculum_version.csv` (Modelo: `op.curriculum.version`)
* `id`: Identificador XML ID do regimento (ex: `reg_ppgcc_2024`). **Obrigatório**.
* `name`: Nome da versão regimental. **Obrigatório**.
* `program_id/id`: FK do programa em `op.program.capes`. **Obrigatório**.
* `min_credits`: Créditos totais exigidos para titulação (ex: `100`). **Obrigatório**.
* `min_subject_credits`: Mínimo de créditos em disciplinas do PPG (ex: `40`). **Obrigatório**.
* `thesis_credits`: Créditos atribuídos à Dissertação/Tese (ex: `52`). **Obrigatório**.
* `other_mandatory_credits`: Créditos em atividades obrigatórias/seminários (ex: `8`). **Obrigatório**.
* `credit_hour_ratio`: Carga horária por unidade de crédito (ex: `15`). **Obrigatório**.
* `max_external_credits_percent`: Teto percentual de disciplinas externas (ex: `50`).
* `max_months_defense`: Prazo regimental máximo em meses (ex: `24` ou `48`). **Obrigatório**.
* `allow_special_students`: Admite alunos especiais (`True` ou `False`). **Obrigatório**.
* `max_special_subjects_limit`: Limite de disciplinas especiais aproveitáveis (ex: `2` ou `0`).
* `special_credit_validity_months`: Validade dos créditos especiais em meses (ex: `36`).
* `special_incorporation_workflow`: `cpg_approval` (Deliberação CPG) ou `direct_request`.
* `special_transcript_fail_policy`: `omit_on_regular` (Omitir reprovações e não-aproveitadas no histórico regular) ou `display_all`.
* `allow_intra_ies_credits`: Permite disciplinas em outros PPGs da mesma IES (`True` ou `False`).
* `max_intra_ies_credits_percent`: Teto percentual de créditos intra-IES (ex: `30.0` ou `0.0` para sem teto).
* `intra_ies_advisor_approval_required`: Exige anuência do orientador (`True` ou `False`).
* `retorno_rule`: `current_matrix` (Vinculação à matriz vigente no retorno).
* `grading_scale_type`: `scale_abc_r` (A, B, C Aprovados / R Reprovado) ou `scale_abcd_rf`.
* `proficiency_stage`: `admission` (Na Admissão), `qualification` (Na Qualificação), `defense` (Na Defesa).
* `teaching_internship_mode`: `not_applicable`, `scholarship_only`, `mandatory_all`, `flexible_equivalence`.
* `ptt_validation_mode`: `cpg_checklist` (Checklist CPG), `qualis_prior` (Qualis Prévia), `none`.
* `defense_location_policy`: `onsite_mandatory`, `hybrid_allowed`, `fully_remote_allowed`.

### `04_areas_concentracao_op_curriculum_subject_rule.csv` (Modelo: `op.curriculum.subject.rule`)
* `id`: Identificador da área de concentração (ex: `area_ppgcc_ia`). **Obrigatório**.
* `name`: Denominação da área de concentração. **Obrigatório**.
* `curriculum_version_id/id`: FK do regimento em `op.curriculum.version`. **Obrigatório**.
* `description`: Descrição e escopo temático da área.

### `05_docentes_orientadores_op_faculty.csv` (Modelo: `op.faculty` / `res.partner`)
* `id`: Identificador XML ID do docente (ex: `fac_doc_01`). **Obrigatório**.
* `name`: Nome completo do professor/orientador. **Obrigatório**.
* `cpf`: CPF com 11 dígitos numéricos sem pontuação. **Validação Módulo 11 obrigatória**.
* `email`: E-mail institucional do docente. **Obrigatório**.
* `orcid`: PID internacional ORCiD (`0000-0000-0000-0000`).
* `lattes_url`: URL oficial do currículo na Plataforma Lattes.
* `gender`: Gênero: `male` (Masculino) ou `female` (Feminino). **Obrigatório**.
* `birth_date`: Data de nascimento (`YYYY-MM-DD`).

### `06_credenciamento_docente_cpg_op_faculty_accreditation.csv` (Modelo: `op.faculty.accreditation`)
* `id`: Identificador do ato de credenciamento. **Obrigatório**.
* `faculty_id/id`: FK do docente em `op.faculty`. **Obrigatório**.
* `program_id/id`: FK do programa em `op.program.capes`. **Obrigatório**.
* `category`: Categoria de credenciamento: `permanent` (Permanente), `collaborator` (Colaborador) ou `visitor` (Visitante). **Obrigatório**.
* `date_start`: Data de vigência inicial (`YYYY-MM-DD`). **Obrigatório**.
* `date_end`: Data de término (em branco se credenciamento ativo).

### `07_disciplinas_catalogo_op_subject.csv` (Modelo: `op.subject`)
* `id`: Identificador da disciplina (ex: `sub_cc501`). **Obrigatório**.
* `code`: Código acadêmico da disciplina (ex: `CC501`). **Obrigatório**.
* `name`: Denominação oficial da disciplina. **Obrigatório**.
* `program_id/id`: FK do programa ofertante em `op.program.capes`. **Obrigatório**.
* `rule_id/id`: FK da área de concentração em `op.curriculum.subject.rule`.
* `type`: Natureza didática: `theory` (Teórica), `practical` (Prática), `both` (Teórico-Prática). **Obrigatório**.
* `subject_type`: Categoria regimental: `compulsory` (Obrigatória) ou `elective` (Eletiva/Optativa). **Obrigatório**.
* `credits`: Valor numérico nominal de créditos (ex: `4.0`). **Obrigatório**.
* `hours`: Carga horária total correspondente (ex: `60.0`). **Obrigatório**.
* `allow_special_students`: Permite matrícula avulsa de alunos especiais (`True` ou `False`).
* `special_seats_quota`: Vagas reservadas para regime especial (ex: `3` ou `0`).
* `special_student_instructor_consent_required`: Exige anuência expressa do docente ministrante (`True`/`False`).

### `08_editais_selecao_op_admission_edital.csv` (Modelo: `op.admission.edital`)
* `id`: Identificador do edital (ex: `edital_ppgcc_2024`). **Obrigatório**.
* `name`: Título do processo seletivo. **Obrigatório**.
* `code`: Código do edital (ex: `EDITAL-01/2024`).
* `program_id/id`: FK do programa em `op.program.capes`. **Obrigatório**.
* `curriculum_version_id/id`: FK da versão regimental de ingresso. **Obrigatório**.
* `academic_year`: Ano de referência letivo (ex: `2024`). **Obrigatório**.
* `academic_term`: Semestre/período de ingresso (`1` ou `2`). **Obrigatório**.
* `total_slots`: Total de vagas ofertadas no certame. **Obrigatório**.
* `affirmative_action_percent`: Percentual de vagas reservadas para ações afirmativas/cotas (ex: `20.0`).
* `start_date`: Data de abertura das inscrições (`YYYY-MM-DD`). **Obrigatório**.
* `end_date`: Data de encerramento (`YYYY-MM-DD`). **Obrigatório**.
* `state`: Situação: `draft`, `published`, `in_selection`, `homologated`, `cancelled`. **Obrigatório**.

### `09_discentes_identidade_op_student.csv` (Modelo: `op.student` / `res.partner`)
* `id`: Identificador XML ID do discente (ex: `stu_dis_01`). **Obrigatório**.
* `name`: Nome completo do discente. **Obrigatório**.
* `cpf`: CPF com 11 dígitos numéricos sem formatação. **Validação Módulo 11 obrigatória**.
* `email`: E-mail oficial do aluno. **Obrigatório**.
* `ra_number`: Registro Acadêmico (RA) soberano perene na IES (ex: `RA20240001`). **Obrigatório**.
* `gr_no`: Identificador OpenEduCat (espelha o RA). **Obrigatório**.
* `company_id/id`: FK da mantenedora / IES em `res.company`. **Obrigatório**.
* `student_category`: Categoria atual: `regular`, `special` ou `alumni`. **Obrigatório**.
* `gender`: Gênero: `m` (Masculino), `f` (Feminino), `o` (Outro). **Obrigatório**.
* `birth_date`: Data de nascimento (`YYYY-MM-DD`).
* `admission_date`: Data de admissão oficial no programa (`YYYY-MM-DD`). **Obrigatório**.
* `english_proficiency_status`: `pending`, `approved`, `exempt`.
* `portuguese_proficiency_status`: `not_applicable`, `pending`, `approved`.

### `10_vinculos_curso_op_student_course.csv` (Modelo: `op.student.course`)
* `id`: Identificador do vínculo acadêmico (ex: `link_stu_dis_01_reg`). **Obrigatório**.
* `student_id/id`: FK do discente em `op.student`. **Obrigatório**.
* `course_id/id`: FK do curso base em `op.course` ou `op.program.capes`. **Obrigatório**.
* `program_id/id`: FK do programa em `op.program.capes`. **Obrigatório**.
* `curriculum_version_id/id`: FK da versão regimental ativa do vínculo. **Obrigatório**.
* `course_type`: Regime do vínculo: `regular` ou `special`. **Obrigatório**.
* `state`: Estado do vínculo: `running` (Ativo/Em curso), `finished` (Titulado/Concluído) ou `canceled` (Desligado/Jubilado). **Obrigatório**.
* `admission_date`: Data de início do percurso (`YYYY-MM-DD`). **Obrigatório**.
* `completion_date`: Data de conclusão ou desligamento (em branco se ativo).

### `11_livro_razao_historico_op_student_credit_ledger.csv` (Modelo: `op.student.credit.ledger`)
* `id`: Identificador único do lançamento imutável (ex: `led_stu_dis_01_cc501`). **Obrigatório**.
* `student_id/id`: FK do discente em `op.student`. **Obrigatório**.
* `curriculum_version_id/id`: FK da versão regimental vinculada. **Obrigatório**.
* `subject_id/id`: FK da disciplina em `op.subject` (opcional para ritos e apo).
* `course_name`: Denominação da disciplina ou atividade acadêmica. **Obrigatório**.
* `credit_type`: Natureza do crédito: `subject_internal`, `subject_intra_ies`, `subject_special_quarantine`, `subject_special_incorporated`, `subject_extra_ies`, `apo`, `milestone`, `external`. **Obrigatório**.
* `credits`: Valor numérico de créditos integralizados (ex: `4.0`). **Obrigatório**.
* `hours`: Carga horária correspondente (ex: `60.0`). **Obrigatório**.
* `grade_concept`: Conceito regimental (`A`, `B`, `C`, `D`, `R`).
* `is_approved`: Booleano de aprovação (`True` ou `False`). **Obrigatório**.
* `date_earned`: Data de consolidação da nota/crédito (`YYYY-MM-DD`). **Obrigatório**.
* `origin_ref`: Referência da turma, semestre ou ata da CPG (ex: `Turma 2024/1`).

### `12_bancas_defesas_capes_thesis.csv` (Modelo: `capes.thesis`)
* `id`: Identificador da banca/trabalho final (ex: `thesis_stu_dis_01`). **Obrigatório**.
* `student_id/id`: FK do discente em `op.student`. **Obrigatório**.
* `work_plan_id/id`: FK do plano de trabalho homologado em `op.student.work_plan`. **Obrigatório para defesas**.
* `curriculum_version_id/id`: FK da versão regimental. **Obrigatório**.
* `title`: Título definitivo da dissertação ou tese. **Obrigatório**.
* `doc_type`: Tipo de trabalho: `dissertation` (Dissertação), `thesis` (Tese), `tech_product`. **Obrigatório**.
* `stage`: Rito acadêmico: `seminar_area` (Seminário de Área), `qualification` (Qualificação), `defense` (Defesa Pública). **Obrigatório**.
* `status`: Situação: `draft`, `scheduled`, `approved`, `disapproved`, `deposit_pending`, `final_version_submitted`, `homologated`. **Obrigatório**.
* `defense_date`: Data da realização da sessão pública (`YYYY-MM-DD`). **Obrigatório**.
* `repository_url`: Handle permanente no repositório institucional DSpace (ex: `http://repositorio.xyzq.edu.br/handle/123456789/42`).
* `advisor_id/id`: FK do docente orientador em `op.faculty`. **Obrigatório**.

### `13_produtos_ptt_capes_ptt_product.csv` (Modelo: `capes.ptt.product`)
* `id`: Identificador do produto técnico-tecnológico (ex: `ptt_stu_dis_01_01`). **Obrigatório**.
* `title`: Denominação oficial do produto tecnológico. **Obrigatório**.
* `name`: Identificador/nome (espelha `title`). **Obrigatório**.
* `thesis_id/id`: FK da dissertação/tese vinculada em `capes.thesis`. **Obrigatório**.
* `student_id/id`: FK do discente autor principal em `op.student`. **Obrigatório**.
* `axis_id/id`: FK do Eixo estruturante CAPES (`1` a `4` em `capes.ptt.axis`). **Obrigatório**.
* `type_id/id`: FK da Tipologia CAPES (`1` a `21` em `capes.ptt.type`). **Obrigatório**.
* `final_stratum`: Estrato Qualis Tecnológico: `T1`, `T2`, `T3`, `T4`, `T5`, `TNC`. **Obrigatório**.
* `trl_level`: Nível de maturidade tecnológica: `trl_1`, `trl_2`, `trl_3`, `trl_4`, `trl_5`, `trl_6`, `trl_7`, `trl_8`, `trl_9`. **Obrigatório**.
* `adherence_justif`: Justificativa circunstanciada de aderência à linha de pesquisa. **Obrigatório**.
* `state`: Situação: `draft`, `adherence_check`, `evaluating`, `homologated`, `rejected`. **Obrigatório**.
