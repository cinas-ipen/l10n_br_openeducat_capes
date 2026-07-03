# Dicionário de Dados DAV: Módulo 01 - Dados Básicos e Infraestrutura

**Objetivo:** Mapear a ontologia primária (IES, Endereços, Programas, Áreas e Linhas) baseada na extração JSON da CAPES para o esquema relacional do Odoo.

## 1. Instituição de Ensino Superior (IES) e Campus (`res.company` / `res.partner`)
| Campo Odoo | Metadado JSON DAV | Tipo de Dado Odoo | Domínio / Validação JSON |
| :--- | :--- | :--- | :--- |
| `name` | Nome da IES / Campus | `Char` | Obrigatório. Texto livre. |
| `name_en` | Nome da IES em inglês | `Char` | Texto livre. |
| `isni_code` | ISNI | `Char` | Validação: https://isni.org/ |
| `ror_id` | Registro de Org. de Pesquisa (ROR)| `Char` | Validação: https://ror.org/ |
| `cnpj` | CNPJ da IES / Campus | `Char` | Numérico. Módulo 11. |
| `capes_code` | Código da IES na Capes | `Char` | Numérico. Fonte Ouro: Cadastro de IES. |
| `emec_code` | Código e-MEC da IES | `Char` | Alfanumérico. Fonte Ouro: E-MEC. |
| `acronym` | Sigla da IES | `Char` | Redução do nome completo. |
| `admin_category`| Categoria administrativa | `Selection` | Pública (Municipal, Estadual, Federal), Privada (com/sem fins lucrativos), Especial. |
| `sub_category` | Sub-categoria (Privadas) | `Selection` | Comunitárias, Confessionais, Filantrópicas. |
| `academic_org` | Organização Acadêmica | `Selection` | Faculdades, Centros Univ., Universidades, IFs, Escola de governo. |
| `pro_rector_name`| Nome do Pró-Reitor de Pós | `Char` | Texto livre. |
| `pro_rector_start`| Início atuação do Pró-Reitor| `Date` | AAAA-MM-DD. |
| `pro_rector_end`| Fim atuação do Pró-Reitor | `Date` | AAAA-MM-DD. |

## 2. Georreferenciamento e Endereço Institucional
| Campo Odoo | Metadado JSON DAV | Tipo de Dado Odoo | Domínio / Validação JSON |
| :--- | :--- | :--- | :--- |
| `street` | Logradouro do endereço | `Char` | Texto livre. |
| `street_number` | Número do logradouro | `Char` | Numérico. |
| `street2` | Complemento do endereço | `Char` | Texto livre. |
| `district` | Bairro do endereço | `Char` | Texto livre. |
| `zip` | CEP do endereço | `Char` | Numérico. |
| `city_id` | Município do endereço | `Many2one` | Tabela Municípios IBGE. |
| `state_id` | Unidade Federativa do endereço | `Many2one` | Tabela UFs Brasil. |
| `country_id` | País do endereço | `Many2one` | Tabela Países IBGE. |
| `po_box` | Caixa postal do endereço | `Char` | Numérico. |
| `ibge_code` | Código do município no IBGE | `Char` | 7 dígitos numéricos. |
| `siafi_code` | Código do município no SIAFI| `Char` | Tabela SIAFI. |
| `mesoregion_id` | Identificador da mesorregião | `Char` | Numérico. |
| `microregion_id`| Identificador da microrregião| `Char` | Numérico. |
| `latitude` | Latitude do endereço | `Float` | Graus decimais. |
| `longitude` | Longitude do endereço | `Float` | Graus decimais. |

## 3. Programa de Pós-Graduação (PPG) (`op.program.capes`)
| Campo Odoo | Metadado JSON DAV | Tipo de Dado Odoo | Domínio / Validação JSON |
| :--- | :--- | :--- | :--- |
| `capes_id` | Identificador do Programa | `Integer` | Numérico. |
| `snpg_code` | Código do PPG no SNPG | `Char` | Numérico (8+5 dígitos). |
| `name` | Nome do Programa | `Char` | Tabela Sucupira. |
| `lang` | Idioma do Nome do PPG | `Selection` | Tabela ISO 639. |
| `phone` | Telefone do Programa | `Char` | Numérico. |
| `website` | Site do Programa | `Char` | Texto livre (URL). |
| `modality` | Modalidade do Programa | `Selection` | Acadêmica, Profissional. |
| `teaching_modal`| Modalidade de ensino | `Selection` | Ensino presencial, Ensino a distância. |
| `operation_form`| Forma de atuação | `Selection` | Singular, Assoc. Interinstitucional, Assoc. Intrainstitucional. |
| `ies_role` | Atuação da IES/Campus | `Selection` | Coordenadora, Associada, Nucleadora, Colaboradora. |
| `school_term` | Regime Letivo do Programa | `Selection` | Bimestral, Trimestral, Quadrimestral, Semestral, Anual. |
| `status` | Situação do Programa | `Selection` | Em projeto, Em funcionamento, Em desativação, Desativado, Perda de eficácia, Suspensão. |
| `start_date` | Data de Início do Programa | `Date` | AAAA-MM-DD. |
| `end_date` | Data de Encerramento | `Date` | AAAA-MM-DD. |
| `recommend_date`| Data de recomendação | `Date` | AAAA-MM-DD. |
| `recognize_date`| Data de reconhecimento | `Date` | AAAA-MM-DD. |
| `general_coord` | Coordenador do Programa | `Many2one` | FK para Docente. |
| `local_coord` | Coordenador Local do PPG | `Many2one` | FK para Docente. |

### 3.1. Áreas de Avaliação e Curso
| Campo Odoo | Metadado JSON DAV | Tipo de Dado Odoo | Domínio / Validação JSON |
| :--- | :--- | :--- | :--- |
| `evaluation_area`| Código da área de avaliação | `Char` | Tabela de Áreas Capes. |
| `broad_area` | Cód. grande área (Nível 1) | `Char` | Tabela Capes. |
| `basic_area` | Cód. área básica (Nível 2) | `Char` | Tabela Capes. |
| `subarea` | Cód. subárea (Nível 3) | `Char` | Tabela Capes. |
| `specialty` | Cód. especialidade (Nível 4)| `Char` | Tabela Capes. |
| `capes_grade` | Nota do curso | `Selection` | 1, 2, 3, 4, 5, 6, 7, A. |
| `grade_year` | Ano base atribuição da nota | `Integer` | AAAA. |
| `total_credits` | Créditos para titulação | `Integer` | Numérico. |

## 4. Área de Concentração e Linhas de Pesquisa
| Campo Odoo | Metadado JSON DAV | Tipo de Dado Odoo | Domínio / Validação JSON |
| :--- | :--- | :--- | :--- |
| `area_capes_id` | Identificador da Área | `Integer` | Numérico. |
| `area_name` | Nome da Área de Concentração| `Char` | Texto livre. |
| `line_capes_id` | Identificador da Linha | `Integer` | Numérico. |
| `line_name` | Nome da Linha de Pesquisa | `Char` | Texto livre. |
| `description` | Descrição (Área/Linha) | `Text` | Texto explicativo. |
| `start_date` | Data de início (Área/Linha) | `Date` | AAAA-MM-DD. |
| `end_date` | Data encerramento (Área/Linha)|`Date` | AAAA-MM-DD. |