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
* **Matriz de Carga Horária e Escala de Avaliação:**
  * Valor em horas-aula de cada crédito (`credit_hour_ratio`: ex: 15h no IPEN/CDTN vs 10h/12h no Mackenzie).
  * Escala de conceitos e nota de corte para aprovação (`grading_scale_type`), suportando o conceito "D" como aprovado (CDTN) ou "C" (IPEN/Mackenzie).
* **Parametrização do Momento da Proficiência (`proficiency_stage`):**
  * `admission`: Exigência na matrícula inicial (Regra IPEN/USP).
  * `qualification`: Exigência no Exame de Qualificação.
  * `defense`: Exigência no momento do depósito da Defesa Final.
* **Disciplinas Obrigatórias Dinâmicas (`op.curriculum.subject.rule`):**
  * Configuração de obrigatoriedade parametrizável (*no hardcoded*), podendo ter escopo geral do programa ou específico por Área de Concentração (`area_id`).
* **Regra de Estágio de Docência / Supervisionado (`teaching_internship_mode` - Portaria CAPES nº 221/2025):**
  * `not_applicable` (Inaplicável para Programas Profissionais ou isentos), `scholarship_only` (Bolsistas), `mandatory_all` (Todos), ou `flexible_equivalence` (Permite substituição por Estágio Supervisionado e atividades práticas).
* **Validação de PTT (`ptt_validation_mode`):**
  * `cpg_checklist` (Checklist + Dupla Anuência + Pauta CPG), `qualis_prior` (Estrato Qualis T1-T5 prévio), ou `none` (Cursos Acadêmicos).
* **Regras de Composição de Bancas e Votação (`op.curriculum.committee.rule`):**
  * Quórum de titulares e suplentes (ex: 3 membros no Mestrado; 3 a 5 no Doutorado; 2 suplentes fixos ou 1 suplente por titular).
  * Voto do Orientador (`voting_president` no IPEN/Mackenzie vs. `non_voting_president` no CDTN e opção USP).
  * Quórum de membros externos ao PPG (mínimo 1 externo, mínimo 2 externos, ou maioria externa).
* **Política de Modalidade da Defesa (`defense_location_policy`):**
  * `onsite_mandatory` (Presencial obrigatório), `hybrid_allowed` (Presença física do aluno/presidente), ou `fully_remote_allowed` (100% remota autorizada).

## 3. O Vínculo Único e Irrevogável do Discente

A arquitetura do sistema bloqueia categoricamente a dubiedade normativa. O perfil do discente (`op.student`) receberá um campo relacional obrigatório denominado `curriculum_version_id`.

Toda a lógica de verificação de pré-requisitos consultará exclusivamente as propriedades desta chave estrangeira. Este vínculo é irrevogável por período letivo; o discente não pode ter o seu versionamento alterado sem a passagem por um fluxo de migração auditável.
