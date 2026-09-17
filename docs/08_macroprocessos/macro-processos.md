Abaixo está a modelagem completa, integral e detalhada dos **10 Macroprocessos Acadêmicos** para a implementação do ERP Educacional (OpenEduCat), incorporando todas as correções de arquitetura, validações regimentais e adendos de parametrização multirregimental.

Nenhum fluxo foi suprimido ou resumido, garantindo que a equipe de engenharia de software e a secretaria acadêmica tenham a especificação exata para a parametrização do sistema e o atendimento às exigências do GoPG da CAPES.

---

## Macroprocesso 01: Governança Regimental e Setup Curricular

Este é o processo fundacional de back-office. Antes de qualquer edital ser publicado ou qualquer aluno ingressar, a coordenação do programa e a secretaria acadêmica definem o ambiente normativo isolado que governará uma geração de discentes, garantindo a rastreabilidade, a prevenção do hibridismo normativo e a tutela inabalável do Ato Jurídico Perfeito.

* **Criação do Versionamento Curricular (`op.curriculum.version`):** A coordenação cadastra uma nova versão de currículo no ERP, estabelecendo uma relação One2many com o programa acadêmico (`op.program.capes`). Cada novo discente que ingressar sob a vigência desta norma receberá em seu perfil (`op.student`) o campo relacional obrigatório e irrevogável `curriculum_version_id`, blindando a base de dados contra a dubiedade normativa.
* **Parametrização Cronológica e Limites Temporais:** O motor de versionamento é configurado com os limites de tempo regimentais:
  * *Prazo Máximo de Titulação (`max_months_defense`):* Configurado em meses conforme o nível (ex: 24 meses para Mestrado e 48 para Doutorado).
  * *Prazos de Prorrogação:* Parametrização do teto máximo de extensão (ex: até 90 dias no IPEN, ou até 6 e 12 meses no CDTN e Mackenzie).
  * *Prazo de Depósito Final (`max_days_post_defense_deposit`):* Definido em dias pós-defesa (ex: 30 dias no IPEN/Mackenzie vs. 90 dias no CDTN).
* **Fator de Conversão de Carga Horária e Escalas de Nota:**
  * *Conversão de Crédito:* Parametrização onde 1 crédito equivale a 15h (IPEN/CDTN), 12h (Mackenzie Computação) ou 10h (Mackenzie ADN).
  * *Escala de Avaliação (`grading_scale_type`):* Definição da regra de conceitos (A, B, C, R com aprovação até C vs. A, B, C, D, R, F com D aprovado no CDTN).
* **Parametrização do Motor de Integralização de Créditos:** Definição das metas quantitativas que balizarão o Livro-Razão Acadêmico (`op.student.credit.ledger`):
  * *Carga Total Exigida:* Fixada na meta global do programa (ex: 100 créditos no MPTRCS/IPEN, 50 no Mackenzie Computação, 60 no Mackenzie ADN, 24/47 no CDTN).
  * *Matriz de Distribuição Obrigatória:* Divisão da integralização em silos/buckets parametrizáveis.
  * *Tetos de Aproveitamento Externo e Produção Técnica:* Configuração das propriedades de validação em Python: teto de disciplinas externas (ex: até 50% no IPEN vs. 40% no Mackenzie) e bonificação por produções (teto de 25%).
  * *Governança de Alunos Especiais:* Parametrização regimental de permissão (`allow_special_students`, default `False` para MPTRCS), teto de disciplinas isoladas (`max_special_subjects_limit`), prazo decadencial de aproveitamento (`special_credit_validity_months`, padrão 36 meses), fluxo deliberativo CPG e política de reprovações (`special_transcript_fail_policy = 'omit_on_regular'`).
  * *Governança Intra-IES vs. Extra-IES:* Configuração da permissão de créditos intra-IES (`allow_intra_ies_credits`) com 100% de equivalência nominal e teto `max_intra_ies_credits_percent`. No IPEN, o programa de Tecnologia Nuclear (titulado pela USP) é parametrizado como extra-IES, exigindo aprovação prévia da CPG e submissão ao teto externo.
* **Parametrização de Proficiência Linguística (`proficiency_stage`):**
  * Configuração do gatilho: `admission` (matrícula inicial - IPEN), `qualification` ou `defense`.
* **Parametrização Dinâmica de Disciplinas Obrigatórias (`op.curriculum.subject.rule`):**
  * Eliminação de códigos fixos em código. Obrigatoriedade gerenciada por tabela de regras com escopo de Programa ou por Área de Concentração (`area_id`).
* **Parametrização do Estágio de Docência / Supervisionado (`teaching_internship_mode` - Portaria CAPES nº 221/2025):**
  * Configuração flexível: `not_applicable` (Cursos Profissionais/Isentos), `scholarship_only` (Apenas Bolsistas), `mandatory_all` (Todos), ou `flexible_equivalence` (Permite Estágio Supervisionado / Equivalentes).
* **Flexibilização da Trava de Produto Técnico-Tecnológico (`ptt_validation_mode`):**
  * `cpg_checklist` (Checklist + Dupla Anuência Orientadores + Homologação CPG no requerimento de defesa), `qualis_prior` (Estrato Qualis T1-T5 prévio), ou `none` (Cursos Acadêmicos).
* **Parametrização das Regras de Comissão Julgadora (`op.curriculum.committee.rule`):**
  * Definição de quórum de titulares e suplentes, direito a voto do Orientador/Coorientador, regras de endogenia e política de presença (presencial, híbrida ou 100% remota).
