# **Documento de Validação Técnica e Funcional: Macroprocesso 01 (MP1)**

## **Governança Regimental, Setup Curricular e Regras Normativas no ERP**

### **1. Finalidade do Macroprocesso 01 (MP1)**

O Macroprocesso 01 é o motor de *back-office* fundacional do ecossistema educacional OpenEduCat CAPES BR (l10n_br_openeducat_capes_academic). Ele é executado antes da publicação de qualquer edital de seleção ou da realização de matrículas discentes.

Sua finalidade principal é criar um **ambiente normativo isolado** para governar uma geração inteira de estudantes de um Programa de Pós-Graduação (PPG). Esse isolamento garante:

* **Prevenção ao Hibridismo Normativo:** Proibe que um discente combine casuisticamente as regras mais benéficas de regulamentos distintos (ex: prazos longos de um regimento antigo com carga menor de disciplinas de um regimento novo).
* **Tutela ao Ato Jurídico Perfeito:** Assegura que matérias e créditos já integralizados pelo aluno sob a vigência de uma norma permanecem imutáveis, mesmo que o programa atualize suas regras no futuro.
* **Auditabilidade GoPG/CAPES:** Garante que todas as validações do censo acadêmico enviadas via APIs RESTful (Fonte Prata) ou colhidas no Repositório Institucional (Fonte Ouro) tenham respaldo regimental exato.

### **2. A Arquitetura do Motor de Versionamento (op.curriculum.version)**

Para superar a limitação dos ERPs multinacionais tradicionais (que amarram as regras de forma estática ao curso), o OpenEduCat centraliza a inteligência regulatória na entidade **Versão de Currículo / Regimento (op.curriculum.version)**.

```text
+-------------------------------------------------------------------------+
|                       PROGRAMA DE PÓS-GRADUAÇÃO                         |
|                       op.program.capes (ex: MPTRCS)                     |
+-------------------------------------------------------------------------+
                                     │ 1
                                     │
                                     │ N (One2many)
                                     ▼
+-------------------------------------------------------------------------+
|                  MOTOR DE VERSIONAMENTO REGIMENTAL                      |
|                       op.curriculum.version                             |
|  - Prazos e Cronometria            - Modos de PTT e Docência            |
|  - Moeda de Crédito e Escala       - Regras de Disciplinas (Subject)    |
|  - Proficiência Linguística        - Regras de Bancas (Committee)       |
+-------------------------------------------------------------------------+
                                     ▲
                                     │ 1
                                     │ (Chave Irrevogável: curriculum_version_id)
                                     │ N
+-------------------------------------------------------------------------+
|                          PERFIL DO DISCENTE                             |
|                              op.student                                 |
+-------------------------------------------------------------------------+
```

Cada discente recebe no ato da matrícula a chave relacional unívoca curriculum_version_id em seu perfil (op.student). As rotinas do sistema (validação de grade, agendamento de bancas, concessão de prorrogações e emissão de diplomas) consultam exclusivamente as propriedades dessa chave.

### **3. Detalhamento dos 10 Subprocessos do Macroprocesso 01**

Abaixo, cada um dos 10 subprocessos do MP1 é detalhado considerando a **Lógica de Workflow**, a **Configuração para o MPTRCS/IPEN (Stakeholders Principais)** e a **Matriz de Parametrização para Outras IES/PPGs**.

#### **Subprocesso 1.1: Criação e Isolamento do Versionamento Curricular**

* **Descrição Operacional:** A Secretaria Acadêmica ou Coordenação cadastra a versão regimental no ERP e estabelece o vínculo relacional *One2many* com o programa acadêmico (op.program.capes). Define-se o período de vigência e ativa-se o indicador booleano is_active para disponibilizar a norma para novos editais de seleção.
* **Configuração Específica MPTRCS/IPEN:**
* *Nome da Versão (name):* "Regulamento MPTRCS 2020 (Revisado CTA)".
* *Vínculo de Programa (program_id):* Programa de Pós-Graduação em Tecnologia das Radiações em Ciências da Saúde (Código SNPG CAPES).
* *Indicador de Vigência (is_active):* True (Versão ativa para as turmas correntes).
* **Matriz de Parametrização no ERP:** Suporta coexistência de ilimitadas versões simultâneas no mesmo banco de dados (ex: "Regimento IPEN 2018", "Regimento IPEN 2020", "Regimento CDTN 2026", "Regimento UPM 2024").

#### **Subprocesso 1.2: Parametrização Cronológica, Prazos e Cronometria**

