# Dicionário de Dados DAV: Módulo 04 - Trabalhos de Conclusão, Planos de Trabalho e Defesas

**Objetivo:** Estruturar as entidades relacionais de Planos de Trabalho, Teses, Dissertações, Ritos Bipartidos (Seminário de Área e Exame de Qualificação) e Composição de Bancas Examinadoras, assegurando total aderência às exigências da CAPES (DAV Módulo 04 e GoPG) e interoperabilidade com o Repositório Institucional (Fonte Ouro / DSpace).

---

## 1. Plano de Trabalho Discente (`op.student.work_plan`)

*Entidade de acompanhamento prévio do projeto de pesquisa, cuja aprovação e homologação na CPG é pré-requisito para evolução nos ritos acadêmicos.*

| Campo Odoo | Metadado DAV / Regra de Negócio | Tipo de Dado Odoo | Domínio / Validação JSON |
| --- | --- | --- | --- |
| `student_id` | Identificador do Discente | `Many2one` | FK para `op.student`. Mandatory.

 |
| `advisor_id` | Orientador Responsável | `Many2one` | FK para `op.faculty`. Mandatory.

 |
| `coadvisor_id` | Coorientador (se houver) | `Many2one` | FK para `op.faculty`.

 |
| `title` | Título Provisório do Projeto | `Char` | Texto livre.

 |
| `summary` | Resumo da Proposta de Pesquisa | `Text` | Texto explicativo.

 |
| `line_id` | Linha de Pesquisa do PPG | `Many2one` | FK para `capes.linha.pesquisa`. Mandatory.

 |
| `expected_ptt_type_id` | Previsão de Tipo de PTT (Se Profissional) | `Many2one` | FK para `capes.ptt.type`. Exigido para cursos profissionais.

 |
| `advisor_approval` | Anuência / OK do Orientador | `Boolean` | Trava: Requer `True` para envio à Secretaria/CPG.

 |
| `evaluator_id` | Parecerista / Avaliador CPG | `Many2one` | FK para `res.partner` / `op.faculty`. Designado em Pauta.

 |
| `evaluator_opinion` | Categoria de Parecer do Avaliador | `Selection` | `approved` (Aprovado), `approved_revisions` (Aprovado c/ Revisões), `approved_cep_pending` (Aprovado c/ Pendência CEP), `rejected_no_revision` (Reprovado s/ Direito).

 |
| `cep_required` | Exige Apreciação de Comitê de Ética (CEP/CEUA) | `Boolean` | Indicador se a pesquisa envolve humanos/animais/biossegurança.

 |
| `cep_approval_document` | Parecer Consubstanciado CEP Aprovado | `Binary` | Anexo em PDF. Libera o status em caso de pendência ética.

 |
| `status` | Situação do Plano de Trabalho | `Selection` | `draft` (Rascunho), `waiting_advisor` (Aguardando OK Orientador), `waiting_screening` (Triagem Secretaria), `ready_for_agenda` (Apto para Pauta CPG), `under_evaluation` (Em Avaliação), `conditional_cep` (Aprovado Pendente CEP), `homologated` (Homologado CPG), `rejected` (Reprovado).

 |

---

## 2. Trabalho de Conclusão e Ritos (`capes.thesis`)

*Entidade transacional central que registra a qualificação, o seminário de área e a defesa final da dissertação ou tese.*

| Campo Odoo | Metadado JSON DAV / Regras Odoo | Tipo de Dado Odoo | Domínio / Validação JSON |
| --- | --- | --- | --- |
| `capes_id` | Identificador na CAPES | `Integer` | Numérico.

 |
| `student_id` | Identificador do Discente | `Many2one` | FK para `op.student`. Mandatory.

 |
| `curriculum_version_id` | Versionamento Regimental Ativo | `Many2one` | FK para `op.curriculum.version` (Garante Ato Perfeito).

 |
| `work_plan_id` | Plano de Trabalho Homologado | `Many2one` | FK para `op.student.work_plan`. Trava de agendamento.

 |
| `project_id` | Projeto de Pesquisa Vinculado | `Many2one` | FK para `capes.research.project`.

 |
| `ptt_product_id` | PTT Associado (Mestrado Profissional) | `Many2one` | FK para `capes.ptt.product`. Condição de desbloqueio para defesa.

 |
| `stage` | Rito Acadêmico Registrado | `Selection` | `seminar_area` (Seminário de Área), `qualification` (Exame de Qualificação Clássico), `defense` (Defesa Pública Final).

 |
| `defense_date` | Data e Horário do Rito | `Datetime` | Data e Hora da sessão. Precedência mínima de 15 dias para agendamento.

 |
