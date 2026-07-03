# Dicionário de Dados DAV: Módulo 04 - Trabalhos de Conclusão e Defesas

**Objetivo:** Estruturar as teses, dissertações e composições de banca, vital para o fluxo de titulação e repositório OAI-PMH.

## 1. Trabalho de Conclusão (`capes.thesis`)
| Campo Odoo | Metadado JSON DAV | Tipo de Dado Odoo | Domínio / Validação JSON |
| :--- | :--- | :--- | :--- |
| `student_id` | Identificador do Discente | `Many2one` | FK para Pós-graduando. |
| `defense_date` | Data da defesa do trabalho | `Date` | AAAA-MM-DD. |
| `title` | Título Final Aprovado | `Char` | Texto exato. |
| `doc_type` | Tipo de documento | `Selection` | Dissertação, Tese, Produto Tecnológico. |
| `repository_url`| URL no Repositório | `Char` | Handle do RI (Exigência GoPG). |

## 2. Composição da Banca (`capes.thesis.committee`)
| Campo Odoo | Metadado JSON DAV | Tipo de Dado Odoo | Domínio / Validação JSON |
| :--- | :--- | :--- | :--- |
| `thesis_id` | Trabalho de Conclusão | `Many2one` | FK para `capes.thesis`. |
| `member_id` | Nome do membro da banca | `Many2one` | FK para Pessoa (Interno/Externo). |
| `member_role` | Papel na Banca | `Selection` | Orientador, Avaliador Interno, Externo. |