* **Descrição Operacional:** Configura os relógios temporais do sistema a partir da data de admissão (admission_date). O motor cronológico dispara notificações de acompanhamento e aciona a Ação Agendada (Cron Job) de jubilamento automático (pending_dismissal) em caso de estouro dos prazos regimentais.
* **Configuração Específica MPTRCS/IPEN:**
* *Prazo Máximo de Titulação (max_months_defense):* **24 meses**.
* *Teto de Prorrogação Regular (max_extension_days):* **90 dias** (em caráter excepcional aprovado pela CPG-MP).
* *Prazo Limite para Depósito Pós-Defesa (max_days_post_defense_deposit):* **30 dias** pós-defesa pública para upload da versão corrigida no Repositório Institucional.
* *Tempo de Exposição do Candidato (presentation_max_minutes):* **50 minutos**.
* *Tempo de Arguição por Examinador (arguing_max_minutes_per_member):* **40 minutos**.
* **Matriz de Parametrização no ERP:**
* *Prazo de Titulação:* Ajustável em meses (ex: 24 meses para Mestrado e 48 meses para Doutorado).
* *Prorrogação Regular:* Ajustável em dias/meses (ex: 90 dias no IPEN vs. 180 dias/6 meses no Mackenzie e CDTN).
* *Depósito Pós-Defesa:* Ajustável em dias (ex: 30 dias no IPEN/Mackenzie vs. 90 dias no CDTN Art. 50).
* *Cronometria da Sessão:* Ajustável em minutos (ex: 45 min de exposição no CDTN Art. 48 §2º).

#### **Subprocesso 1.3: Fator de Conversão de Carga Horária e Escala de Avaliação**

* **Descrição Operacional:** Define a "moeda" acadêmica impressa no histórico escolar consolidado (op.student.transcript.br) e a regra matemática de apuração de notas/conceitos para gravação na tabela imutável (*append-only*) do Livro-Razão Acadêmico (op.student.credit.ledger).
* **Configuração Específica MPTRCS/IPEN:**
* *Razão Carga Horária/Crédito (credit_hour_ratio):* **15 horas-aula** por unidade de crédito.
* *Escala de Avaliação (grading_scale_type):* 'scale_abc_r' (Conceitos A, B e C conferem créditos; **Conceito R é Reprovado**; exigência de frequência mínima de 75%).
* **Matriz de Parametrização no ERP:**
* *Fator de Crédito:* 15 horas (IPEN e CDTN), 12 horas (Mackenzie Computação) ou 10 horas (Mackenzie ADN).
* *Escalas e Notas de Corte:* Suporta notas numéricas de 0 a 10 com corte 7.0 (Mackenzie) ou escalas com conceito "D" considerado **Aprovado** (CDTN Art. 38/42, onde D = 60% a 69%).

#### **Subprocesso 1.4: Motor de Integralização e Silos de Créditos**

* **Descrição Operacional:** Estabelece as metas globais e fracionadas de integralização acadêmica. O ERP divide as exigências em compartimentos (*buckets*) independentes que exigem cumprimento isolado para liberar a câmara de pré-requisitos da defesa.
* **Configuração Específica MPTRCS/IPEN:**
* *Carga Total Mínima Exigida (min_credits):* **100 unidades de crédito**.
* *Silo de Disciplinas do Programa (min_subject_credits):* Mínimo de **40 créditos**.
* *Silo de Seminários Gerais de Área (min_seminar_credits):* Mínimo de **8 créditos**.
* *Silo de Preparo do Trabalho Final (min_thesis_credits):* Mínimo de **52 créditos**.
* *Trava Carga Inicial de Calouros (min_first_semester_credits):* Mínimo de **24 créditos** no 1º semestre de ingresso.
* *Teto de Aproveitamento Externo (max_external_credits):* Até **50% dos créditos em disciplinas** (máximo 20 créditos externos).
* *Teto de Créditos por Produção/Patente (max_publication_credits):* Até **25% dos créditos em disciplinas** (máximo 10 créditos por artigos Web of Science / Patente / Software).
* **Matriz de Parametrização no ERP:**
* *Metas Globais:* 100 créditos (IPEN), 50/60 créditos (Mackenzie), 24 créditos (Mestrado CDTN) ou 47 créditos (Doutorado CDTN).
* *Carga Mínima de Ingressante:* Ajustável por regimento (previne bloqueios em cursos com metas totais menores).
* *Tetos de Aproveitamento:* Configurável (ex: teto externo de 40% no Mackenzie vs 50% no IPEN).