* **Migração de Regimento (Tutela do Ato Jurídico Perfeito e Direito de Opção):**
  * *Acionamento via Portal:* Requerimento `op.academic.request.regime_migration` no Portal do Aluno com quadro comparativo e assinatura de termo irrevogável.
  * *Execução Algorítmica:* Encerramento da leitura na versão anterior (preservando o Ato Jurídico Perfeito) e reabertura na nova chave `curriculum_version_id`.

---

## Macroprocesso 02: Admissão e Ingresso (Fluxo do Edital, Proficiência e Matrículas)

Abandona-se a matrícula direta e manual em favor da concorrência pública parametrizada pelo sistema, garantindo transparência auditável e conformidade com as diretrizes da CAPES. Este fluxo orquestra o ciclo completo de captação, avaliação qualitativa e quantitativa de candidatos, consolidação do vínculo acadêmico e definição inicial do escopo de pesquisa.

**2.1. Parametrização do Certame e Gestão de Turmas (Cohorts)**

* **Cadastro do Edital (`op.admission.edital`):** A secretaria acadêmica cadastra o edital no ERP, definindo o período de inscrições, taxas operacionais e a distribuição de vagas, atrelando-as diretamente às Linhas de Pesquisa e aos Orientadores credenciados no programa.
* **Entidade de Turma:** O sistema cria a entidade central de agrupamento denominada "Turma" (ex: Turma 07, Turma 08), que atuará como a âncora cronológica irrevogável para todos os ingressantes daquele ciclo.
* **Ações Afirmativas:** O sistema reserva percentuais obrigatórios das vagas oferecidas para políticas de ações afirmativas (ex: 20%), destinadas a candidatos autodeclarados pretos, pardos, indígenas ou com deficiência.
* **Edital de Vagas Remanescentes:** Caso haja ociosidade após o primeiro processo, o ERP permite a duplicação rápida das regras do certame para lançar um edital de vagas remanescentes. Os candidatos aprovados neste segundo certame são vinculados sistemicamente à mesma "Turma" do edital original, equalizando os prazos de titulação e os fluxos letivos com o restante do grupo.

**2.2. Captação e Triagem Documental (Portal do Candidato)**

* **Upload Documental:** O candidato acessa o portal e realiza o upload dos arquivos exigidos em PDF, incluindo formulário de inscrição, foto 3x4, diploma de graduação (ou atestado de conclusão), histórico escolar e documentos de identificação.
* **Vínculo Lattes e Proficiência:** O ERP exige o preenchimento obrigatório da URL para o currículo na Plataforma Lattes e o upload do Certificado de Proficiência Linguística.
* **Pré-projeto e Termos:** O candidato submete a proposta de pré-projeto de pesquisa, indicando a área de concentração, as linhas de pesquisa pretendidas e o nome de um possível orientador, além do Termo de Compromisso assinado atestando disponibilidade de carga horária presencial.
* **Autoavaliação e Cotas:** O candidato anexa a planilha de autoavaliação do currículo Lattes (para o cálculo inicial de pontos) e, caso seja optante pelas cotas, a autodeclaração étnico-racial ou o relatório médico comprobatório.

**2.3. Máquina de Estados do Processo Seletivo (Workflow de Avaliação, Arguição e Exceção)**

* **Etapas Preliminares (Provas e Análises):**
* A secretaria insere no sistema as notas brutas da Prova Objetiva de Conhecimentos e valida os certificados de proficiência. Candidatos estrangeiros recebem um alerta sistêmico exigindo aprovação em proficiência tanto de Inglês quanto de Português.
* O sistema processa a Análise Curricular (Lattes) e do Pré-projeto, aplicando o peso configurado (ex: Peso 2). O algoritmo calcula quem atingiu as notas de corte e sugere o status "Aprovado para Entrevista" ou "Reprovado".


* **Entrevista Qualitativa com a CPG (Etapa 3):**
* O ERP disponibiliza um painel específico (Rubrica de Avaliação) para a sub-comissão da CPG durante as entrevistas. O avaliador insere a nota numérica (ex: Peso 3) e preenche campos qualitativos parametrizados (escala de 1 a 5): Maturidade Profissional, Alinhamento com o Setor Produtivo e Potencial de Geração do PTT. O sistema consolida o Score Final.


* **O Gatilho de Soberania da Coordenação (Override Estratégico):**
* Se um candidato estratégico for reprovado por critérios estritamente teóricos, o Coordenador do Programa (via administrador acadêmico) aciona o botão "Aprovação em Caráter Excepcional (Override)".
* O sistema exige preenchimento obrigatório de um campo de texto livre para a redação da justificativa em ata, mudando o status do candidato para "Aprovado (Exceção CPG)". O ERP registra a ação no log de auditoria de segurança (timestamp e usuário) e pode configurar pendências condicionais futuras.


* **Auditoria de Recursos:** O workflow do sistema prevê travas que respeitam períodos formais de recursos operados via painel (após inscrições deferidas e após a lista final).

**2.4. Transição de Estado, Trava de Proficiência e Matrícula Regular**

* Ao final do certame, o status muda para a condição intermediária de "Candidato Aprovado".
* **Trava Dura de Proficiência na Matrícula (IPEN):** Durante o procedimento de conversão para Aluno Regular (`op.student`), se o regimento ativo definir `proficiency_stage = 'admission'`, o Odoo impede a geração da matrícula e do registro discente caso a proficiência em Inglês/Português não esteja deferida.
* **Início do Relógio:** A efetivação da matrícula dispara o relógio cronológico oficial (24 meses).
* **Gatilho de Evasão Precoce:** O sistema inicia um monitoramento de assiduidade inicial. Alunos matriculados que não registrarem presença (sem justificativa comprovada atestada no portal) nas três primeiras semanas letivas terão a matrícula sumariamente cancelada (status "Desistente"). O sistema notificará a secretaria para convocar imediatamente o próximo candidato da lista de espera.
* **Preenchimento Obrigatório do Perfil Profissional (Baseline de Egressos):** Para atender às diretrizes da CAPES relativas ao impacto e inserção profissional de titulados em programas acadêmicos e profissionais, o sistema impõe uma etapa final de matrícula onde o ingressante declara dados corporativos (empresa, setor, porte, cargo, tempo de casa, alinhamento com o mestrado e faixa salarial), concedendo anuência por meio de aceite digital auditável (`capes_terms_accepted`) para fins de prestação de contas estatística.

