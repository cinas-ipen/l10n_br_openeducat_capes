# Dicionário de Dados DAV: Módulo 05 - Projetos de Pesquisa

**Objetivo:** Estruturar o módulo de projetos, consolidando a ligação entre linhas, membros e cooperação baseada no JSON.

## 1. Projeto de Pesquisa (`capes.research.project`)
| Campo Odoo | Metadado JSON DAV | Tipo de Dado Odoo | Domínio / Validação JSON |
| :--- | :--- | :--- | :--- |
| `capes_id` | Identificador do projeto | `Integer` | Numérico. |
| `name` | Nome do projeto de pesquisa | `Char` | Texto livre. |
| `description` | Descrição do projeto | `Text` | Texto explicativo. |
| `project_type` | Tipo de projeto de pesquisa | `Selection` | Científica, Extensão, Inovação, Ensino. |
| `research_nature`| Natureza da pesquisa | `Selection` | Aplicada, Básica. |
| `is_cooperation`| Projeto em cooperação | `Boolean` | Sim; Não. |
| `foreign_ies` | Nome da IES Estrangeira | `Many2one` | Cadastro IES Estrangeira. |
| `status` | Situação do projeto | `Selection` | Em andamento, Concluido. |
| `status_date` | Data da situação | `Date` | AAAA-MM-DD. |
| `start_date` | Data de início | `Date` | AAAA-MM-DD. |
| `end_date` | Data de encerramento | `Date` | AAAA-MM-DD. |

## 2. Vínculos e Membros
| Campo Odoo | Metadado JSON DAV | Tipo de Dado Odoo | Domínio / Validação JSON |
| :--- | :--- | :--- | :--- |
| `coord_id` | Nome do coordenador | `Many2one` | FK para Docente. |
| `member_id` | Nome do membro | `Many2one` | FK para Pessoa. |
| `contrib_type` | Tipo de contribuição | `Selection` | Taxonomia CRediT (Conceitualização, Metodologia, Validação, Escrita...). |
| `link_start` | Início do vínculo do membro | `Date` | AAAA-MM-DD. |
| `link_end` | Encerramento do vínculo | `Date` | AAAA-MM-DD. |
| `area_id` | Vínculo c/ Área Concentração| `Many2one` | FK para Área. |
| `line_id` | Vínculo c/ Linha de Pesquisa| `Many2one` | FK para Linha. |