#### **Subprocesso 1.5: Configuração de Proficiência Linguística (proficiency_stage)**

* **Descrição Operacional:** Configura o momento exato em que o ERP exige a aprovação no exame de proficiência em língua estrangeira (Inglês, e Português no caso de discentes estrangeiros).
* **Configuração Específica MPTRCS/IPEN:**
* *Gatilho de Exigência (proficiency_stage):* 'admission' (Modo IPEN).
* *Efeito Sistêmico:* A aprovação no exame de proficiência é condição *sine qua non* no ato do ingresso. O Odoo bloqueia a conversão do candidato aprovado em aluno regular (op.student) e a emissão do número de matrícula caso o comprovante não esteja homologado.
* **Matriz de Parametrização no ERP:**
* 'admission': Exigência na matrícula inicial (IPEN).
* 'qualification': Exigência como pré-requisito para o agendamento da Qualificação (Mackenzie).
* 'defense': Exigência para o depósito da Defesa Final.

#### **Subprocesso 1.6: Parametrização Dinâmica de Disciplinas Obrigatórias (op.curriculum.subject.rule)**

* **Descrição Operacional:** Elimina qualquer código de disciplina fixado em código (*hardcoded*). A obrigatoriedade é gerenciada pela tabela de regras op.curriculum.subject.rule, permitindo definir disciplinas comuns a todo o programa ou vinculadas especificamente a uma Área de Concentração.
* **Configuração Específica MPTRCS/IPEN:**
* *Disciplinas Obrigatórias Gerais (Escopo scope = 'program'):*
1. MP-01 - Fundamentos de Física em Ciências da Saúde.
2. MP-02 - Proteção, Segurança e Logística Radiológica.
* **Matriz de Parametrização no ERP:**
* *Escopo program:* Disciplinas obrigatórias para todos os discentes daquela versão.
* *Escopo area:* Disciplinas obrigatórias atreladas a uma Área de Concentração específica (area_id). O sistema consulta o perfil do aluno (op.student.area_id) e exige o cumprimento do conjunto específico de sua área.

#### **Subprocesso 1.7: Parametrização do Estágio de Docência / Supervisionado (teaching_internship_mode)**

* **Descrição Operacional:** Adequa as travas de obrigatoriedade de atividades didáticas de ensino de acordo com as diretrizes da **Portaria CAPES nº 221/2025**.
* **Configuração Específica MPTRCS/IPEN:**
* *Regra de Estágio de Docência (teaching_internship_mode):* 'not_applicable' (Inaplicável).
* *Justificativa:* Por se tratar de um Programa de Pós-Graduação Profissional, no qual a CAPES não concede bolsas de fomento acadêmico tradicionais, a trava é desativada nativamente pelo ERP.
* **Matriz de Parametrização no ERP:**
* 'not_applicable': Trava desativada (Cursos Profissionais ou isentos).
* 'scholarship_only': Exigido exclusivamente para alunos bolsistas de fomento acadêmico.
* 'mandatory_all': Exigido para todos os discentes do currículo.
* 'flexible_equivalence': Exigido, mas aceita substituição por Estágio Supervisionado ou atividades práticas/profissionais equivalentes homologadas pela CPG.

#### **Subprocesso 1.8: Regras do Produto Técnico-Tecnológico (PTT) (ptt_validation_mode)**

* **Descrição Operacional:** Define o fluxo de validação da entrega aplicada exigida em programas profissionais perante a taxonomia oficial da CAPES (21 tipos GTPT / 10 subcategorias Medicina II).
* **Configuração Específica MPTRCS/IPEN:**
* *Modo de Validação do PTT (ptt_validation_mode):* 'cpg_checklist' (Modelo V1 / MPTRCS).
* *Fluxo de Trabalho V1:*
1. **Checklist no Portal:** No requerimento de agendamento de defesa, o aluno seleciona o PTT gerado a partir do checklist de tipologias da CAPES e faz upload das evidências.
2. **Dupla Anuência Eletrônica:** O **Orientador Principal** e o **Coorientador** (quando houver) devem emitir o aceite eletrônico ("De acordo") nos seus respectivos painéis.
3. **Triagem da Secretaria:** A secretaria acadêmica valida os anexos e marca o chamado como `ready_for_agenda` (Apto para Pauta).
4. **Homologação CPG:** O requerimento entra na pauta da Reunião da CPG (`op.cpg.meeting`). O colegiado avalia o PTT e delibera a aprovação formal que autoriza a realização da defesa.
* **Matriz de Parametrização no ERP:**
* 'cpg_checklist': Checklist + Dupla Anuência + Pauta CPG (Modelo V1 - MPTRCS).
* 'qualis_prior': Exige avaliação prévia em câmara de peritos e atribuição de estrato Qualis (T1 a T5) antes da abertura da defesa.
* 'none': Desativado para programas acadêmicos tradicionais.