**2.5. Associação de Orientação Sistêmica (Primeiro Semestre)**

* O fluxo de vinculação deve ser formalizado no sistema preferencialmente até o 3º mês letivo. O aluno acessa o portal e seleciona seu orientador (e coorientador) na lista de docentes.
* O sistema envia notificações internas e e-mails. O orientador clica em "Aceitar Orientação".
* A secretaria atua como última barreira de auditoria, confere os limites regimentais de alunos por docente e homologa o vínculo.

**2.6. Submissão, Workflow de Avaliação e CEP do Plano de Trabalho**

* O discente preenche os metadados e submete o PDF do Plano de Trabalho via Portal.
* **OK do Orientador:** O plano transita para `waiting_advisor`. O orientador deve revisar e dar seu "OK / Aprovação" eletrônico no sistema para liberar o envio à secretaria.
* **Pauta CPG e Parecerista:** A secretaria realiza a triagem e inclui o plano na pauta da reunião da CPG. O colegiado indica o parecerista/avaliador, e a secretaria cadastra a atribuição no ERP.
* **Emissão do Parecer:** O avaliador acessa o dossiê e seleciona obrigatoriamente uma das 4 alternativas:
1. *Aprovado:* Liberado para homologação.
2. *Aprovado com Revisões:* Retorna para ajustes do aluno, exige novo OK do orientador e reavaliação do parecerista.
3. *Aprovado com Pendência CEP:* Recebe status condicional. O Odoo trava o agendamento de bancas intermediárias/defesa até o upload do parecer aprovado do CEP/CEUA.
4. *Reprovado sem Direito a Revisão:* Encaminhado à CPG para deliberação sobre novo tema ou desligamento.


* **Homologação Sistêmica:** A homologação final do plano pela CPG atua como chave de destravamento da carreira acadêmica do aluno.

**2.7. Adendo de Matrículas Especiais (Disciplinas Isoladas)**

* O sistema disponibiliza um fluxo de admissão não conducente a título para candidatos em disciplinas isoladas.
* **Emissão do RA Perene:** O candidato recebe um Registro Acadêmico (RA) definitivo da IES em `op.student`, unívoco por CPF e mantido perenemente mesmo se futuramente o aluno ingressar como regular.
* **Governança Regimental:** O ERP checa a permissão regimental do programa (`allow_special_students`), sendo desabilitada por padrão no MPTRCS. Nos programas que permitem, a matrícula exige aceite do docente (`special_student_instructor_consent_required`) e respeito à cota de vagas (`special_seats_quota`).
* **Livro-Razão em Quarentena:** As disciplinas concluídas com êxito são gravadas como `subject_special_quarantine`, servindo apenas para emissão de certidão de disciplinas isoladas. Não entram em cálculos de titulação regular até que ocorra posterior aprovação em processo seletivo e homologação de aproveitamento pela CPG dentro do prazo decadencial de 36 meses.
* **Expurgo de Reprovações:** Reprovações ocorridas sob vínculo de aluno especial não contam para jubilação do curso regular e não constam no histórico oficial de conclusão (política `omit_on_regular`).

---

---

## Macroprocesso 03: Vida Estudantil e Matrículas em Disciplinas

Gerencia a operacionalização do dia a dia letivo, desde a oferta de turmas até a consolidação imutável do histórico escolar, prevendo prazos rígidos de execução e fluxos de exceção para demandas jurídicas ou colegiadas.

**3.1. Oferta de Turmas, Parametrização de Capacidade e Docência**

* A secretaria cadastra as turmas parametrizando a **Capacidade Máxima** e a **Capacidade Mínima (Quórum)**. Se não atingir o quórum, o sistema emite alerta, cancela a turma e notifica os alunos.
* **Composição de Equipe Docente:** O ERP permitirá que o Coordenador da disciplina (docente permanente) vincule à turma até 3 (três) outros professores portadores do título de Doutor (permanentes ou colaboradores).
* O sistema configura o **Prazo de Matrícula** fixado no calendário acadêmico.

**3.2. Inscrição Semestral em Disciplinas, Trava de Calouros e Matrículas Intra-IES**

* **Disciplinas Regulares:** O aluno seleciona o elenco de turmas ofertadas. O ERP submete a grade à validação eletrônica do orientador e homologação da secretaria.
* **Matrículas Intra-IES:** O discente pode requerer matrícula em turmas de outros PPGs da mesma IES mantenedora (`res.company`). O processo exige anuência do orientador e aceite do docente responsável. Os créditos integralizados contam com 100% de peso nominal, respeitando o teto `max_intra_ies_credits_percent`. No IPEN, disciplinas da Tecnologia Nuclear (USP) são consideradas extra-IES e requerem validação pela CPG.
* **Trava de Matrícula Inicial:** No semestre de admissão (calouros), o algoritmo impedirá a finalização da matrícula caso a seleção de disciplinas seja inferior ao mínimo parametrizado no regimento (`min_first_semester_credits`, ex: 24 créditos no IPEN MPTRCS).
* **Matrícula de Acompanhamento (Ato Estudantil):** Alunos que concluíram os créditos teóricos devem, semestralmente, solicitar via portal a matrícula na atividade de "Elaboração de Dissertação", submetendo-se à validação do orientador e homologação da secretaria.

