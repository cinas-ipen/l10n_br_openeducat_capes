# Documento 04: Portal Discente, Requerimentos e Governança CPG


## 1. Descentralização via Portal Self-Service (`op.academic.request`)

Todas as solicitações discentes (migração de regimento, prorrogações de prazo, trancamentos, aproveitamento de créditos externos, coorientação, proficiência e homologação de PTT) são iniciadas no Portal do Aluno via modelo unificado `op.academic.request`. O modelo herda `mail.thread` e `mail.activity.mixin`, garantindo rastreabilidade integral:

* **Estados do Requerimento (`state`):** `draft` (Rascunho) $\rightarrow$ `submitted` (Submetido) $\rightarrow$ `under_review` (Em Análise Gabinete/CPG) $\rightarrow$ `approved` (Aprovado / Deferido), `rejected` (Indeferido) ou `cancelled` (Cancelado).
* **Anuência do Orientador (`advisor_approval`):** `pending` (Pendente), `approved` (Aprovado), `rejected` (Rejeitado).

## 2. A Esteira de Tramitação e Pauta CPG

Os requerimentos submetidos passam pelo seguinte fluxo padronizado:

1. O discente submete o requerimento no portal (`state = 'submitted'`).
2. Quando a regra exige, o orientador registra a anuência eletrônica (`advisor_approval = 'approved'`).
3. O chamado avança para análise da Secretaria Acadêmica e vinculação à pauta de reunião da CPG (`state = 'under_review'`).
4. A secretaria associa o requerimento à reunião colegiada através do campo `cpg_meeting_id` (vinculando a `agenda_request_ids` em `op.cpg.meeting`).

## 3. Orquestração da Reunião e Pauta da CPG (`op.cpg.meeting`)

A secretaria agenda a sessão colegiada ordinária ou extraordinária, controlando o ciclo de vida da reunião:
* **Estados da Reunião:** `draft` (Rascunho) $\rightarrow$ `agenda_open` (Pauta Aberta / Em Preparação) $\rightarrow$ `in_approval` (Em Aprovação) $\rightarrow$ `published` (Publicada / Homologada) ou `cancelled` (Cancelada).
* **Composição da Pauta:** A reunião agrega os requerimentos acadêmicos pautados (`agenda_request_ids`), onde cada processo é apreciado individualmente.

## 4. O Motor de Template da Ata (QWeb) e o Clique Auditável (`op.cpg.approval.log`)

Durante a reunião do colegiado:

1. A secretaria registra a presença e deliberações sobre os processos em pauta.
2. O motor QWeb compila o documento de ata final (`minutes_pdf`) anexado diretamente ao registro da reunião.
3. **Clique Auditável (`op.cpg.approval.log`):** Os membros votantes registram a aprovação da ata através de clique no ERP. A classe `op.cpg.approval.log` grava atomicamente:
   * `user_id`: Membro votante autenticado.
   * `timestamp`: Carimbo de tempo digital exato.
   * `ip_address`: Endereço IP do dispositivo de votação.
   * `vote`: `approve` (Aprovar/Deferir), `reject` (Rejeitar/Indeferir) ou `abstain` (Abstenção).
   * `notes`: Observações e ressalvas do votante.

## 5. Gatilho de Execução Autônoma

A publicação formal da ata (`action_publish_minutes()`) transiciona a reunião para `published` e consolida os efeitos regimentais:

* **Atualização Discente:** Os requerimentos pautados deferidos executam suas ações de negócio atômicas (ex: na migração de regimento, atualiza `student_id.curriculum_version_id = target_curriculum_version_id`; nas prorrogações, computa novos prazos limites).
* **Imutabilidade e Transparência:** A reunião é travada contra edições destrutivas e o documento QWeb PDF é averbado para os órgãos de controle interno e da CAPES.

## 6. Requerimentos Especiais: Aproveitamento de Estudos e Trânsito Intra-IES

* **Requerimento de Aproveitamento de Aluno Especial (`op.special.credit.incorporation.request`):**
  * O discente regular seleciona na esteira do portal as disciplinas previamente cursadas no regime isolado (armazenadas em `subject_special_quarantine`).
  * O motor verifica a validade temporal ($\le 36$ meses da admissão regular) e o teto regimental de disciplinas.
  * O requerimento é submetido à anuência do Orientador e encaminhado para triagem e pauta da CPG.
  * A aprovação em Ata CPG injeta os créditos no livro-razão como `subject_special_incorporated`, habilitando sua exibição no histórico oficial de titulação.
* **Requerimento de Inscrição em Disciplina Intra-IES:**
  * O discente solicita cursar disciplina de outro PPG da mesma IES.
  * O portal dispara notificações para coleta da anuência eletrônica do orientador e do docente ministrante da disciplina receptora, garantindo transparência interdepartamental.
