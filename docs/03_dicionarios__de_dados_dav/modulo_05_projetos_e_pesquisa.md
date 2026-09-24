# Dicionário de Dados DAV: Módulo 05 - Projetos de Pesquisa

**Objetivo:** Estruturar o módulo de projetos, consolidando a ligação entre linhas, membros e cooperação baseada no JSON.

## 1. Projeto de Pesquisa (`capes.research.project`)

Entidade responsável pela gestão de projetos científicos e tecnológicos vinculados ao PPG, integrando agências de fomento, cooperação internacional e o quadro kanban de tarefas nativo do Odoo (`project.project`).

| Campo Odoo | Metadado JSON DAV / Regras | Tipo de Dado Odoo | Domínio / Validação JSON |
| :--- | :--- | :--- | :--- |
| `capes_id` | Identificador do projeto | `Integer` | Numérico (identificador na Coleta/Sucupira). |
| `name` | Nome do projeto de pesquisa | `Char` | Título oficial da pesquisa. Obrigatório. |
| `description` | Descrição do projeto | `Text` | Resumo descritivo e objetivos científicos. |
| `project_type` | Tipo de projeto | `Selection` | `scientific` (Científica), `extension` (Extensão), `innovation` (Inovação), `teaching` (Ensino). |
| `research_nature`| Natureza da pesquisa | `Selection` | `basic` (Pesquisa Básica), `applied` (Pesquisa Aplicada). |
| `is_cooperation`| Projeto em cooperação | `Boolean` | Sim; Não. Indica parceria interinstitucional. |
| `foreign_ies` | Nome da IES Estrangeira | `Char` | Denominação da instituição estrangeira parceira. |
| `foreign_country_id` | País da IES Estrangeira | `Many2one` | FK para `res.country`. |
| `funding_agency` | Agência de Fomento | `Char` | Ex: CNPq, CAPES, FAPESP, FINEP, IAEA. |
| `funding_process` | Processo de Fomento / Grant | `Char` | Número do processo formal de auxílio financeiro. |
| `status` | Situação do projeto | `Selection` | `ongoing` (Em Andamento), `completed` (Concluído), `suspended` (Suspenso), `cancelled` (Cancelado). |
| `status_date` | Data da situação | `Date` | AAAA-MM-DD. |
| `start_date` | Data de início | `Date` | AAAA-MM-DD. Obrigatório. |
| `end_date` | Data de encerramento | `Date` | AAAA-MM-DD. Trava: $\ge$ `start_date`. |
| `program_id` | Programa de Pós-Graduação | `Many2one` | FK para `op.program.capes`. Obrigatório. |
| `research_line_id` | Linha de Pesquisa do PPG | `Many2one` | FK para `op.program.research.line`. |
| `coordinator_id` | Coordenador do Projeto | `Many2one` | FK para `op.faculty`. Obrigatório. |
| `odoo_project_id` | Task Board Odoo Integrado | `Many2one` | FK para `project.project`. Integração com Kanban de tarefas. |
| `member_ids` | Equipe de Pesquisadores | `One2many` | Relação com `capes.project.member`. |

## 2. Membros e Taxonomia CRediT (`capes.project.member`)

Mapeia a equipe do projeto com a adoção estrita da taxonomia internacional **CRediT (Contributor Roles Taxonomy)** com 14 funções científicas normatizadas:

| Campo Odoo | Metadado JSON DAV / Regras | Tipo de Dado Odoo | Domínio / Validação JSON |
| :--- | :--- | :--- | :--- |
| `project_id` | Projeto de Pesquisa | `Many2one` | FK para `capes.research.project`. Obrigatório. |
| `partner_id` | Pesquisador / Membro | `Many2one` | FK para `res.partner`. Âncora de pessoa física. Obrigatório. |
| `faculty_id` | Docente Institucional | `Many2one` | FK para `op.faculty`. Preenchido se membro for docente do quadro. |
| `student_id` | Discente Vinculado | `Many2one` | FK para `op.student`. Preenchido se membro for discente/orientando. |
| `role` | Função na Gestão do Projeto | `Selection` | `coordinator` (Coordenador Principal), `vice_coordinator` (Vice-Coordenador), `researcher` (Pesquisador/Docente), `student_researcher` (Pesquisador Discente), `external_collaborator` (Colaborador Externo). |
| `contrib_type` | Tipo de Contribuição CRediT | `Selection` | `conceptualization` (Conceitualização), `methodology` (Metodologia), `software` (Software), `validation` (Validação), `formal_analysis` (Análise Formal), `investigation` (Investigação), `resources` (Recursos), `data_curation` (Curadoria de Dados), `writing_original` (Redação Original), `writing_review` (Revisão e Edição), `visualization` (Visualização), `supervision` (Supervisão), `project_admin` (Administração), `funding_acquisition` (Captação de Recursos). |
| `link_start` | Início do Vínculo na Equipe | `Date` | AAAA-MM-DD. Obrigatório. |
| `link_end` | Encerramento do Vínculo | `Date` | AAAA-MM-DD. Trava: $\ge$ `link_start`. |
| `area_name` | Área de Concentração | `Char` | Área de atuação associada à contribuição. |
| `research_line` | Linha de Pesquisa | `Char` | Linha de pesquisa vinculada à atuação do membro. |