**3.3. Cancelamento de Matrícula em Disciplina (Artigo 41º do MPTRCS e Anuência Tácita)**

* **Parametrização do Calendário:** A secretaria define a regra de prazo de cancelamento por disciplina ou de forma global/por dias corridos a partir do início das aulas.
* **Fluxo de Solicitação e Anuência:** O estudante protocola o pedido de cancelamento via Portal do Aluno dentro do prazo regulamentar. O ERP aciona o orientador para anuência obrigatória.
* **Mecanismo de Anuência Tácita (SLA do Orientador):** Se o pedido do aluno for protocolado no prazo, mas o orientador ultrapassar o SLA estipulado para resposta sem manifestação contrária, o sistema aplica o deferimento automático por anuência tácita, protegendo o direito do discente de acordo com o Artigo 41º do regulamento.
* **Efeitos Acadêmicos:** O cancelamento efetivado retira a disciplina do histórico escolar sem atribuição de conceito "R", mantendo inalterados os prazos máximos regimentais de conclusão do curso.

**3.4. Frequência, Lançamento de Notas e Prazos Operacionais**

* O docente registra comparecimento e notas. O sistema aplica a trava de assiduidade de 75% (reprovação automática por falta).
* O sistema monitora o prazo limite para que os professores lancem as notas e conceitos finais (A, B, C ou R). Após o prazo, o diário eletrônico é bloqueado.
* A secretaria possui uma janela temporal para revisar os diários, verificar inconsistências e comandar o encerramento da turma no sistema.

**3.5. Consolidação no Livro-Razão Acadêmico (Ato Finalizado)**

* Ao acionar a consolidação, a secretaria transforma os conceitos em um ato finalizado. O sistema injeta os créditos na tabela *append-only* do Livro-Razão (`op.student.credit.ledger`). Os registros tornam-se nativamente imutáveis e categorizados:
  * `subject_internal`: Disciplinas regulares do PPG do aluno.
  * `subject_intra_ies`: Disciplinas de outros programas da mesma instituição mantenedora.
  * `subject_special_quarantine`: Disciplinas cursadas sob vínculo de Aluno Especial, mantidas em quarentena.

**3.6. Ajuste Manual Retroativo (Fluxo de Exceção e Demandas Judiciais)**

* Para demandas jurídicas ou retificações fundamentadas da CPG, o professor inicia um requerimento no sistema informando: Nome/Matrícula do aluno, Disciplina/Semestre, Coordenador, Solicitante, Nota original, Nota pretendida e a descrição pormenorizada com upload obrigatório de provas documentais.
* O pedido é roteado para a Coordenação do Programa. Somente após a aprovação eletrônica do Coordenador, o fluxo retorna à secretaria, que executa o lançamento efetivo.
* O ERP sobrepõe o dado no Livro-Razão, gerando um selo de auditoria indelével (exibindo todo o rastro da alteração) para proteger a instituição.

---

---

## Macroprocesso 04: Requerimentos, Vigilância Cronológica e Jubilamento

Executa uma vigilância algorítmica sobre os prazos de titulação e desligamento, fornecendo ferramentas para gerenciar contingências institucionais, pandemias ou decisões judiciais.

**4.1. Solicitação e Deliberação Colegiada de Trancamento de Matrícula**

* **Iniciação via Portal:** O aluno protocola a suspensão no Portal do Aluno anexando a documentação comprobatória obrigatória (atestados, portarias ou laudos).
* **Esteira Obrigatória de Aprovação da CPG:** Diferente de fluxos automatizados de dispensa, todo requerimento de trancamento e prorrogação exige obrigatoriamente a deliberação e aprovação da CPG. Após a triagem formal da secretaria (`waiting_screening` -> `ready_for_agenda`), o pedido é pautado na reunião do colegiado (`op.cpg.meeting`).
* **Parâmetros e Limites:** O sistema valida o teto contínuo de trancamento regimental (`max_trancamento_days`, ex: 365 dias) e checa a permissão de período inicial (`block_first_semester_trancamento`).
* **Execução Autônoma Pós-Ata:** Após o "Clique Auditável" dos membros da CPG na Ata em QWeb, o ERP executa autonomamente o deferimento, atualizando o status do aluno e pausando o relógio de prazos.
* **Retorno e Ato Jurídico Perfeito (Art. 23º):** Ao retornar do trancamento, o discente é vinculado à estrutura curricular vigente na data de retorno (`retorno_rule`). O sistema preserva integralmente as notas e créditos obtidos anteriormente no Livro-Razão (`op.student.credit.ledger`), mas submete o aluno às normas vigentes para as etapas futuras, vedando o hibridismo normativo. 
* **Exceções Autoritativas (Override):** Para trancamentos que excedem os limites regimentais (ex: pandemia), o sistema exige a vinculação da Portaria do Conselho Superior/CPG e do Parecer favorável. Esse ato fica permanentemente registrado no prontuário do aluno como "Exceção Administrativa Auditável" (`op.administrative.override`), garantindo que, durante uma auditoria, o IPEN possa provar que a quebra de prazo foi um ato legal e fundamentado.


**4.2. Requerimento de Prorrogação de Prazos (Fracionado)**

* O discente e orientador abrem o chamado de extensão cronológica no ERP.
* O sistema submete o pedido a pré-requisitos parametrizáveis (ex: obrigatoriedade de integralização teórica prévia e qualificação aprovada).
* As prorrogações podem ser fracionadas. O algoritmo soma as frações e barra submissões cujo total ultrapasse o teto regimental padrão de (`max_extension_days`) dias para conclusão.

