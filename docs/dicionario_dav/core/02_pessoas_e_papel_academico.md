# Dicionário de Dados DAV: Módulo 02 - Pessoas e Papéis Acadêmicos

**Objetivo:** Mapear a herança biográfica e as extensões de papéis acadêmicos baseados no JSON da CAPES.

## 1. Classe Base: Pessoa (`res.partner`)
| Campo Odoo | Metadado JSON DAV | Tipo de Dado Odoo | Domínio / Validação JSON |
| :--- | :--- | :--- | :--- |
| `capes_id` | Identificador na Capes | `Integer` | Numérico. |
| `internal_code` | Identificador na Instituição| `Char` | Alfanumérico. |
| `name` | Nome da pessoa | `Char` | Texto livre (inclui nome social). |
| `fiscal_name` | Nome fiscal da pessoa | `Char` | Texto exato Receita Federal. |
| `cpf` | Número do CPF | `Char` | Numérico (Receita Federal). |
| `mother_name` | Nome da mãe | `Char` | Texto livre. |
| `birth_date` | Data de nascimento | `Date` | AAAA-MM-DD. |
| `gender` | Sexo biológico | `Selection` | Feminino, Masculino, Intersexo, Não declarado. |
| `race_color` | Raça/Cor | `Selection` | Branca, Preta, Parda, Amarela, Indígena, Não declarada. |
| `has_disability`| Pessoa com deficiência | `Boolean` | Sim; Não. |
| `nationality` | Nacionalidade | `Char` | Texto livre. |
| `birth_country` | País de nascimento | `Many2one` | Tabela IBGE. |
| `birth_state` | UF do nascimento | `Selection` | AL, AP, AM, BA... |
| `birth_city` | Município do nascimento | `Many2one` | Tabela IBGE. |
| `email` | Endereço de e-mail | `Char` | Texto livre. |
| `social_url` | URL da Rede Social | `Char` | Alfanumérico. |

### 1.1. Identificadores (PIDs) e Formação
| Campo Odoo | Metadado JSON DAV | Tipo de Dado Odoo | Domínio / Validação JSON |
| :--- | :--- | :--- | :--- |
| `orcid` | Identificador ORCiD | `Char` | Alfanumérico. |
| `lattes_url` | Identificador Lattes | `Char` | Alfanumérico. |
| `researcher_id` | Identificador ResearcherID | `Char` | Alfanumérico. |
| `scopus_id` | Scopus Author ID | `Char` | Numérico. |
| `academic_level`| Nível acadêmico | `Selection` | Ens. Fundamental, Médio, Graduação, Pós. |
| `highest_degree`| Grau acadêmico | `Selection` | Bacharelado, Especialização, Mestrado, Doutorado... |

## 2. Docente (`op.faculty`)
| Campo Odoo | Metadado JSON DAV | Tipo de Dado Odoo | Domínio / Validação JSON |
| :--- | :--- | :--- | :--- |
| `category` | Nome da categoria | `Selection` | Docente permanente, visitante, colaborador. |
| `work_regime` | Tipo de dedicação | `Selection` | Dedicação exclusiva, Integral, Parcial. |
| `workload` | Carga horária de atuação | `Integer` | Numérico. |
| `status` | Tipo de situação | `Selection` | Ativo, Inativo, Falecido. |
| `is_retired` | Indicação de aposentadoria | `Boolean` | Sim; Não. |
| `degree_area` | Área de Conhec. Titulação | `Many2one` | Tabela CAPES. |
| `degree_level` | Nível acadêmico da titulação| `Selection` | Mestrado, Doutorado. |
| `degree_ies` | IES da titulação | `Char` | Texto livre. |

## 3. Discente / Pós-Graduando (`op.student`) e Egresso
| Campo Odoo | Metadado JSON DAV | Tipo de Dado Odoo | Domínio / Validação JSON |
| :--- | :--- | :--- | :--- |
| `status` | Tipo de situação | `Selection` | Matriculado, Abandono, Desligado, Titulado, Falecido. |
| `admission_date`| Data de ingresso | `Date` | AAAA-MM-DD. |
| `promotion` | Promoção mudança de nível | `Boolean` | Sim; Não. |
| `status_date` | Data da situação | `Date` | AAAA-MM-DD. |
| `advisor_id` | Nome do Orientador | `Many2one` | FK para Docente. |
| `coadvisor_id` | Nome do Coorientador | `Many2one` | FK para Docente. |
| `egress_end` | Encerramento vínculo egresso| `Date` | AAAA-MM-DD. |

## 4. Afastamentos (Discentes e Docentes)
| Campo Odoo | Metadado JSON DAV | Tipo de Dado Odoo | Domínio / Validação JSON |
| :--- | :--- | :--- | :--- |
| `leave_type` | Tipo de afastamento | `Selection` | Saúde própria, Doença família, Maternidade, Paternidade... |
| `start_date` | Data início afastamento | `Date` | AAAA-MM-DD. |
| `end_date` | Data encerramento afastamento| `Date` | AAAA-MM-DD. |

## 5. Pós-Doutorando e Externos
| Campo Odoo | Metadado JSON DAV | Tipo de Dado Odoo | Domínio / Validação JSON |
| :--- | :--- | :--- | :--- |
| `supervisor` | Nome do supervisor | `Char` | Texto livre. |
| `foreign_ies` | IES do curso no exterior | `Char` | Texto livre. |
| `acting_ies` | Instituição de atuação | `Many2one` | Cadastro IES Capes. |
| `ext_origin_ies`| IES do Participante Externo | `Char` | Lista e-MEC / CHEA. |