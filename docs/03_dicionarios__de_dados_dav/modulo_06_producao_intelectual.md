# Dicionário de Dados DAV: Módulo 06 - Produção Intelectual

**Objetivo:** Mapear as produções acadêmicas e bibliográficas, com metadados para interoperabilidade OAI-PMH extraídos do JSON 3 e 4.

## 1. Produção Intelectual (`capes.intellectual.production`)
| Campo Odoo | Metadado JSON DAV | Tipo de Dado Odoo | Domínio / Validação JSON |
| :--- | :--- | :--- | :--- |
| `capes_id` | Identificador na Capes | `Integer` | Numérico. |
| `sucupira_id` | Id Sucupira (Relacionada) | `Integer` | Numérico. |
| `main_author` | Autor da produção | `Char` | Nome responsável. |
| `title` | Título da produção | `Char` | Idioma principal. |
| `alt_title` | Título alternativo | `Char` | Em outro idioma. |
| `prod_type` | Tipo de produção | `Selection` | Bibliográfica, Artística, Técnica, Tecnológica. |
| `doc_type` | Tipo de documento | `Selection` | Tabela COAR (Resource Types). |
| `language` | Idioma principal | `Selection` | Lista ISO 639. |
| `pub_date` | Data da publicação | `Date` | AAAA-MM-DD. |
| `access_rule` | Permissão de acesso | `Selection` | Acesso aberto, restrito, embargado. |
| `embargo_end` | Liberação do texto completo | `Date` | AAAA-MM-DD. |
| `uid_type` | Tipo de identificador único | `Selection` | DOI, Handle, Ark, dArk, PubMed Id. |
| `uid_uri` | URI do identificador único | `Char` | URL persistente. |
| `license_uri` | URI da licença autoral | `Char` | Creative Commons, etc. |
| `source_uri` | URI da fonte original | `Char` | Repositório/Editora oficial. |
| `related_uri` | Produção relacionada (URI) | `Char` | Vínculo com projetos/produtos. |
| `abstract_main` | Resumo no idioma principal | `Text` | Texto. |
| `abstract_alt` | Resumo em outro idioma | `Text` | Texto. |
| `keywords_main` | Palavra-chave principal | `Char` | Vocabulário controlado. |
| `keywords_alt` | Palavra-chave outro idioma | `Char` | Vocabulário controlado. |
| `pages_total` | Número total de páginas | `Integer` | Numérico. |
| `page_start` | Página inicial | `Integer` | Numérico. |
| `page_end` | Página final | `Integer` | Numérico. |
| `resp_type` | Tipo de responsabilidade | `Selection` | Autor, Organizador, Editor, Tradutor... |
| `contrib_type` | Tipo de contribuição | `Selection` | Taxonomia CRediT. |

## 2. Detalhamento (Livros, Periódicos e Eventos)
| Campo Odoo | Metadado JSON DAV | Tipo de Dado Odoo | Domínio / Validação JSON |
| :--- | :--- | :--- | :--- |
| `book_title` | Título do livro | `Char` | Texto livre. |
| `collection_title`| Título da coleção | `Char` | Texto livre. |
| `isbn` | Número do ISBN | `Char` | Numérico. |
| `book_edition` | Número da edição do livro | `Integer` | Numérico. |
| `book_volume` | Volume do livro na coleção | `Integer` | Numérico. |
| `pub_place` | Local de publicação | `Char` | Cidade/Editora. |
| `journal_title` | Título do periódico | `Char` | Texto livre. |
| `issn` | Número do ISSN | `Char` | Numérico. |
| `journal_vol` | Número do volume (Periódico)| `Integer` | Numérico. |
| `journal_ed` | Número da edição (Periódico)| `Integer` | Numérico. |
| `event_title` | Título do evento | `Char` | Exclui número da edição. |
| `event_nature` | Natureza trabalho no evento | `Selection` | Resumo, Resumo expandido, Trabalho Curto/Completo. |
| `funder_agency` | Agência de fomento | `Char` | Tabela Financiador Capes. |