**4.3. Exceções Autoritativas (O Gatilho de Soberania da CPG e da CAPES)**

* **Override de Exceções:** Implementado módulo de `op.administrative.override`. Toda exceção (ex: trancamento ou prorrogação de prazo ou prazo de credenciamento docente acima dos limites regimentais) é tratada como um ato administrativo que exige: 1) Documento legal (Portaria/Ata); 2) Deliberação do Conselho Superior/CPG; 3) Registro no log de auditoria do aluno/docente. O sistema nunca altera datas de vencimento sem vincular o `override_id` ao `meeting_id` da aprovação colegiada.


**4.4. Vigilância de Prazos e Jubilamento Sistêmico (Cron Job Contínuo)**

* Um script diário (Cron Job) varre os relógios dos perfis de alunos.
* Estudantes que ultrapassarem o limite regimental padrão (`curriculum_version_id`) (somados dias de trancamento, prorrogações regulares e extensões autoritativas) sem depósito de dissertação são bloqueados e movidos para "Pendente de Desligamento por Prazos".
* O algoritmo também desliga automaticamente alunos que atingirem limites de falha (ex: duas reprovações em disciplinas, duas reprovações no Seminário Geral) ou abandono formalizado por ausência injustificada.

**4.5. Portal, Requerimentos e Governança da CPG**

* A CPG é a instância final de decisão para trancamentos e prorrogações excepcionais.
* Triagem (Secretaria): O chamado entra em `waiting_screening`.
* Reunião da CPG: O item é puxado para pauta (`op.cpg.meeting`).
* Template de Ata (QWeb): Sistema compila a ata automaticamente.
* Clique Auditável: Aprovação eletrônica com User ID, Timestamp e IP.
* Gatilho de Execução: Após aprovação, o sistema injeta os dias de prorrogação ou atualiza o status (trancamento).

---

## Macroprocesso 05: Gestão de PTTs (Mestrados/Doutorados Profissionais)

Processo que orquestra todo o ciclo de vida da produção aplicada (Produto Técnico-Tecnológico), desde a sua proposição até a estratificação no Qualis Tecnológico da CAPES, servindo como condicionante de defesa.

**5.1. Submissão e Tipologia do Produto Técnico-Tecnológico (PTT)**

* O ERP exige o registro formal do PTT gerado como pré-requisito para o depósito da dissertação.
* O autor preenche os metadados estruturados de sua produção. O menu *dropdown* do sistema reflete a taxonomia exata do Comitê Medicina II da CAPES, permitindo classificar e anexar evidências para:
* Ativos de propriedade intelectual (registro de software, patente).
* Artigo científico a ser publicado em revista indexada na base Web of Science.
* Empresa ou organização social inovadora.
* Curso de formação profissional.
* Norma ou marco regulatório.
* Relatório técnico conclusivo.
* Manual/Protocolo.
* Base de dados técnico-científica.
* Produto de editoração.
* Processos, tecnologias, produtos ou materiais não patenteáveis.



**5.2. Auditoria de Aderência e Trava Eliminatória (TNC)**

* O orientador e/ou coordenação realiza uma auditoria técnica. Avalia-se se o produto adere estritamente ao plano de trabalho e linha de pesquisa.
* Se rejeitado por falta de impacto ou inovação, o ERP atribui o status TNC (Trabalho Não Conforme), impedindo que o aluno contabilize créditos de produção ou avance para a defesa final.

**5.3. Avaliação e Estratificação no Qualis Tecnológico**

* Produtos aderentes são avaliados em quatro dimensões obrigatórias: Impacto, Inovação, Aplicabilidade (escala TRL) e Complexidade.
* O ERP processa a pontuação ponderada das dimensões e calcula o estrato oficial do produto, classificando-o em uma escala de T1 (mais elevado) a T5 (menor impacto).

**5.4. Validação Documental de Entrega e Injeção de Créditos**

* A homologação do PTT gera créditos por publicação/produto (se permitido pelo plano curricular), injetando até 25% de créditos no Livro-Razão (condicionado a aprovações da CPG).
* Se a chave curricular exigir o PTT, a homologação de seu estrato atua como chave de desbloqueio liberando o depósito da dissertação.

---

## Macroprocesso 06: Ritos de Titulação (Marcos Intermediários e Defesa Final)

Orquestra os ritos acadêmicos de passagem e consolidação do grau, aplicando rigorosas auditorias de quórum, endogenia e pré-requisitos curriculares.

**6.1. Travas Prévias de Elegibilidade para Defesa Final**

* O ERP bloqueia o workflow de agendamento da defesa até a verificação de:
  1. *Plano de Trabalho Homologado:* Confirmação de homologação pela CPG do `op.student.work_plan`.
  2. *Trava Ética:* Validação de aprovação do CEP/CEUA, se requerida pelo plano.
  3. *Proficiência Linguística:* Status aprovado conforme o momento exigido pelo regimento.
  4. *Integralização e Disciplinas Obrigatórias:* Cumprimento dos créditos e aprovação nas disciplinas obrigatórias (gerais e da Área de Concentração do discente).
  5. *Validação do PTT:* Confirmação do fluxo de PTT configurado no regimento (`ptt_validation_mode`), verificando no Modo V1 a dupla anuência do Orientador/Coorientador e a homologação formal aprovada em pauta da CPG.
  6. *Estágio de Docência / Supervisionado:* Validação da regra do regimento (`teaching_internship_mode` - Portaria CAPES nº 221/2025). Trava desativada automaticamente para cursos profissionais ou regimentos isentos.

