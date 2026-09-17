# Dicionário de Esqueletos CSV de Importação e Ordem de Carga
## Ecossistema l10n_br_openeducat_capes (Odoo 19.0 / OpenEduCat 19.0)

Este diretório contém os **modelos padronizados de planilhas CSV** para importação oficial de dados em lote no Odoo 19.0 e OpenEduCat 19.0.

---

## 1. Ordem Estrita de Carga de Arquivos

Para assegurar a resolução de todas as Chaves Estrangeiras (*Foreign Keys*) sem falhas de integridade referencial, os 33 arquivos devem ser importados rigorosamente na seguinte sequência:

### Fase 1: Infraestrutura Institucional e OpenEduCat Base
1. `01a_ies_instituicao_res_company.csv` (`res.company`) — Instituição de Ensino Superior / Empresa Mantenedora.
2. `01b_departamentos_op_department.csv` (`op.department`) — Departamentos acadêmicos, CPG e Secretarias.
3. `01c_categorias_op_category.csv` (`op.category`) — Categorias discentes e docentes.
4. `01d_anos_academicos_op_academic_year.csv` (`op.academic.year`) — Anos letivos e regimes de semestres.
5. `01e_termos_academicos_op_academic_term.csv` (`op.academic.term`) — Períodos e termos semestrais.
6. `01f_niveis_programa_op_program_level.csv` (`op.program.level`) — Níveis de pós-graduação stricto sensu.
7. `01g_programas_openeducat_op_program.csv` (`op.program`) — Programas acadêmicos na ontologia OpenEduCat.
8. `01h_cursos_openeducat_op_course.csv` (`op.course`) — Cursos base vinculados aos programas.
9. `01i_lotes_turmas_op_batch.csv` (`op.batch`) — Lotes/turmas discentes de ingresso (cohorts).

### Fase 2: Ontologia Regimental e Programas CAPES
10. `02_programas_capes_op_program.csv` (`op.program.capes`) — Programas oficiais com código SNPG e nota CAPES.
11. `03_versao_curricular_op_curriculum_version.csv` (`op.curriculum.version`) — Regimentos e matrizes curriculares.
12. `04a_areas_concentracao_op_program_concentration_area.csv` (`op.program.concentration.area`) — Áreas de concentração do PPG.
13. `04b_linhas_pesquisa_op_program_research_line.csv` (`op.program.research.line`) — Linhas de pesquisa vinculadas às áreas.

### Fase 3: Corpo Docente, Credenciamento e Pesquisa
14. `05_docentes_orientadores_op_faculty.csv` (`op.faculty`) — Docentes com PIDs (ORCiD/Lattes) e Censo CAPES completo.
15. `06a_vinculos_docente_programa_op_faculty_program_link.csv` (`op.faculty.program.link`) — Vínculos formais docente-programa.
16. `06b_credenciamento_docente_ledger_op_faculty_category_ledger.csv` (`op.faculty.category.ledger`) — Livro-razão append-only de credenciamento.
17. `07a_disciplinas_catalogo_op_subject.csv` (`op.subject`) — Disciplinas do catálogo com créditos e horas.
18. `07b_regras_curriculares_op_curriculum_subject_rule.csv` (`op.curriculum.subject.rule`) — Regras regimentais das disciplinas.
19. `07c_projetos_pesquisa_capes_research_project.csv` (`capes.research.project`) — Projetos de pesquisa com fomento oficial.

### Fase 4: Processo Seletivo, Discentes e Vida Acadêmica
20. `08_editais_selecao_op_admission_edital.csv` (`op.admission.edital`) — Editais de processos seletivos públicos.
21. `09_discentes_identidade_op_student.csv` (`op.student`) — Identidades discentes soberanas e RA perene.
22. `10a_vinculos_curso_op_student_course.csv` (`op.student.course`) — Vínculos ativos/concluídos com cursos e turmas.
23. `10b_planos_trabalho_op_student_work_plan.csv` (`op.student.work_plan`) — Planos de trabalho homologados com PDF em Base64.
24. `11_livro_razao_historico_op_student_credit_ledger.csv` (`op.student.credit.ledger`) — Livro-razão acadêmico append-only.

### Fase 5: Conclusão, PTT, Diplomas e Governança
25. `12a_bancas_defesas_capes_thesis.csv` (`capes.thesis`) — Defesas públicas de dissertação e tese homologadas.
26. `12b_comissoes_examinadoras_capes_thesis_committee.csv` (`capes.thesis.committee`) — Composição completa de bancas examinadoras.
27. `13a_produtos_ptt_capes_ptt_product.csv` (`capes.ptt.product`) — Produtos Técnico-Tecnológicos com estrato Qualis e TRL.
28. `13b_autores_ptt_capes_ptt_author.csv` (`capes.ptt.author`) — Coautoria discente e docente no PTT.
29. `14_diplomas_digitais_capes_digital_diploma.csv` (`capes.digital.diploma`) — Diplomas digitais registrados (Portaria MEC 70/2025).
30. `15a_governanca_cpg_comissoes_op_cpg_committee.csv` (`op.cpg.committee`) — Gestões e mandatos da Comissão de Pós-Graduação.
31. `15b_membros_cpg_op_cpg_member.csv` (`op.cpg.member`) — Membros titulares, suplentes e representação discente da CPG.
32. `15c_reunioes_atas_cpg_op_cpg_meeting.csv` (`op.cpg.meeting`) — Reuniões ordinárias e atas homologadas.
33. `16_usuarios_perfis_res_users.csv` (`res.users`) — Perfis de usuários institucionais e permissões de acesso.

---

## 2. Regras Essenciais de Integridade e Modelagem

1. **Separação Soberana entre Pessoa e Vínculo:**
   * `op.student` indexa a pessoa física e o RA institucional perene (imutável por CPF).
   * `op.student.course` registra cada percurso formativo específico (regular ou especial) vinculado ao respectivo `op.course` e `op.batch`.
2. **Imutabilidade do Livro-Razão Acadêmico:**
   * `op.student.credit.ledger` opera estritamente em modo *append-only*. Não admite deleções ou recálculos destrutivos.
3. **Estrutura Bipartida de Credenciamento Docente:**
   * `op.faculty.program.link` estabelece o vínculo Many2one docente-programa.
   * `op.faculty.category.ledger` armazena o histórico auditável de credenciamentos com datas de início/fim e número de portaria.
4. **Governança de Bancas e Produtos PTT:**
   * As bancas examinadoras residem em `capes.thesis.committee` (evitando colunas restritivas em `capes.thesis`).
   * A tipologia de produtos PTT utiliza os identificadores oficiais da taxonomia CAPES (ex: `l10n_br_openeducat_capes_ptt.ptt_type_t19`), e o campo `axis_id` é preenchido automaticamente pelo Odoo.
