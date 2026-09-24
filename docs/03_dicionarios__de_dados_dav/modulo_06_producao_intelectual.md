# Dicionário de Dados DAV: Módulo 06 - Produção Intelectual

**Objetivo:** Mapear as produções acadêmicas e bibliográficas, com metadados para interoperabilidade OAI-PMH extraídos do JSON 3 e 4.

## 1. Produção Intelectual (`capes.intellectual.production`)

Entidade central do módulo `l10n_br_openeducat_capes_integration` destinada à guarda, validação acadêmica e exportação interoperável da produção bibliográfica, artística e técnica-tecnológica de discentes e docentes do PPG.

| Campo Odoo | Metadado JSON DAV / Regras | Tipo de Dado Odoo | Domínio / Validação JSON |
| :--- | :--- | :--- | :--- |
| `name` | Título da Produção Intelectual | `Char` | Título oficial da obra/artigo/patente. Obrigatório. |
| `production_type` | Tipo de Produção | `Selection` | `article` (Artigo em Periódico Indexado), `book` (Livro Técnico-Científico), `chapter` (Capítulo de Livro), `conference` (Trabalho em Anais de Evento), `patent` (Patente/PI - PTT), `software` (Software/App - PTT), `other_ptt` (Outro PTT). |
| `student_id` | Discente Autor | `Many2one` | FK para `op.student`. Vincula autoria ou coautoria discente. |
| `faculty_id` | Docente Autor / Orientador | `Many2one` | FK para `op.faculty`. Vincula autoria ou supervisão docente. |
| `program_id` | Programa PPG Associado | `Many2one` | FK para `op.program.capes`. Obrigatório. |
| `publication_year` | Ano de Publicação / Concessão | `Integer` | Ano de lançamento ou depósito formal. Obrigatório. |
| `doi` | DOI (Digital Object Identifier) | `Char` | Identificador persistente digital (ex: `10.1016/j.radphyschem.2026.101234`). |
| `handle` | URI Handle no Repositório (DSpace) | `Char` | Link permanente na Fonte Ouro institucional (ex: `http://repositorio.ipen.br/handle/12345/6789`). |
| `isbn_issn` | Código ISBN ou ISSN | `Char` | Identificador de livro ou periódico. |
| `journal_conference_name` | Nome do Veículo / Periódico / Evento | `Char` | Nome do periódico científico, anais de conferência ou órgão concessionário. |
| `qualis_stratum` | Estrato Qualis / Qualis Tecnológico | `Selection` | `A1`, `A2`, `A3`, `A4`, `B1`, `B2`, `B3`, `B4`, `C`, `T1`, `T2`, `T3`, `T4`, `T5`, `TNC`. |
| `oai_pmh_xml_payload` | Payload XML Gerado (`oai_capes`) | `Text` | XML gerado pelo método `action_generate_oai_payload()` para alinhamento com DSpace e Coleta CAPES. |
| `state` | Situação da Produção | `Selection` | `draft` (Rascunho), `validated` (Validado CPG), `exported` (Exportado DSpace / Sucupira). |

## 2. Crosswalk Semântico e Exportação OAI-PMH (`oai_capes`)

Ao acionar a validação via `action_generate_oai_payload()`, o sistema injeta no campo `oai_pmh_xml_payload` o manifesto XML formatado:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<oai_capes:thesis xmlns:oai_capes="http://capes.gov.br/oai/oai_capes/">
    <oai_capes:programCode>{snpg_code}</oai_capes:programCode>
    <oai_capes:title>{name}</oai_capes:title>
    <oai_capes:publicationYear>{publication_year}</oai_capes:publicationYear>
    <oai_capes:identifier>{doi ou handle}</oai_capes:identifier>
    <oai_capes:author>
        <oai_capes:name>{nome_autor}</oai_capes:name>
        <oai_capes:orcid>{orcid_autor}</oai_capes:orcid>
    </oai_capes:author>
    <oai_capes:institutionRor>{ror_code}</oai_capes:institutionRor>
    <oai_capes:qualisStratum>{qualis_stratum}</oai_capes:qualisStratum>
</oai_capes:thesis>
```

A ação `action_mark_exported()` formaliza a transição do lote para a situação `exported` após confirmação do harvesting ou ingestão no repositório institucional.