**6.3. Depósito da Dissertação e Validação de Banca de Defesa**

* O orientador atesta a aptidão do trabalho e submete a proposta de banca examinadora no ERP com antecedência parametrizada no regimento (ex: 15 ou 30 dias).
* **Auditoria Paramétrica da Comissão Julgadora (`op.curriculum.committee.rule`):**
  * Validação do quórum de titulares (3 ou 5 membros) e suplentes conforme a regra ativa do programa (par fixo vs. 1 por titular).
  * Aplicação da regra de voto do Orientador (Votante no IPEN/Mackenzie vs. Não-Votante no CDTN).
  * Validação da participação de membros externos ao PPG/IES conforme a exigência do regimento.
  * Checagem de impedimentos por parentesco cível até 4º grau.

**6.4. Sessão de Julgamento, Modalidades, Validação da Versão Final e Depósito pela Biblioteca**

* **Modalidade:** Presencial, híbrida ou totalmente remota, conforme parametrizado em `defense_location_policy`.
* **Dinâmica Temporal:** Registro dos tempos de exposição e arguição configurados no regimento.
* **Upload da Versão Final pelo Discente (Portal):** Após a aprovação na defesa, o status altera para `deposit_pending`. O discente dispõe do prazo limite regimental (`max_days_post_defense_deposit`, ex: 30 dias) para efetuar as correções solicitadas pela banca e realizar o upload da versão final corrigida do PDF no Portal do Aluno (incluindo capa, folha de aprovação e ficha catalográfica). O status altera para `final_version_submitted`.
* **Triagem da Secretaria e Deferimento de Titulação:** A secretaria acadêmica verifica a conformidade técnica e de formatação do PDF. Ao conceder o aceite formal ("De acordo em Depósito da Versão Final"), o ERP altera autonomamente a situação da tese para `homologated` e a condição do discente para **"Titulado"**, liberando a expedição do Histórico Escolar Consolidado e a esteira de titulação.
* **Geração do Manifesto de Metadados e Envio à Biblioteca:** O ERP gera automaticamente o **Documento/Guia de Metadados para o DSpace (Manifesto OAI-PMH)** contendo todos os PIDs, resumos bilíngues, banca e autor. A secretaria encaminha a ordem de serviço com o PDF validado para a **Biblioteca Central**, que realiza exclusivamente o upload oficial no Repositório Institucional DSpace (Fonte Ouro).
* **Averbação do Handle:** A biblioteca aprova o depósito no DSpace e informa o Handle (URI) permanente gerado, que é averbado no campo `repository_url` no Odoo para fechamento da malha de interoperabilidade.

---

## Macroprocesso 07: Consolidação do Pacote de Titulação, Registro Interinstitucional (USP) e Expedição (Digital / Físico)

Processo integrado de auditoria de back-office e consolidação documental para encerramento do vínculo acadêmico, operacionalizado para atender tanto instituições com autonomia registradora direta quanto institutos de pesquisa (como o IPEN) que encaminham o registro para uma Universidade Registradora Externa (como a USP), com suporte a diplomas digitais (Portaria MEC nº 70/2025) e físicos em papel com Livro de Registro.

* **Geração de Histórico Escolar Consolidado e Auditável (IPEN):** O módulo de emissão compila o relatório oficial de notas e créditos do discente acessando diretamente as tabelas *append-only* do `op.student.credit.ledger`. O documento exibe de forma detalhada o título final da dissertação defendida, a composição completa da banca examinadora (identificando os membros externos) e a carga horária em horas convertida de acordo com o fator do regimento do aluno (ex: 100 créditos = 1.500 horas de atividades no IPEN). Em conformidade com a política regimental (`special_transcript_fail_policy = 'omit_on_regular'`), o histórico oficial de titulação omite reprovações e créditos avulsos não aproveitados cursados no passado como aluno especial, listando unicamente as disciplinas formalmente integradas ao percurso regular. O documento é selado com uma chave Hash SHA-256 e QR Code de verificação pública.
* **Empacotamento do Dossiê e Remessa Interinstitucional (IPEN $\rightarrow$ USP):** O OpenEduCat compila o **Pacote de Titulação** contendo o histórico validado, a ata de defesa assinada e o link do DSpace (Handle/URI). Nos casos de institutos de pesquisa como o IPEN, o sistema gera o protocolo de remessa física/digital (`physical_dispatch_date`) para averbação na Pró-Reitoria de Pós-Graduação da Universidade Registradora (USP).
* **Averbação do Registro e Expedição (Papel / Nato-Digital):**
    * *Modalidade Físico em Papel (`paper_hybrid`):* Registro do número do Livro de Registro (`registration_book_number`) e da Folha (`registration_page_number`) emitidos pela USP, com arquivamento do dossiê físico/digital.
    * *Modalidade Nato-Digital (`digital` - MEC 70/2025):* Geração dos esquemas XML federais, aplicação de envelope criptográfico XAdES-BES (ICP-Brasil) com Carimbo de Tempo e emissão da Representação Visual (RVDD) com QR Code.

---

## Macroprocesso 08: Interoperabilidade e Envio de Dados (GoPG/CAPES)

O processo contínuo de integração de back-office que ocorre nos bastidores do ERP, estruturado para extrair, transformar e transmitir os metadados da produção intelectual e da vida acadêmica diretamente para as plataformas analíticas da CAPES (GoPG - Governança da Pós-Graduação, Plataforma Sucupira e Rede RICA|PG).

