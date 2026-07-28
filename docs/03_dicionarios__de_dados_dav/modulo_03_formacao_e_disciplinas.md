# Dicionário de Dados DAV: Módulo 03 - Formação, Disciplinas e Turmas

**Objetivo:** Mapear o catálogo de disciplinas, ofertas e instâncias de turmas baseadas no JSON DAV.

## 1. Disciplina (`op.subject`)
| Campo Odoo | Metadado JSON DAV | Tipo de Dado Odoo | Domínio / Validação JSON |
| :--- | :--- | :--- | :--- |
| `capes_id` | Identificador da disciplina | `Integer` | Numérico. |
| `internal_code` | Código da disciplina no PPG | `Char` | Alfanumérico. |
| `name` | Nome da disciplina | `Char` | Texto livre. |
| `syllabus` | Ementa da disciplina | `Text` | Texto explicativo. |
| `basic_biblio` | Bibliografia Básica | `Text` | Referências essenciais. |
| `workload` | Carga horária da disciplina | `Integer` | Numérico. |
| `credits` | Número de créditos | `Integer` | Numérico. |
| `is_mandatory` | Indicador de obrigatoriedade| `Boolean` | Sim; Não. |
| `start_date` | Data de início da disciplina| `Date` | AAAA-MM-DD. |
| `end_date` | Data de encerramento | `Date` | AAAA-MM-DD. |

## 2. Turma (`op.batch` / `op.session`)
| Campo Odoo | Metadado JSON DAV | Tipo de Dado Odoo | Domínio / Validação JSON |
| :--- | :--- | :--- | :--- |
| `capes_id` | Identificador da turma | `Integer` | Numérico. |
| `batch_code` | Código da turma | `Char` | Alfanumérico. |
| `academic_year` | Ano de oferta da turma | `Integer` | AAAA. |
| `academic_term` | Período letivo da turma | `Selection` | 1°, 2°, 3°, 4°, 5°, 6°. |
| `language` | Idioma da turma | `Selection` | Tabela Idiomas Capes. |
| `phea_indicator`| Utilização de PHEA (Híbrido)| `Boolean` | Sim; Não. |
| `prog_content` | Conteúdo Programático | `Text` | Temas e unidades de estudo. |
| `complem_biblio`| Bibliografia Complementar | `Text` | Obras adicionais. |

### 2.1 Ministrantes da Turma
| Campo Odoo | Metadado JSON DAV | Tipo de Dado Odoo | Domínio / Validação JSON |
| :--- | :--- | :--- | :--- |
| `faculty_id` | Ministrante da turma | `Many2one` | Docente vinculado. |
| `is_responsible`| Responsável pela turma | `Boolean` | Sim; Não. |