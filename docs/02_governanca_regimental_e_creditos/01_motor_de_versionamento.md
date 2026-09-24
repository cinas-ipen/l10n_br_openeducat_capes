# Documento 01: Motor de Versionamento Curricular e Parametrização

## 1. O Desafio da Parametrização Acadêmica no Stricto Sensu

A arquitetura nativa do OpenEduCat baseia-se na premissa norte-americana e europeia de que um curso ou programa de pós-graduação (`op.course` ou `op.program`) detém regras estáticas e universais para todos os alunos ali matriculados. No cenário acadêmico brasileiro, devido à autonomia universitária e à necessidade de atender às métricas evolutivas da CAPES, os programas atualizam constantemente os seus regulamentos.

Essa realidade exige que o ERP suporte a coexistência de discentes no mesmo programa operando sob conjuntos de regras drasticamente diferentes. Para solucionar essa lacuna arquitetural, o módulo `l10n_br_openeducat_capes_academic` isola as regras do nível de programa e as transfere para uma nova entidade dinâmica de versionamento.

## 2. A Entidade de Versionamento (`op.curriculum.version`)

O modelo `op.curriculum.version` atua como o motor orquestrador de regras e o cérebro das validações sistêmicas do OpenEduCat. Cada programa de pós-graduação (`op.program.capes`) possuirá uma relação *One2many* com suas respectivas versões de currículo.

Esta entidade concentra parâmetros vitais que balizam o motor cronológico, a avaliação acadêmica e as bancas de titulação, incluindo:

* **Prazos Temporais e Cronometria:**
  * Prazo máximo para exame de qualificação/seminário de área e prazo limite em meses para a defesa (`max_months_defense`).
  * Teto máximo de prorrogação regular e extraordinária (`max_extension_days`).
  * Prazo limite para entrega do PDF definitivo pós-defesa (`max_days_post_defense_deposit`), configurável de 30 dias (IPEN/Mackenzie) a 90 dias (CDTN).
  * Minutagem de exposição e arguição (`presentation_max_minutes`, `arguing_max_minutes_per_member`).
* **Regras de Trancamento e Flexibilidade:**
  * Prazo máximo de trancamento contínuo (`max_trancamento_days`): Parametrizável (ex: 365 dias no MPTRCS).
  * Bloqueio de trancamento no 1º semestre (`block_first_semester_trancamento`): Booleano parametrizável (True/False).
  * Regra de Retorno (`retorno_rule`): Define a vinculação automática à estrutura curricular vigente no retorno, aplicando o Ato Jurídico Perfeito sobre créditos já integralizados e exigindo cumprimento da nova matriz para pendências.
* **Matriz de Carga Horária, Créditos e Aproveitamento (Sucupira / CAPES / Regimento):**
  * Créditos Totais Exigidos (`min_credits`): Total geral necessário para titulação (ex: 100 créditos no MP-TRCS v2).
  * Créditos Mínimos em Disciplinas (`min_subject_credits`): Créditos exigidos em disciplinas presenciais do programa (ex: 40 créditos no MP-TRCS v2).
  * Créditos da Dissertação / Tese (`thesis_credits`): Créditos atribuídos ao Trabalho Final de Curso (ex: 52 créditos no MP-TRCS v2).
  * Créditos em Outras Atividades Obrigatórias (`other_mandatory_credits`): Créditos atribuídos a Seminários Gerais de Área ou Estágios (ex: 8 créditos no MP-TRCS v2).
  * Teto de Aproveitamento de Créditos Externos (`max_external_credits_percent`): Percentual máximo de disciplinas cursadas fora do PPG (ex: 50% no MP-TRCS v2).
  * Teto Efetivo de Créditos Externos (`max_external_subject_credits`): Campo computado automaticamente (`min_subject_credits * max_external_credits_percent / 100`, ex: 20.0 créditos).
  * Valor em horas-aula de cada crédito (`credit_hour_ratio`: ex: 15h no IPEN/CDTN vs 10h/12h no Mackenzie).
  * Escala de conceitos e nota de corte para aprovação (`grading_scale_type`), suportando o conceito "D" como aprovado (CDTN) ou "C" (IPEN/Mackenzie).
* **Governança de Alunos Especiais (Disciplinas Isoladas):**
  * Permissão de Alunos Especiais no Programa (`allow_special_students`): Booleano parametrizável. No MPTRCS do IPEN, por diretriz regimental, o valor padrão é **`False`** (o programa não admite alunos especiais em suas disciplinas exclusivas).
  * Limite Máximo de Disciplinas Isoladas (`max_special_subjects_limit`): Quantidade máxima de disciplinas que um aluno especial pode cursar (ex: até 2 disciplinas ou 8 créditos).
  * Prazo Decadencial de Validade de Créditos (`special_credit_validity_months`): Prazo limite em meses (padrão **36 meses / 3 anos**) contado da conclusão da disciplina isolada para que o aluno, uma vez aprovado como aluno regular, possa requerer a integralização em seu histórico.
  * Fluxo de Homologação de Aproveitamento (`special_incorporation_workflow`): `cpg_approval` (exige parecer do orientador e homologação em ata da CPG) ou `direct_request` (incorporação direta via requerimento dentro do prazo de validade).
  * Política de Exibição de Reprovações no Histórico (`special_transcript_fail_policy`):
    * `omit_on_regular` (**Padrão MPTRCS**): Reprovações ("R" ou "F") obtidas enquanto discente sob vínculo de aluno especial figuram exclusivamente na certidão interna de estudos isolados; ao ingressar como Aluno Regular, o Histórico Escolar Oficial de titulação exibe apenas as disciplinas formalmente deferidas e aproveitadas pela CPG.
    * `display_all`: Qualquer reprovação sofrida em regime especial é transportada e exibida no histórico final do curso regular.