#### **Subprocesso 1.9: Regras de Composição de Comissões Julgadoras (op.curriculum.committee.rule)**

* **Descrição Operacional:** Gerencia as regras de quórum, papéis, direitos de voto, endogenia de membros externos e impedimentos por parentesco para os ritos de Seminário de Área, Qualificação e Defesa Final.
* **Configuração Específica MPTRCS/IPEN:**
* *Banca do Seminário Geral de Área (stage = 'seminar'):*
* **2 membros titulares Doutores** (Coordenador da Atividade/Disciplina + 1 examinador Doutor convidado).
* *Banca da Defesa Final de Dissertação (stage = 'defense'):*
* **3 membros titulares Doutores**.
* *Papel do Orientador (advisor_vote_role):* voting_president (Preside a sessão e possui direito a voto ativo).
* *Participação do Coorientador (coadvisor_participation):* forbidden_with_advisor (Participação vedada caso o orientador esteja presente na sessão - Regulamento MPTRCS Art. 10 §3º).
* *Regra de Externos (external_rule):* min_one_external (Pelo menos 1 Doutor obrigatoriamente externo ao Programa e ao IPEN/CNEN).
* *Exceção de Notória Especialização:* Permite especialista de mercado sem doutorado mediante parecer aprovado por **2/3 do Colegiado** (Regulamento MPTRCS Art. 46 §3º).
* *Política de Presença (defense_location_policy):* hybrid_allowed (Presença física obrigatória do discente e do presidente na sede do IPEN, permitindo examinadores remotos).
* **Matriz de Parametrização no ERP:**
* *Quórum:* 3 a 5 membros titulares; suplentes por par fixo (1 int / 1 ext - Mackenzie) ou 1 para cada titular.
* *Voto do Orientador:* Votante (voting_president - IPEN/Mackenzie) vs. Não-Votante (non_voting_president - CDTN Art. 44 §4º).
* *Membros Externos:* Mínimo 1 externo (IPEN/Mackenzie), Mínimo 2 externos (CDTN Doutorado), ou Maioria Externa ao PPG.
* *Impedimento Cível:* Trava automática para parentesco em linha reta ou colateral até 4º grau com o discente ou orientador.
* *Modalidade:* Presencial, Híbrida ou 100% Remota autorizada (CDTN Art. 49).

#### **Subprocesso 1.10: Tramitação e Protocolo de Migração Regimental**

* **Descrição Operacional:** Garante a transparência e o cumprimento estrito do direito de opção quando o programa aprova uma atualização em seu regulamento.
* **Configuração Específica MPTRCS/IPEN:**
* *Formulário de Solicitante no Portal:* Requerimento `op.academic.request` (`request_type = 'regime_migration'` com seleção de `target_curriculum_version_id`).
* *Fluxo de Trabalho:*
1. O estudante inicia a solicitação no Portal do Aluno.
2. O Odoo gera e exibe um **Quadro Comparativo de Impacto** (demonstrando eventuais variações de carga de disciplinas e prazos).
3. O discente assina digitalmente o **Termo de Aceite Irrevogável**.
4. Após homologação na pauta da CPG, o Odoo encerra a leitura do Livro-Razão no regimento antigo (preservando o Ato Jurídico Perfeito de todas as disciplinas e notas já conquistadas) e passa a contabilizar a integralização na nova versão curriculum_version_id, vedando o hibridismo normativo.

### **4. Tabela de Parametrização para Validação com Stakeholders (MPTRCS)**

A tabela abaixo deve ser revisada e formalmente aprovada durante a reunião de trabalho com a Coordenação, Comissão de Pós-Graduação (CPG-MP) e Secretaria Acadêmica do MPTRCS/IPEN:

