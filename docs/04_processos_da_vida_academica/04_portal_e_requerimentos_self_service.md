# Documento 04: Portal Discente, Requerimentos e Governança CPG

## 1. Descentralização via Portal Self-Service (`op.academic.request`)

Todas as solicitações discentes (migração de regimento, prorrogações, trancamentos, aproveitamento de créditos externos, mudança de orientador) são iniciadas no Portal do Aluno. A classe `op.academic.request` herda `mail.thread`, garantindo histórico imutável com selo de data, hora, usuário e endereço IP.

## 2. A Esteira de Triagem da Secretaria

Os requerimentos submetidos não caem diretamente na mesa dos pareceristas. O sistema institui a etapa de **Triagem da Secretaria**:

1. O chamado entra no dashboard com o status `waiting_screening`.
2. A secretaria acadêmica valida se a documentação anexada está completa e se não há pendências na biblioteca ou setor financeiro.
3. Se válida, a secretaria clica em "Aprovar Triagem", alterando o status para `ready_for_agenda` (Apto para Pauta).

## 3. Orquestração da Reunião e Pauta da CPG (Macroprocesso 10)

A secretaria abre um registro de reunião da CPG (`op.cpg.meeting`) e puxa todos os chamados em `ready_for_agenda` para compor a pauta oficial, juntamente com os itens administrativos livres.

## 4. O Motor de Template da Ata (QWeb) e o Clique Auditável

Durante a reunião do colegiado:

1. A secretaria registra o quórum de membros presentes (`op.cpg.member`) e preenche o resultado das deliberações (*Deferido*, *Indeferido*, *Aprovado com Ressalvas*).
2. O motor de relatórios QWeb do Odoo compila instantaneamente a Ata da Reunião em formato PDF formatado.
3. **Clique Auditável:** Os membros presentes recebem uma notificação no ERP e clicam no botão **"Aprovar Ata"**. O sistema grava o ID do usuário, carimbo de data/hora e IP de conexão, dispensando tokens externos para atos internos.

## 5. Gatilho de Execução Autônoma

Aprovação da Ata pelo colegiado dispara autonomamente três ações no sistema:

* **Atualização Discente:** O status dos requerimentos pautados avança para "Deferido" ou "Indeferido", aplicando automaticamente os efeitos no banco de dados (ex: injetando dias de prorrogação ou atualizando o regimento).
* **Congelamento da Reunião:** O registro da reunião e sua pauta são travados em modo Read-Only.
* **Publicação:** O PDF da Ata com os selos de auditoria é marcado como "Publicado" para transparência ativa.

## 6. Requerimentos Especiais: Aproveitamento de Estudos e Trânsito Intra-IES

* **Requerimento de Aproveitamento de Aluno Especial (`op.special.credit.incorporation.request`):**
  * O discente regular seleciona na esteira do portal as disciplinas previamente cursadas no regime isolado (armazenadas em `subject_special_quarantine`).
  * O motor verifica a validade temporal ($\le 36$ meses da admissão regular) e o teto regimental de disciplinas.
  * O requerimento é submetido à anuência do Orientador e encaminhado para triagem e pauta da CPG.
  * A aprovação em Ata CPG injeta os créditos no livro-razão como `subject_special_incorporated`, habilitando sua exibição no histórico oficial de titulação.
* **Requerimento de Inscrição em Disciplina Intra-IES:**
  * O discente solicita cursar disciplina de outro PPG da mesma IES.
  * O portal dispara notificações para coleta da anuência eletrônica do orientador e do docente ministrante da disciplina receptora, garantindo transparência interdepartamental.
