# Dicionário de Dados DAV: Módulo 04 - Trabalhos de Conclusão, Planos de Trabalho e Defesas

**Objetivo:** Estruturar as entidades relacionais de Planos de Trabalho, Teses, Dissertações, Ritos Bipartidos (Seminário de Área e Exame de Qualificação) e Composição de Bancas Examinadoras, assegurando total aderência às exigências da CAPES (DAV Módulo 04 e GoPG) e interoperabilidade com o Repositório Institucional (Fonte Ouro / DSpace).

---

## 1. Plano de Trabalho Discente (`op.student.work_plan`)

*Entidade de acompanhamento prévio do projeto de pesquisa, cuja aprovação e homologação na CPG é pré-requisito para evolução nos ritos acadêmicos.*

| Campo Odoo | Metadado DAV / Regra de Negócio | Tipo de Dado Odoo | Domínio / Validação JSON |
| --- | --- | --- | --- |
| `name` | Título do Plano de Trabalho | `Char` | Título preliminar do projeto de pesquisa. Obrigatório. |
| `student_id` | Identificador do Discente | `Many2one` | FK para `op.student`. Obrigatório. |
| `advisor_id` | Orientador Responsável | `Many2one` | FK para `op.faculty`. Relacionado a `student_id.advisor_id`. |
| `research_line_id` | Linha de Pesquisa (Entidade) | `Many2one` | FK para `op.program.research.line`. |
| `program_id` | Programa CAPES | `Many2one` | FK para `op.program.capes` (relacionado a `research_line_id.program_id`). |
| `research_line` | Linha de Pesquisa (Denominação) | `Char` | Denominação oficial da linha de pesquisa. Obrigatório. |
| `summary` | Resumo e Objetivos | `Text` | Texto explicativo da proposta. Obrigatório. |
| `methodology` | Metodologia de Pesquisa | `Text` | Detalhamento dos métodos científicos/técnicos. Obrigatório. |
| `ptt_prediction` | Previsão de PTT (Se Profissional) | `Text` | Previsão de patentes, registros de software, protótipos ou guias técnicos. |
| `attachment_pdf` | PDF Estruturado do Plano | `Binary` | Arquivo PDF estruturado contendo a íntegra do plano. Obrigatório. |
| `advisor_ok` | Anuência Eletrônica do Orientador | `Boolean` | Trava: Aceite formal autorizando tramitação para Secretaria/CPG. |
| `evaluator_id` | Parecerista / Avaliador CPG | `Many2one` | FK para `res.partner`. Designado para avaliação colegiada. |
| `cpg_meeting_id` | Pauta na Reunião CPG | `Many2one` | FK para `op.cpg.meeting`. Sessão de homologação colegiada. |
| `opinion_category` | Categoria de Parecer do Avaliador | `Selection` | `approved` (Aprovado sem Ressalvas), `revisions` (Aprovado com Revisões), `cep_pending` (Aprovado com Pendência CEP/CEUA), `rejected` (Reprovado sem Direito a Revisão). |
| `evaluator_opinion` | Parecer Técnico Circunstanciado | `Text` | Texto com considerações e fundamentação do avaliador. |
| `cep_document` | Parecer Consubstanciado CEP/CEUA | `Binary` | Upload do parecer de aprovação da Plataforma Brasil / CEUA. |
| `cep_approved` | Aprovação Ética Validada | `Boolean` | Trava: Libera o discente da pendência ética para agendamento de bancas. |
| `state` | Situação do Plano de Trabalho | `Selection` | `draft` (Rascunho), `submitted` (Submetido / Aguardando OK Orientador), `advisor_approved` (Aprovado pelo Orientador / Fila Secretaria), `under_evaluation` (Em Avaliação pelo Parecerista), `revisions_requested` (Em Revisão pelo Discente), `cep_pending` (Aprovado Condicional / Pendente CEP), `homologated` (Homologado CPG), `rejected` (Reprovado). |

---

## 2. Trabalho de Conclusão e Ritos (`capes.thesis`)

*Entidade transacional central que registra a qualificação, o seminário de área e a defesa final da dissertação ou tese.*