| Item de Governança / Parâmetro | Campo Técnico no Odoo | Configuração Padrão MPTRCS (IPEN) | Outras Opções Suportadas pelo ERP |
| :---- | :---- | :---- | :---- |
| **Duração Regimental do Curso** | max_months_defense | **24 Meses** | Parametrizável (ex: 12 a 48 meses) |
| **Teto Contínuo de Trancamento** | `max_trancamento_days` | **365 dias** (Art. 22º, §3º) | Parametrizável por regimento (ex: 180 a 365 dias) |
| **Bloqueio no 1º Semestre** | `block_first_semester_trancamento` | **False** (Permitido em qualquer tempo) | **True** (Caso o regimento exija carência inicial) |
| **Regra de Retorno Pós-Trancamento** | `retorno_rule` | **Matriz Vigente no Retorno** (Ato Jurídico Perfeito preservado) | Vinculação imediata à estrutura atual sem hibridismo. |
| **Teto de Prorrogação Regular** | max_extension_days | **90 Dias** (Excepcional CPG) | Parametrizável (ex: 180 a 365 dias) |
| **Prazo de Depósito Pós-Defesa** | max_days_post_defense_deposit | **30 Dias** | Parametrizável (ex: 30 a 90 dias) |
| **Fator Carga Horária/Crédito** | credit_hour_ratio | **15 Horas / Crédito** | 10h, 12h ou 15h por crédito |
| **Meta Global de Integralização** | min_credits | **100 Créditos** | Configurável (24, 47, 50, 60, 100) |
| **Bucket 1: Disciplinas Programa** | min_subject_credits | **40 Créditos** (mínimo) | Configurável por versão regimental |
| **Bucket 2: Seminários Gerais** | min_seminar_credits | **8 Créditos** (mínimo) | Configurável por versão regimental |
| **Bucket 3: Preparo Dissertação** | min_thesis_credits | **52 Créditos** (mínimo) | Configurável por versão regimental |
| **Trava Carga Inicial Calouros** | min_first_semester_credits | **24 Créditos** (1º Semestre) | Configurável conforme a meta do PPG |
| **Gatilho de Proficiência** | proficiency_stage | 'admission' (Matrícula Inicial) | 'qualification' ou 'defense' |
| **Disciplinas Obrigatórias** | op.curriculum.subject.rule | MP-01 e MP-02 (Gerais) | Por Programa ou por Área de Concentração |
| **Estágio de Docência (CAPES 221)** | teaching_internship_mode | 'not_applicable' (Profissional) | 'scholarship_only', 'mandatory_all', 'flexible' |
| **Mecânica de Validação de PTT** | ptt_validation_mode | 'cpg_checklist' (Checklist + CPG) | 'qualis_prior' ou 'none' |
| **Papel e Voto do Orientador** | advisor_vote_role | 'voting_president' (Preside/Vota) | 'non_voting_president' (CDTN) |
| **Participação Coorientador** | coadvisor_participation | 'forbidden_with_advisor' | 'non_voting_additional' ou 'full_voting' |
| **Endogenia de Externos** | external_rule | 'min_one_external' (1 externo IPEN) | 'min_two_external' ou 'majority_external' |
| **Aprovação de Não-Doutor** | non_phd_approval_level | 'cpg_qualified' (2/3 da CPG) | 'cpg_simple' ou 'superior_council' |
| **Modalidade da Sessão Defesa** | defense_location_policy | 'hybrid_allowed' (Aluno na Sede) | 'onsite_mandatory' ou 'fully_remote_allowed' |

### **5. Roteiro Prático para a Reunião de Validação (Checklist CPG-MP)**

Para conduzir a pauta de homologação do Macroprocesso 01 com a coordenação e a CPG do MPTRCS, recomenda-se passar pelos seguintes quatro pontos de confirmação:

1. **Confirmação da Régua de Créditos:**
 * Ratificar a meta de 100 créditos (40 disciplinas, 8 seminários, 52 dissertação) e a equivalência de 15 horas por crédito.
2. **Homologação das Disciplinas Obrigatórias Gerais:**
 * Confirmar a vinculação compulsória das disciplinas MP-01 e MP-02 a todos os ingressantes do programa.
3. **Aprovação do Fluxo de PTT V1 (cpg_checklist):**
 * Chancelar o procedimento no qual o aluno seleciona a entrega no checklist do portal, colhe a anuência eletrônica do Orientador/Coorientador, passa pela triagem da Secretaria e recebe a autorização de defesa na pauta da CPG.
4. **Validação das Regras da Comissão Julgadora de Defesa:**
 * Confirmar a banca de 3 Doutores (orientador preside e vota, coorientador não vota simultaneamente e no mínimo 1 membro externo ao IPEN/CNEN), a janela de 15 dias para agendamento e o prazo de 30 dias pós-defesa para depósito no repositório.