* **Provisionamento da Fonte Ouro (Repositório Institucional e OAI-PMH):**
* *Sincronização com DSpace:* Quando uma dissertação e seu respectivo PTT são homologados no Macroprocesso 06, o ERP dispara uma integração via API REST para o repositório institucional (ex: DSpace do IPEN). O sistema exporta o arquivo integral do trabalho juntamente com o pacote de metadados padronizados segundo o protocolo de Dublin Core.
* *Exposição OAI-PMH:* O repositório expõe o protocolo de coleta *Open Archives Initiative Protocol for Metadata Harvesting* (OAI-PMH). O Odoo é parametrizado para formatar a saída utilizando o prefixo obrigatório **`oai_capes`**, assegurando que os robôs coletores do GoPG identifiquem corretamente o tipo de produção, área de avaliação (Medicinas II), linha de pesquisa e resumo bilíngue.
* *Gestão de Identificadores Persistentes (PIDs):* O sistema vincula e armazena chaves universais e imutáveis em cada registro: o **ORCID** (obrigatório para discentes e docentes orientadores), o **DOI** (*Digital Object Identifier*, atribuído automaticamente à dissertação e ao PTT) e o **ROR** (*Research Organization Registry*, identificando de forma unívoca o IPEN-CNEN/SP no cenário global).


* **Disponibilização da Fonte Prata (Endpoints RESTful para a Rede RICA|PG):** Para atender à modernização de coleta de dados da CAPES (que abandona a digitação manual na Plataforma Sucupira em prol da interoperabilidade automatizada), o módulo `l10n_br_openeducat_capes` implementa uma camada de APIs RESTful seguras no Odoo, funcionando como a "Fonte Prata" institucional:
* *Autenticação e Segurança:* Os endpoints são blindados por protocolo OAuth2 / mTLS (Mutual TLS), acessíveis exclusivamente pelos servidores autorizados da Rede de Interoperabilidade e Computação Científica da CAPES (RICA|PG).
* *Endpoints de Carga Acionados por Robôs:* O ERP responde a requisições automatizadas entregando cargas úteis (payloads) em formato JSON estritamente tipadas:
* `/api/capes/v1/students`: Entrega o perfil, etnia, gênero, ano de ingresso, situação da matrícula, chave de versão curricular (`curriculum_version_id`), regime de dedicação e dados de bolsas dos estudantes ativos e titulados.
* `/api/capes/v1/faculty`: Entrega o cadastro dos docentes permanentes, colaboradores e visitantes, com chaves do Lattes, período de credenciamento (que no IPEN é válido por até 2 anos) e carga horária ministrada em disciplinas.
* `/api/capes/v1/curriculums`: Expõe a matriz de disciplinas ativas, ementas, créditos, coordenadores de disciplina e o formato de oferta (presencial, híbrido ou convênio de cotutela/dupla titulação internacional).
* `/api/capes/v1/projects_and_ptts`: Exporta os projetos de pesquisa consolidados do programa, relacionando-os diretamente às dissertações defendidas e aos Produtos Técnico-Tecnológicos com seus respectivos estratos Qualis calculados no Macroprocesso 05, garantindo que o programa comprove sua excelência e aplicabilidade prática na avaliação quadrienal da CAPES.



---

## Macroprocesso 09: Gestão do Corpo Docente e Rastreabilidade GoPG

A documentação do GoPG e a Plataforma Sucupira exigem não apenas o retrato atual do corpo docente, mas o "filme" de sua vida acadêmica. A mudança de status deve ser preservada temporalmente, alimentando de forma limpa as APIs de interoperabilidade.

**9.1. Entidade de Vínculo Docente (`op.faculty.program.link`)**

* Em vez de adicionar um campo estático no cadastro base do funcionário (`hr.employee`), o sistema cria uma tabela relacional entre o Docente e o Programa (`op.program.capes`).
* Esta arquitetura permite que um mesmo professor atue concomitantemente como Docente Permanente no Mestrado Profissional do IPEN e como Docente Colaborador ou Visitante em outro programa da base (ex: CDTN ou Mackenzie), sem gerar conflito de dados na exportação para a CAPES.

**9.2. O Livro-Razão de Categorias (Timeline de Credenciamento)**

* Abaixo do vínculo principal, o sistema implementa uma estrutura *append-only* (apenas inserção) chamada `op.faculty.category.ledger`.
* Quando a CPG delibera sobre o credenciamento ou recredenciamento de um docente, a secretaria insere um novo registro contendo:
* **Categoria:** Permanente, Colaborador, Visitante ou Assistente.
* **Período de Vigência:** Data de Início e Data de Fim (refletindo o prazo de credenciamento, que no MPTRCS é válido por até 2 anos).
* **Documento Comprobatório:** Anexo em PDF (ou link referencial) da ata/portaria de aprovação.


* *Endpoint GoPG:* Quando o robô da CAPES acessar a API da instituição, o ERP compilará um JSON varrendo esta tabela, informando o tempo exato em que o docente permaneceu em cada estrato, evitando glosas na avaliação.

**9.3. Gestão de Exceções e Override de Credenciamento**

Em situações excepcionais (ex: pandemia ou deliberações extraordinárias do Conselho Superior), o programa pode necessitar prorrogar credenciamentos fora dos prazos padrão.

* **Fluxo de Override (`op.administrative.override`):** O sistema permite uma excepcionalidade administrativa que não viola a imutabilidade do Ledger. A secretaria abre um requerimento de override anexando a Portaria do Conselho Superior/CPG.
* **Trava de Auditoria:** O sistema só permite a prorrogação se o `override_id` estiver vinculado a uma Ata da CPG (`op.cpg.meeting`) que contenha a deliberação de aprovação. O registro original de vencimento permanece, mas é anotado com uma referência de exceção, garantindo total transparência para auditorias externas.