* **Governança de Disciplinas Intra-IES vs. Extra-IES:**
  * Permissão de Cursar Disciplinas em outros PPGs da mesma IES (`allow_intra_ies_credits`): Booleano parametrizável (default `True`).
  * Teto de Créditos Intra-IES (`max_intra_ies_credits_percent`): Percentual máximo da carga teórica que pode ser cumprido em outros programas da mesma instituição mantenedora (`res.company`). Disciplinas intra-IES mantêm **100% de equivalência nominal de créditos** (sem fator de conversão redutor).
  * Exigência de Anuência do Orientador (`intra_ies_advisor_approval_required`): Booleano (default `True`).
  * **Distinção Regulatória no Contexto IPEN (MPTRCS vs. Tecnologia Nuclear):** No caso singular do IPEN, o programa acadêmico tradicional de Tecnologia Nuclear é institucionalmente titulado e registrado pela Universidade de São Paulo (USP) — ou seja, perante o MEC e a CAPES, pertence a outra IES registradora. Dessa forma, para os alunos regulares do MPTRCS (programa exclusivo do IPEN), disciplinas cursadas na Tecnologia Nuclear da USP são classificadas juridicamente como **extra-IES**. Elas não operam sob a regra automática intra-IES, exigindo abertura de processo formal de equivalência e aprovação prévia da CPG do MPTRCS, respeitando o teto de créditos externos (`max_external_credits_percent`).
* **Parametrização do Momento da Proficiência (`proficiency_stage`):**
  * `admission`: Exigência na matrícula inicial (Regra IPEN).
  * `qualification`: Exigência no Exame de Qualificação.
  * `defense`: Exigência no momento do depósito da Defesa Final.
* **Disciplinas Obrigatórias Dinâmicas (`op.curriculum.subject.rule`):**
  * Configuração de obrigatoriedade parametrizável (*no hardcoded*), com tipo de regra (`rule_type`: obrigatória ou eletiva) e escopo de abrangência (`scope`: geral do programa `'program'` ou restrito por Área de Concentração `'area'`), armazenando a denominação da área no campo `area_name`.
* **Regra de Estágio de Docência / Supervisionado (`teaching_internship_mode` - Portaria CAPES nº 221/2025):**
  * `not_applicable` (Inaplicável para Programas Profissionais ou isentos), `scholarship_only` (Bolsistas), `mandatory_all` (Todos), ou `flexible_equivalence` (Permite substituição por Estágio Supervisionado e atividades práticas).
* **Validação de PTT (`ptt_validation_mode`):**
  * `cpg_checklist` (Checklist + Dupla Anuência + Pauta CPG), `qualis_prior` (Estrato Qualis T1-T5 prévio), ou `none` (Cursos Acadêmicos).
* **Regras de Composição de Bancas e Votação (`op.curriculum.committee.rule`):**
  * Quórum de titulares e suplentes (ex: 3 membros no Mestrado; 3 a 5 no Doutorado; 2 suplentes fixos ou 1 suplente por titular).
  * Voto do Orientador (`voting_president` no IPEN/Mackenzie vs. `non_voting_president` no CDTN).
  * Quórum de membros externos ao PPG (mínimo 1 externo, mínimo 2 externos, ou maioria externa).
* **Política de Modalidade da Defesa (`defense_location_policy`):**
  * `onsite_mandatory` (Presencial obrigatório), `hybrid_allowed` (Presença física do aluno/presidente), ou `fully_remote_allowed` (100% remota autorizada).

## 3. A Separação entre Identidade Soberana e Vínculo Acadêmico (Opção B)

A arquitetura do sistema consagra a separação entre a **Pessoa Acadêmica Soberana** (`op.student`), que detém o Registro Acadêmico (RA) unificado e irrevogável emitido pela IES sob a âncora do CPF, e os **Vínculos Acadêmicos de Curso** (`op.student.course` / histórico de matrículas).

* Cada vínculo regular ativo referencia obrigatoriamente um `curriculum_version_id` específico.
* Toda a lógica de verificação de pré-requisitos, prazos e integralização consulta as propriedades da versão regimental vinculada ao percurso ativo do discente.
* Este modelo garante que um aluno especial possa transitar para aluno regular no MPTRCS preservando seu RA institucional único, mantendo o histórico de auditoria intacto e permitindo a incorporação estrita das disciplinas válidas e homologadas pela CPG sob a chancela do Ato Jurídico Perfeito.
