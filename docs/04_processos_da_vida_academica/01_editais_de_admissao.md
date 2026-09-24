# Documento 01: Editais de Admissão, Fases de Seleção e Workflow do Plano de Trabalho

## 1. O Paradigma da Concorrência Pública no Brasil

O processo nativo de admissão do OpenEduCat (`op.admission.register`) foi concebido para um modelo de "matrícula contínua" (*rolling admission*), típico de instituições de ensino privadas multinacionais. No Brasil, o ingresso na pós-graduação *Stricto Sensu* está vinculado a rigorosos princípios de impessoalidade, publicidade e concorrência pública, materializados na figura do **Edital de Seleção**.

A arquitetura do módulo `l10n_br_openeducat_capes_admission` substitui o fluxo linear nativo por uma máquina de estados parametrizável e auditável ancorada no modelo `op.admission.edital`.

## 2. Modelagem do Edital (`op.admission.edital`) e Gestão de Turmas (Cohorts)

Esta classe orquestra as regras do certame público, conectando a oferta de vagas às áreas de concentração, linhas de pesquisa, docentes credenciados e agrupamentos temporais de ingressantes.

* **Vinculação Regimental:** Cada edital nasce obrigatoriamente atrelado à versão do currículo vigente (`curriculum_version_id`), garantindo que os novos ingressantes sejam inseridos sob a tutela do Ato Jurídico Perfeito.
* **Gestão de Turmas (Cohorts) e Vagas Remanescentes:** O Edital cria a entidade de agrupamento "Turma" (ex: Turma 2026/1), que atua como âncora cronológica irrevogável. Em caso de ociosidade, o ERP permite duplicar o certame para "Vagas Remanescentes", atrelando os aprovados à mesma Turma original para equalização de prazos.
* **Reserva de Vagas (Ações Afirmativas):** Parametrização de cota obrigatória (ex: 20%) reservada a candidatos autodeclarados pretos, pardos, indígenas ou pessoas com deficiência (PcD), auditada através dos campos estendidos em `res.partner`.
* **Quadro de Vagas por Linha/Orientador (`op.edital.slot.distribution`):** As vagas são vinculadas na relação *One2many* do edital, mapeando a denominação da Linha de Pesquisa (`research_line`), o orientador responsável (`faculty_id` Many2one `op.faculty`) e a quantidade exata de vagas disponibilizadas (`slots`).

## 3. Fases de Seleção Dinâmicas e Trava de Proficiência na Admissão (`op.edital.phase`)

O sistema permite a configuração de `N` fases encadeadas através de uma relação *One2many*:

1. **Validação Documental:** Homologação da inscrição (conferência de diploma de graduação, histórico escolar e documentos civis).
2. **Análise de Currículo Lattes e Provas:** Computação objetiva da pontuação do Lattes e lançamento de notas de provas escritas.
3. **Trava de Proficiência Linguística na Admissão (Regra IPEN):** Quando o regimento atrelado ao edital possuir `proficiency_stage = 'admission'`, a aprovação e apresentação do certificado de proficiência em Língua Inglesa (e Português para estrangeiros) passa a ser condição **sine qua non** para a homologação do resultado.
4. **Entrevista Qualitativa e Rubrica CPG:** Painel de avaliação no ERP para a banca de entrevistas, com atribuição de notas de 1 a 5 nas dimensões: *Maturidade Profissional*, *Alinhamento com o Setor Produtivo/Linha de Pesquisa* e *Potencial de Geração de PTT*.

## 4. O Gatilho de Soberania do Coordenador (Override Estratégico)

Para situações em que um candidato de elevado valor acadêmico ou tecnológico para o programa seja reprovado por critérios estritamente teóricos, o Odoo disponibiliza ao Coordenador do Programa o botão de **"Aprovação em Caráter Excepcional (Override)"**.

* **Mecanismo de Auditoria:** Ao acionar o override, o campo booleano `is_override` é alterado para `True`, tornando obrigatório o preenchimento da justificativa técnica no campo `override_justification`.
* **Rastreabilidade e Log:** O ERP grava o ID do usuário, timestamp e registra um selo no log do sistema (`mail.thread`), alterando a situação do candidato para "Aprovado (Exceção CPG)".

## 5. Evasão Precoce, Vínculo de Orientação e Conversão de Matrícula