| `title` | Título Final Aprovado em Ata | `Char` | Texto exato no idioma principal. Mandatory.

 |
| `name` | Identificador / Título do Trabalho | `Char` | Campo armazenado relacionado a `title`.

 |
| `title_alt` | Título Traduzido (Inglês) | `Char` | Texto exato no idioma estrangeiro.

 |
| `doc_type` | Tipo de Documento Final | `Selection` | `dissertation` (Dissertação), `thesis` (Tese), `tech_product` (Produto Tecnológico).

 |
| `final_pdf_file` | Versão Final da Dissertação/Tese (PDF) | `Binary` | Upload do PDF final corrigido pelo discente (contendo capa, folha de aprovação e ficha catalográfica).
 |
| `secretariat_approval` | Validação da Secretaria Acadêmica | `Boolean` | Aceite formal da Secretaria após conferência do PDF e ficha catalográfica (Libera status Titulado).
 |
| `library_manifest_payload` | Manifesto de Metadados DSpace | `Text` | Guia com metadados gerada pelo Odoo para envio à Biblioteca Central.
 |
| `status` | Situação do Rito | `Selection` | `draft` (Rascunho), `scheduled` (Agendado), `approved` (Aprovado na Banca), `disapproved` (Reprovado na Banca), `deposit_pending` (Pendente Envio Versão Final Aluno), `final_version_submitted` (Versão Final Enviada - Triagem Secretaria), `homologated` (Homologado / Titulado - Secretaria OK).
 |
| `repository_url` | Handle / URI no Repositório (DSpace) | `Char` | Handle permanente gerado e averbado pela Biblioteca Central (Fonte Ouro) após o upload no DSpace.
 |
| `abstract_main` | Resumo no Idioma Principal | `Text` | Texto integral do resumo aprovado.

 |
| `abstract_alt` | Resumo em Inglês (Abstract) | `Text` | Texto integral do resumo em língua estrangeira.

 |
| `keywords_main` | Palavras-chave no Idioma Principal | `Char` | Vocabulário controlado separado por ponto e vírgula.

 |
| `keywords_alt` | Palavras-chave em Inglês | `Char` | Vocabulário controlado no idioma estrangeiro.

 |
| `presentation_time_minutes` | Tempo de Exposição do Candidato | `Integer` | Gravado em Ata. Teto regimental: 50 minutos.

 |
| `arguing_time_minutes` | Tempo de Arguição por Examinador | `Integer` | Gravado em Ata. Teto regimental: 40 minutos por membro.

 |

---

## 3. Composição da Banca Examinadora (`capes.thesis.committee`)

*A validação da comissão julgadora é realizada dinamicamente pelo Odoo consultando a tabela de regras do regimento do aluno (`op.curriculum.committee.rule`).*

| Campo Odoo | Metadado JSON DAV / Regras Odoo | Tipo de Dado Odoo | Domínio / Validação JSON |
| --- | --- | --- | --- |
| `thesis_id` | Rito / Trabalho de Conclusão | `Many2one` | FK para `capes.thesis`. Mandatory. |
| `member_id` | Nome do Examinador | `Many2one` | FK para `res.partner` (Interno ou Externo). Mandatory. |
| `member_role` | Papel na Comissão Julgadora | `Selection` | `advisor` (Orientador / Presidente), `coadvisor` (Coorientador), `internal_evaluator` (Avaliador Interno), `external_evaluator` (Avaliador Externo), `substitute_internal` (Suplente Interno), `substitute_external` (Suplente Externo). |
| `is_titular` | Indicador de Membro Titular | `Boolean` | `True` para membros efetivos da pauta; `False` para suplentes. |
| `can_vote` | Direito a Voto Ativo | `Boolean` | Computado de acordo com as regras `advisor_vote_role` e `coadvisor_participation` do regimento do aluno (ex: `False` para orientadores no CDTN). |
| `is_internal` | Pertence ao Quadro Institucional da IES | `Boolean` | Computado de `res.partner.is_internal`. Utilizado para validar a regra `external_rule` de endogenia. |
| `ies_origin` | IES de Origem do Examinador | `Char` | Texto livre para membros externos (exportado na DAV / Sucupira). |
| `has_phd` | Possui Título de Doutor | `Boolean` | Valida se exige doutorado ou se possui parecer de notória especialização aprovado pela alçada correspondente. |
| `civil_relationship_flag` | Impedimento por Parentesco | `Boolean` | Valida ausência de parentesco direto/colateral até 4º grau com discente ou orientador (Impedimento Cível Regimental). |
