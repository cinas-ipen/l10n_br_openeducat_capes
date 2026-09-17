# Manual Operacional do Usuário: Coordenação do Programa de Pós-Graduação
## Ecossistema l10n_br_openeducat_capes (Odoo 19.0)

Este manual é destinado aos Coordenadores de Programa, Vice-Coordenadores e Presidentes da Comissão de Pós-Graduação (CPG), abordando as decisões estratégicas, aprovações regimentais e monitoramento de conformidade CAPES / GoPG.

---

## 1. Perfil de Acesso e Responsabilidades

* **Grupos de Segurança:** `openeducat_core.group_op_back_office_admin` e Membro da Comissão CPG (`op.cpg.committee`).
* **Usuários Padrão de Homologação/Treinamento:**
  * **Coordenador do PPG:** `coordenador` / Senha: `coordenador123`
  * **Vice-Coordenador do PPG:** `vicecoordenador` / Senha: `vicecoordenador123`
* **Responsabilidades Primárias:**
  * Homologação de Bancas Examinadoras de Qualificação e Defesa.
  * Presidência e condução das deliberações da CPG (colegiado de 6 membros titulares e 4 suplentes).
  * Monitoramento de prazos regimentais e controle de retenção/jubilamento discente.
  * Validação de Produtos Técnico-Tecnológicos (PTT) e acompanhamento do Qualis.
  * Supervisão da interoperabilidade com a CAPES (APIs RESTful do Programa GoPG).
  * Gestão de parâmetros curriculares e turmas do OpenEduCat.

---

## 2. Monitoramento de Prazos e Prevenção de Jubilamento

### 2.1. Painel de Controle de Prazos Regimentais
O Odoo 19 calcula em tempo real o relógio acadêmico de cada discente a partir da data de ingresso:
1. Acesse **Ensino CAPES $ightarrow$ Monitoramento Cronológico**.
2. Visualize o kanban com os alertas de semáforo:
   * 🟢 **Em Prazo Regular:** < 75% do prazo máximo do regimento.
   * 🟡 **Alerta de Conclusão:** Entre 75% e 90% do prazo decorrido.
   * 🔴 **Risco de Jubilamento:** > 90% do prazo sem agendamento de defesa.
3. **Prorrogações de Prazo:**
   * A Coordenação recebe os requerimentos de prorrogação submetidos pelos orientadores.
   * O sistema verifica se o pedido respeita o teto regimental (ex: até 90 dias no MPTRCS).
   * Caso deferido pela CPG, o novo prazo de defesa é recalculado automaticamente.

### 2.2. Gestão de Trancamentos e Desligamentos
* **Trancamento:** A CPG homologa suspensões temporárias do vínculo (até 365 dias). Durante o trancamento, o relógio acadêmico é pausado.
* **Cron Job Noturno de Jubilamento:** Diariamente, o robô noturno do sistema verifica discentes que ultrapassaram o prazo máximo sem defesa ou que incorreram em dupla reprovação. O status é alterado para `pending_dismissal`. A Coordenação revisa esses casos para formalizar a notificação ou emitir a portaria de desligamento.

---

## 3. Deliberações da CPG e Homologação de Requerimentos

### 3.1. Requerimentos de Aproveitamento de Créditos Especiais
1. Acesse **Governança CPG $ightarrow$ Requerimentos de Aproveitamento de Créditos Especiais**.
2. Filtre por registros com status `advisor_approved` (com parecer favorável do orientador).
3. Analise:
   * Atestado de conclusão da disciplina.
   * Certificação de que a disciplina foi cursada há **menos de 36 meses (3 anos)**.
   * Cumprimento dos tetos regimentais de disciplinas especiais do programa.
4. Clique em **Aprovar pela CPG** (`action_cpg_approve`) informando o número da Resolução da CPG e a data da ata.
5. O sistema grava automaticamente a convalidação imutável no Livro-Razão discente como `subject_special_incorporated`.

### 3.2. Autorização de Trânsito Intra-IES e Extra-IES
* **Intra-IES:** Disciplinas cursadas em outros PPGs da mesma instituição. A Coordenação verifica se o discente respeita o teto percentual curricular (`max_intra_ies_credits_percent`).
* **Extra-IES (Disciplinas Externas):**
  * Para alunos de programas como o **MPTRCS**, disciplinas de outros programas (como o de Tecnologia Nuclear da **USP**) são formalmente Extra-IES.
  * A CPG delibera sobre a equivalência do programa e a aderência à linha de pesquisa do discente, observando o teto regimental de créditos externos (Art. 31º §1º - máximo de 20 créditos).