* **Trava de Conversão em Aluno Regular e Unicidade do RA (`op.student`):** Ao acionar o comando de conversão de candidato aprovado em aluno regular, o Odoo verifica o parâmetro `proficiency_stage`. Se configurado como `'admission'` (Modo IPEN), o sistema bloqueia a geração da matrícula caso o comprovante de proficiência não esteja deferido no dossiê do candidato.
* **Preservação da Identidade Soberana da IES (RA Único por CPF):** Durante a conversão, o motor de admissão busca se a pessoa física (`partner_id` / CPF) já possui cadastro discente prévio em `op.student` na instituição mantenedora (`res.company`):
  * *Discente já existente (ex: ex-Aluno Especial ou egresso):* O sistema **reutiliza obrigatoriamente** o registro de `op.student` e o **mesmo Registro Acadêmico (RA)** institucional perene. Cria-se um novo vínculo acadêmico em `op.student.course` atrelado ao programa de pós-graduação (ex: MPTRCS) e à versão curricular ativa (`curriculum_version_id`), preservando o histórico pregresso intacto.
  * *Discente novo:* O sistema gera o novo registro de `op.student` com RA institucional permanente gerado pela sequência sequencial da IES.
* **Gatilho de Evasão Precoce:** O sistema monitora a assiduidade nas primeiras 3 semanas letivas. Ingressantes sem registro de presença ou justificativa formal no portal têm a matrícula cancelada automaticamente como "Desistente", notificando a secretaria para convocar o próximo candidato da lista de espera.
* **Associação de Orientação:** A formalização do vínculo entre orientador/coorientador e discente deve ser executada no sistema impreterivelmente até o 3º mês letivo, mediante solicitação do aluno e aceite eletrônico do docente via portal.
* **Declaração de Perfil Profissional (Baseline de Egressos):** No momento da conversão de candidato aprovado em Aluno Regular (`op.student`), o sistema exige obrigatoriamente o preenchimento da ficha de perfil profissional e impacto da titulação (`capes.student.professional.profile`) no Portal do Aluno. O aceite formal dos termos de monitoramento da CAPES é restrição técnica para a emissão definitiva do registro acadêmico e relatórios de acompanhamento quadrienal.

## 6. Subprocesso 3.1: Submissão e Workflow do Plano de Trabalho (`op.student.work_plan`)

O Plano de Trabalho estabelece a proposta formal da pesquisa, o cronograma de execução e a previsão do Produto Técnico-Tecnológico (PTT). A evolução acadêmica do discente fica sistemicamente conditioned à aprovação e homologação deste plano.

### 6.1. Pré-requisitos para Submissão

1. O discente deve estar com o status "Matriculado Regular".
2. O vínculo de orientação (`advisor_id`) deve estar devidamente aceito e ativo no sistema.

### 6.2. Workflow Operacional Passo a Passo

```text
[Aluno: Submete PDF no Portal] 
               │
               ▼
[Orientador: Aceite / OK Eletrônico] ──(Rejeitado)──► [Devolvido ao Aluno]
               │
               ▼
[Secretaria: Fila de Triagem] ──► [Apto para Pauta CPG]
               │
               ▼
[CPG: Designa Parecerista / Avaliador]
               │
               ▼
[Avaliador: Emite Parecer no Sistema com Prazo]
               │
               ├─────────────────────────────────────────┐
               │                                         │
               ▼                                         ▼
      [a) Aprovado]                         [b) Aprovado c/ Revisões]
               │                                         │
               ├──────────────────────┐                  ▼
               │                      │     [Aluno Ajusta + OK Orientador]
               ▼                      ▼                  │
    [Sem Etapa Ética]       [c) Pendência CEP]           └─► [Reavaliação Avaliador]
               │                      │
               │                      ▼
               │            [Upload do Parecer CEP]
               │                      │
               └──────────┬───────────┘
                          │
                          ▼
             [d) Reprovado s/ Direito] ──► [Desligamento / Novo Plano]
                          │
                          ▼
            [Homologação Final da CPG]

```