**9.4. Painel de Produção e Orientação (Prevenção de Sobrecarga)**

* O módulo cruza automaticamente o vínculo do docente com o livro-razão de alunos regulares, monitorando em tempo real o número de orientandos ativos.
* O sistema emite um alerta se o docente atingir o limite regulamentar do programa (ex: limite de 8 alunos por orientador no IPEN, respeitando as diretrizes do Comitê Medicinas II da CAPES).

---

## Macroprocesso 10: Governança do Colegiado e Reuniões da CPG

Transforma o ERP na ferramenta oficial de orquestração do programa. Este macroprocesso modela desde a composição do conselho até a publicação de decisões, conectando os requerimentos dos alunos diretamente à pauta.

**10.1. Gestão da Composição da CPG (`op.cpg.committee` e `op.cpg.member`)**

* O sistema institui um módulo próprio para gerir o ciclo de vida do colegiado. Nenhuma reunião pode ser criada sem estar vinculada a uma composição de CPG vigente.
* **Cadastro de Composição:** A secretaria cria um registro para a gestão atual (ex: "Gestão CPG 2024-2027"), informando a data de início e a data de término do mandato (que no MPTRCS possui duração de 3 anos, com possibilidade de uma recondução).
* **Quadro de Membros:** Adicionam-se os membros especificando seus papéis e origens:
* *Cargos de Mesa:* Identificação de quem foi eleito como Coordenador e Vice-Coordenador da CPG.
* *Membros Titulares e Suplentes:* Cadastro dos representantes com título de Doutor.
* *Origem do Mandato:* O sistema registra se o membro foi "Eleito pelos Pares" (exigindo a data da eleição) ou "Indicado pelo Reitor/Conselho Superior" (exigindo o número da portaria de indicação).
* *Representação Discente:* Cadastro do membro discente (se aplicável na versão regimental em vigor), registrando a data da eleição estudantil e a duração diferenciada de seu mandato.


* **Histórico Institucional:** Ao trocar a gestão, a composição antiga não é deletada, mas recebe o status "Encerrada". Isso garante que reuniões passadas mantenham a integridade de quem eram os decisores da época.

**10.2. Triagem da Secretaria (A Esteira de Requerimentos)**

* Todos os chamados no Portal do Aluno que demandam deliberação colegiada (como aproveitamento de disciplinas cursadas como aluno especial `op.special.credit.incorporation.request`, prorrogações excepcionais de prazos, trancamentos fora do fluxo legal, homologação de planos de trabalho, equivalência de disciplinas extra-IES da USP, mudança de orientador sem anuência) caem em uma fila unificada no dashboard da secretaria com o status "Aguardando Triagem CPG".
* A secretaria atua como filtro técnico: confere a integridade dos documentos anexados e, com um clique, altera o status dos requerimentos aprovados na triagem para "Apto para Pauta".

**10.3. Orquestração da Reunião (`op.cpg.meeting`)**

* A secretaria cria um novo registro de reunião (Ordinária mensal ou Extraordinária), vinculando-a automaticamente à Composição da CPG vigente.
* **Composição da Pauta:** O ERP permite puxar para a reunião todos os requerimentos estudantis com status "Apto para Pauta" vindos da triagem. Adicionalmente, a secretaria possui autonomia para cadastrar e incluir diretamente itens administrativos de pauta livre (ex: homologação de credenciamentos docentes, propostas de disciplinas ou pautas institucionais extraordinárias). Todos os itens (sejam requerimentos discentes ou processos administrativos livres) recebem o mesmo tratamento de tramitação, deliberação, inclusão na Ata QWeb e votação por Clique Auditável.
* **Convocação Automatizada:** O sistema dispara um e-mail de convocação contendo a ordem do dia e os links de acesso seguro aos dossiês diretamente para os e-mails (ores painéis) dos membros titulares (ou de seus suplentes, em caso de vacância).

**10.4. O Motor de Template da Ata (QWeb)**

* Para garantir uma formatação institucional inabalável, o Odoo utilizará o seu motor de renderização (QWeb).
* Durante ou logo após a reunião, a secretaria registra o quórum de presença no sistema e preenche os campos de deliberação (ex: "Aprovado", "Indeferido", "Aprovado com ressalvas") ao lado de cada item da pauta.
* O sistema injeta essas deliberações, o cabeçalho institucional, a lista de presentes e os textos legais em um template HTML codificado, gerando um documento PDF limpo, padronizado e auditável.

**10.5. Workflow de Aprovação (Clique Auditável) e Publicação**

* Ao finalizar a redação do documento, a secretaria altera o status da reunião para "Em Aprovação".
* **Chancela Eletrônica Rastreável:** Cada membro da CPG registrado como "Presente" na reunião recebe uma notificação na central do ERP. Eles visualizam o PDF gerado e clicam no botão **"Aprovar Ata"**. O ERP grava o ID do usuário logado, a data, a hora e o endereço IP (Clique Auditável), suprindo a necessidade de assinaturas físicas ou tokens externos para rotinas internas.
* **Gatilho de Execução Sistêmica:** Uma vez que a ata alcança a aprovação unânime (ou da maioria qualificada configurada), o sistema dispara três ações autônomas:
1. *Feedback Operacional:* O status de todos os requerimentos estudantis inseridos na pauta avança automaticamente para "Deferido" ou "Indeferido", destravando as fases acadêmicas dos alunos e notificando-os em seus portais.
2. *Congelamento da Reunião:* O registro da reunião é travado contra edições (`readonly`).
3. *Transparência Ativa:* O PDF com o selo de auditoria interno recebe o status "Publicado" e pode ser disponibilizado na intranet ou no portal público do programa, assegurando total governança aos atos do IPEN.