### 3.3. Calendário Mensal de Reuniões da CPG e Assinatura Eletrônica Auditável
1. Acesse **Governança CPG $ightarrow$ Reuniões da CPG** (`op.cpg.meeting`).
2. O conselho colegiado (6 membros titulares e 4 suplentes) reúne-se mensalmente para pautar e deliberar requerimentos discentes (`op.academic.request`), bancas e credenciamentos.
3. Para publicar e homologar as decisões:
   * Abra a reunião com status `in_approval` e clique em **Aprovar e Publicar Ata**.
   * O sistema aciona o mecanismo de **Clique Auditável** (`op.cpg.approval.log`), registrando de forma inviolável o login do usuário autenticado, carimbo de tempo (timestamp UTC) e endereço IP da conexão.
   * É gerada a Ata da Reunião oficial em QWeb PDF (`minutes_pdf`), ficando disponível no acervo do colegiado.

---

## 4. Homologação de Comissões Examinadoras (Bancas)

1. Acesse **Bancas & Titulação $ightarrow$ Trabalhos Finais**.
2. Abra a solicitação de banca agendada pela secretaria.
3. **Auditoria de Impedimento Cível:** O sistema sinaliza automaticamente se há parentesco até 4º grau (`civil_relationship_flag`) entre examinador e candidato/orientador.
4. **Auditoria de Endogenia e Titulação:** O sistema confere se o quórum de doutores e examinadores externos à IES e ao PPG está atendido.
5. A Coordenação clica em **Homologar Banca**, emitindo os convites formais aos membros da comissão.

---

## 5. Avaliação de Produtos Técnico-Tecnológicos (PTTs) e Qualis

1. Acesse **Produção Intelectual $ightarrow$ Produtos Técnico-Tecnológicos** (`capes.ptt.product`).
2. Avalie a classificação informada pelo orientador nos 4 eixos estruturantes:
   * **Eixo 1:** Demanda e Aderência (0 a 30 pts)
   * **Eixo 2:** Inovação e Ineditismo (0 a 25 pts)
   * **Eixo 3:** Aplicabilidade e Utilidade (0 a 25 pts)
   * **Eixo 4:** Complexidade Técnica (0 a 20 pts)
3. A calculadora automatizada de estratos gera o Qualis Tecnológico (`final_stratum`: `T1` a `T5`). A Coordenação valida a nota e o nível de maturidade tecnológica (`trl_level`: `trl_1` a `trl_9`) antes da homologação formal (`state = 'homologated'`) e encaminhamento para a coleta Sucupira/GoPG.

---

## 6. Interoperabilidade e Governança GoPG (CAPES)

1. Acesse **Integração Externa $ightarrow$ Painel de Coleta GoPG**.
2. **Auditoria da Fonte Prata:** O Odoo disponibiliza os dados acadêmicos via API RESTful sob `/api/capes/v1/`:
   * Discentes e PIDs biográficos (ORCiD, CPF, Lattes).
   * Docentes, regimes de trabalho e credenciamento CPG.
   * Matrizes curriculares e histórico de créditos do Livro-Razão.
   * Projetos de pesquisa e PTTs com Qualis.
3. **Auditoria da Fonte Ouro (DSpace):** Acompanhe se as teses e dissertações tituladas receberam o Handle permanente e estão indexadas no namespace `oai_capes`.

---

## 7. Visão 360° Estratégica da Coordenação
Para acompanhamento global dos indicadores do programa sem necessidade de relatórios externos:
1. **Auditoria Discente 360°:** Acesse a ficha de qualquer estudante para verificar diretamente no cabeçalho o botão **"Imprimir Histórico Escolar"**, os smart buttons de vínculos, créditos, trabalhos finais, produtos PTT, requerimentos e diplomas digitais, bem como o extrato detalhado de disciplinas cursadas na aba de créditos.
2. **Auditoria Docente 360°:** Acesse os formulários de professores para auditar a distribuição de orientações ativas (respeitando o teto de orientandos por docente permanente), o histórico de egressos titulados, a carga de disciplinas ministradas e a atuação em bancas examinadoras.