1. **Submissão pelo Discente:** O aluno preenche os metadados (Título, Resumo, Objetivos, Linha de Pesquisa, Metodologia e Previsão de PTT) e anexa o PDF do Plano de Trabalho no Portal.
2. **Anuência e OK do Orientador:** O plano **não** segue diretamente para a secretaria. O sistema envia uma notificação ao orientador, que deve revisar o documento e clicar em "Aprovar e Encaminhar". Esta etapa garante que o orientador esteja ciente e de acordo com o plano submetido.
3. **Triagem da Secretaria e Pauta da CPG:** A secretaria valida a documentação e marca o chamado como `ready_for_agenda` (Apto para Pauta). Na reunião da CPG, o colegiado indica formalmente o parecerista/avaliador do plano.
4. **Designação e Avaliação:** A secretaria cadastra a indicação no ERP, que envia o dossiê ao painel do avaliador com prazo limite para resposta.

### 6.3. As 4 Categorias de Parecer do Avaliador

Ao concluir a análise, o parecerista deve selecionar obrigatoriamente um dos 4 resultados no formulário do sistema:

* **a) Aprovado:** O plano é considerado satisfatório e sem ressalvas técnicas.
* **b) Aprovado com Revisões:** O plano exige ajustes conceituais, metodológicos ou de cronograma.
* *Ciclo de Reavaliação:* O aluno recebe as solicitações no portal, realiza as correções junto ao orientador e ressubmete o arquivo. O orientador deve dar um novo "OK" no sistema para que a secretaria reencaminhe o plano corrigido ao mesmo avaliador para verificação final.


* **c) Aprovado com Pendência de CEP:** O plano técnico está correto, mas envolve seres humanos, animais ou biossegurança/radioproteção, exigindo aprovação de Comitê de Ética em Pesquisa (CEP/CEUA/Plataforma Brasil).
* *Trava de Ética/CEP:* O plano recebe o status "Aprovado Condicional". O Odoo bloqueia a liberação de recursos de bancas de qualificação e compras de insumos de projeto até que o discente anexe o Comprovante/Parecer Consubstanciado do CEP aprovado.


* **d) Reprovado sem Direito a Revisão:** O plano apresenta inviabilidade técnica, falta de aderência grave ou plágio. A CPG é notificada para deliberar sobre a concessão de um prazo extraordinário para submissão de um novo tema ou desligamento do aluno.

### 6.4. Homologação e Desbloqueio da Carreira

O Plano de Trabalho atinge o estado `homologated` somente após o parecer favorável do avaliador (e eventual comprovação do CEP) ser chancelado em Ata da CPG. Esta homologação é a chave de desbloqueio que permite ao discente avançar para os ritos de Seminário Geral de Área e Qualificação.

---

## 7. Regime de Alunos Especiais (Disciplinas Isoladas)

O sistema disponibiliza um fluxo paralelo e simplificado de admissão para candidatos a disciplinas isoladas (sem vínculo regular conducente a título de pós-graduação):

* **Atribuição do Registro Acadêmico (RA) Perene:** O candidato aprovado para cursar disciplinas isoladas recebe um Registro Acadêmico (RA) definitivo e perene da IES gerado em `op.student`, associado de forma única ao seu CPF. Se futuramente for aprovado como aluno regular em qualquer programa da IES, este mesmo RA e ficha cadastral serão mantidos.
* **Governança no Programa e Oferta:**
  * O ERP verifica se o regimento do programa autoriza discentes especiais (`allow_special_students = True`). No caso do **MPTRCS/IPEN**, o regimento padrão estabelece `allow_special_students = False`, bloqueando inscrições isoladas no programa.
  * Em programas que admitem alunos especiais, a inscrição requer que a disciplina autorize (`allow_special_students = True` em `op.subject`), respeite a cota de vagas (`special_seats_quota`) e possua o aceite expresso do professor responsável (`special_student_instructor_consent_required`).
* **Controle de Teto Regimental:** O sistema controla a quantidade máxima de disciplinas/créditos permitidos para a categoria (`max_special_subjects_limit`).
* **Armazenamento em Quarentena e Restrição de Direitos:** Alunos especiais não possuem orientador, não submetem plano de trabalho e não recebem status de regular. Os créditos concluídos são armazenados no livro-razão no estado `subject_special_quarantine`. O sistema emite ao final apenas uma Declaração/Certidão de Estudos Isolados.
* **Regra de Aproveitamento e Política de Reprovações:** Ao ingressar futuramente como regular, o aproveitamento segue a janela decadencial de 36 meses e requer homologação da CPG. Reprovações ocorridas no regime especial figuram apenas na certidão de estudos isolados, não constando no histórico escolar oficial de titulação regular (política `omit_on_regular`).