| Campo Odoo | Metadado JSON DAV / Regras Odoo | Tipo de Dado Odoo | Domínio / Validação JSON |
| --- | --- | --- | --- |
| `capes_id` | Identificador na CAPES | `Integer` | Numérico (identificador na Coleta/Sucupira). |
| `student_id` | Identificador do Discente | `Many2one` | FK para `op.student`. Obrigatório. |
| `curriculum_version_id` | Versionamento Regimental Ativo | `Many2one` | FK para `op.curriculum.version` (relacionado a `student_id.curriculum_version_id`). |
| `program_id` | Programa CAPES | `Many2one` | FK para `op.program.capes` (relacionado a `curriculum_version_id.program_id`). |
| `work_plan_id` | Plano de Trabalho Homologado | `Many2one` | FK para `op.student.work_plan`. Trava de agendamento (exige `homologated`). |
| `project_id` | Projeto de Pesquisa Vinculado | `Many2one` | FK para `capes.research.project`. |
| `stage` | Rito Acadêmico Registrado | `Selection` | `seminar_area` (Seminário de Área), `qualification` (Exame de Qualificação Clássico), `defense` (Defesa Pública Final). |
| `doc_type` | Tipo de Documento Final | `Selection` | `dissertation` (Dissertação de Mestrado), `thesis` (Tese de Doutorado), `tech_product` (Produto Tecnológico / Relatório Técnico). |
| `defense_date` | Data e Horário da Sessão | `Datetime` | Data e Hora da sessão. Precedência mínima de 15 dias para agendamento. |
| `title` | Título Final Aprovado em Ata | `Char` | Texto exato no idioma principal. Obrigatório. |
| `name` | Título Final (Identificador) | `Char` | Campo armazenado relacionado a `title`. |
| `title_alt` | Título Traduzido (Inglês) | `Char` | Texto exato no idioma estrangeiro. |
| `abstract_main` | Resumo no Idioma Principal | `Text` | Texto integral do resumo aprovado. |
| `abstract_alt` | Resumo em Inglês (Abstract) | `Text` | Texto integral do resumo em língua estrangeira. |
| `keywords_main` | Palavras-chave no Idioma Principal | `Char` | Vocabulário controlado separado por ponto e vírgula. |
| `keywords_alt` | Palavras-chave em Inglês | `Char` | Vocabulário controlado no idioma estrangeiro. |
| `presentation_time_minutes` | Tempo de Exposição do Candidato | `Integer` | Gravado em Ata. Teto regimental: 50 minutos. |
| `arguing_time_minutes` | Tempo de Arguição por Examinador | `Integer` | Gravado em Ata. Teto regimental: 40 minutos por membro. |
| `final_pdf_file` | Versão Final da Dissertação/Tese (PDF) | `Binary` | Upload do PDF final corrigido pelo discente (com capa, folha de aprovação e ficha catalográfica). |
| `final_pdf_filename` | Nome do Arquivo PDF Final | `Char` | Nome do arquivo anexado. |
| `final_pdf_upload_date` | Data de Envio da Versão Final | `Date` | Registrada automaticamente no upload. |
| `secretariat_approval` | Validação da Secretaria Acadêmica | `Boolean` | Aceite formal da Secretaria após conferência do PDF e ficha catalográfica (Libera status Titulado). |
| `secretariat_approval_date` | Data de Validação da Secretaria | `Date` | Data de deferimento da versão final pela Secretaria. |
| `library_manifest_payload` | Manifesto de Metadados DSpace | `Text` | Guia com metadados gerada pelo Odoo para envio à Biblioteca Central. |
| `repository_url` | Handle / URI no Repositório (DSpace) | `Char` | Handle permanente gerado e averbado pela Biblioteca Central (Fonte Ouro) após o upload no DSpace. |
| `deposit_date` | Data do Depósito no Repositório | `Date` | Data da averbação no repositório institucional DSpace. |
| `committee_ids` | Membros da Banca Examinadora | `One2many` | Relação com `capes.thesis.committee`. |
| `status` | Situação do Rito | `Selection` | `draft` (Rascunho), `scheduled` (Agendado), `approved` (Aprovado na Banca), `disapproved` (Reprovado na Banca), `deposit_pending` (Pendente Envio Versão Final Aluno), `final_version_submitted` (Versão Final Enviada - Triagem Secretaria), `homologated` (Homologado / Titulado - Secretaria OK). |

> [!NOTE]
> **Vínculo com PTT em Mestrados Profissionais:** O Produto Técnico-Tecnológico (`capes.ptt.product`) referencia diretamente o trabalho de conclusão através do campo Many2one `thesis_id`, estabelecendo a rastreabilidade estrita entre o trabalho final e a produção técnica tecnológica.

---

## 3. Composição da Banca Examinadora (`capes.thesis.committee`)

*A validação da comissão julgadora é realizada dinamicamente pelo Odoo consultando a tabela de regras do regimento do aluno (`op.curriculum.committee.rule`).*

| Campo Odoo | Metadado JSON DAV / Regras Odoo | Tipo de Dado Odoo | Domínio / Validação JSON |
| --- | --- | --- | --- |
| `thesis_id` | Rito / Trabalho de Conclusão | `Many2one` | FK para `capes.thesis`. Obrigatório. |
| `member_id` | Nome do Examinador | `Many2one` | FK para `res.partner` (Interno ou Externo). Obrigatório. |
| `member_role` | Papel na Comissão Julgadora | `Selection` | `advisor` (Orientador / Presidente), `coadvisor` (Coorientador), `internal_evaluator` (Avaliador Interno), `external_evaluator` (Avaliador Externo), `substitute_internal` (Suplente Interno), `substitute_external` (Suplente Externo). |
| `is_titular` | Indicador de Membro Titular | `Boolean` | `True` para membros efetivos da pauta; `False` para suplentes. |
| `can_vote` | Direito a Voto Ativo | `Boolean` | Computado de acordo com as regras `advisor_vote_role` e `coadvisor_participation` do regimento do aluno (ex: `False` para orientadores no CDTN). |
| `is_internal` | Pertence ao Quadro Institucional da IES | `Boolean` | Computado de `res.partner.is_internal`. Utilizado para validar a regra `external_rule` de endogenia. |
| `ies_origin` | IES de Origem do Examinador | `Char` | Texto livre para membros externos (exportado na DAV / Sucupira). |
| `has_phd` | Possui Título de Doutor | `Boolean` | Valida se exige doutorado ou se possui parecer de aprovação da CPG para não-doutor. |
| `non_phd_approval_doc` | Ata / Aprovação CPG para Não-Doutor | `Char` | Número da ata CPG que autorizou o especialista sem doutorado. |
| `civil_relationship_flag` | Impedimento por Parentesco | `Boolean` | Valida ausência de parentesco direto/colateral até 4º grau com discente ou orientador (Impedimento Cível Regimental). |
