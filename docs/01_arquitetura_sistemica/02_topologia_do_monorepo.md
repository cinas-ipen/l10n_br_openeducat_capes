# Documento 02: Topologia do Monorepo e Engenharia de Módulos

## 1. Princípios de Design Modular e Domain-Driven Design (DDD) no Odoo

O desenvolvimento da localização brasileira para a pós-graduação *Stricto Sensu* impõe o uso de padrões avançados de arquitetura de software para mitigar acoplamentos destrutivos. O monorepo `l10n_br_openeducat_capes` adota os princípios do Domain-Driven Design (DDD), dividindo as complexidades de negócio em submódulos independentes e isolados no ecossistema Odoo.

Essa separação cirúrgica de responsabilidades garante que falhas pontuais em integrações de APIs externas ou atualizações de layouts documentais de diplomas não gerem impactos ou indisponibilidades no motor acadêmico central e no livro-razão de créditos. A extensibilidade do framework Odoo é explorada através do mecanismo de herança estrita, permitindo que cada submódulo injete campos, visualizações e lógicas específicas apenas em suas respectivas camadas de domínio.

## 2. Arquitetura Detalhada do Monorepo (`l10n_br_openeducat_capes`)

A árvore de diretórios do ecossistema e o escopo funcional e técnico de cada componente estrutural do monorepo estão descritos a seguir:

```text
l10n_br_openeducat_capes/
├── docs/
│   ├── 01_arquitetura_sistemica/
│   ├── 02_governanca_regimental_e_creditos/
│   ├── 03_dicionarios_de_dados_dav/
│   ├── 04_processos_da_vida_academica/
│   ├── 05_produtos_tecnico_tecnologicos_ptt/
│   ├── 06_titulacao_e_conformidade_documental/
│   └── 07_padroes_de_interoperabilidade_externa/
├── l10n_br_openeducat_capes_core/
├── l10n_br_openeducat_capes_admission/
├── l10n_br_openeducat_capes_academic/
├── l10n_br_openeducat_capes_research/
├── l10n_br_openeducat_capes_thesis/
├── l10n_br_openeducat_capes_ptt/
├── l10n_br_openeducat_capes_integration/
└── l10n_br_openeducat_capes_diploma/

```

### 2.1. `l10n_br_openeducat_capes_core`

* **Escopo:** Mapeia a ontologia primária e as entidades estáticas fundamentais do Módulo 01 e Módulo 02 do dicionário de dados da DAV.
* **Modelos Estendidos/Criados:** `res.company`, `res.partner`, `op.program.capes`, `op.faculty`, `op.student`.
* **Responsabilidade Técnica:** Armazenar os códigos SNPG e e-MEC, estruturar os georreferenciamentos de campi e gerenciar a injeção rígida dos Identificadores Persistentes (PIDs) acadêmicos universais (ORCiD, Lattes, ROR e ISNI).

### 2.2. `l10n_br_openeducat_capes_admission`

* **Escopo:** Substitui o fluxo linear de inscrição de alunos nativo do OpenEduCat por uma estrutura de concorrência pública baseada em normas brasileiras.
* **Modelos Estendidos/Criados:** `op.admission.register`, `op.admission.edital`, `op.edital.phase`, `op.student.work_plan`.
* **Responsabilidade Técnica:** Gerenciar editais parametrizáveis com tabelas One2many para fases de seleção com pontuações ponderadas, controle de ações afirmativas (cotas de 20%), ranqueamento eliminatório/classificatório, mecanismo de Aprovação por Soberania do Coordenador (`is_override`), gatilho de evasão precoce (3 semanas de ausência) e submissão/avaliação do Plano de Trabalho Discente com trava ética do CEP.

### 2.3. `l10n_br_openeducat_capes_academic`

* **Escopo:** Rege a vida estudantil corrente, orquestra a governança colegiada (CPG) e implementa a inteligência de regras curriculares do Módulo 03 da DAV.
* **Modelos Estendidos/Criados:** `op.subject`, `op.batch`, `op.session`, `op.curriculum.version`, `op.student.credit.ledger`, `op.academic.request`, `op.faculty.program.link`, `op.faculty.category.ledger`, `op.cpg.committee`, `op.cpg.member`, `op.cpg.meeting`.
* **Responsabilidade Técnica:** Versionamento dinâmico de regulamentos, operação do livro-razão imutável de integralização de créditos, automação de matrículas compulsórias de acompanhamento de pesquisa, trava de carga inicial de calouros (mínimo 24 créditos), fluxo de ajuste manual retroativo com selo de auditoria, e gestão de pautas/atas QWeb da CPG com aprovação por clique auditável.

### 2.4. `l10n_br_openeducat_capes_research`

* **Escopo:** Mapeia a estrutura de fomento e atividade de investigação descrita no Módulo 05 da DAV.
* **Modelos Estendidos/Criados:** `capes.research.project`, `capes.project.member`.
* **Responsabilidade Técnica:** Estender as capacidades de gerenciamento de projetos nativas do Odoo para capturar a natureza científica da pesquisa, classificar parcerias interinstitucionais e vincular pesquisadores às entregas operando sob a Taxonomia CRediT.

### 2.5. `l10n_br_openeducat_capes_thesis`

* **Escopo:** Governa as regras acadêmicas de ritos de passagem intermediários e finais do Módulo 04 da DAV.
* **Modelos Estendidos/Criados:** `capes.thesis`, `capes.thesis.committee`.
* **Responsabilidade Técnica:** Orquestrar o fluxo bipartido (Seminário Geral de Área/Qualificação e Defesa com quórum e composição de PhDs parametrizáveis por regimento via `op.curriculum.committee.rule`), auditar pré-requisitos do Plano de Trabalho homologado, gerenciar o processamento de impedimentos éticos e endogenia em comissões julgadoras, registrar cronometria de exposição/arguição (50 min / 40 min) e controlar o prazo limite de 30 dias para depósito da versão eletrônica no DSpace.

### 2.6. `l10n_br_openeducat_capes_ptt`

* **Escopo:** Internaliza a taxonomia e a engenharia de avaliação qualitativa do Grupo de Trabalho de Produção Técnica (GTPT) e Comitê Medicina II da CAPES para programas profissionais.
* **Modelos Estendidos/Criados:** `capes.ptt.axis`, `capes.ptt.type`, `capes.ptt.product`, `capes.ptt.evaluation`.
* **Responsabilidade Técnica:** Processar o motor de regras do Qualis Tecnológico, validar de forma eliminatória a aderência institucional de produções intelectuais, mapear níveis de Maturidade Tecnológica (TRL 1-9) e computar a média de notas para estratificação em tempo real (T1 a T5 ou TNC) servindo como pré-requisito de defesa e gerador de créditos APO.

### 2.7. `l10n_br_openeducat_capes_integration`

* **Escopo:** Concentra a inteligência de conectividade e o mapeamento semântico de comunicação externa da DAV Módulo 06.
* **Modelos Estendidos/Criados:** `capes.intellectual.production`.
* **Responsabilidade Técnica:** Expor controladores RESTful (rotas HTTP `/api/capes/v1/`) para transmissão de payloads JSON criptografados para a rede RICA|PG, gerenciar as autorizações OAuth 2.0 e atuar como barramento unificado de cruzamento semântico com os esquemas de conversão XSLT do DSpace (`oai_capes`).

### 2.8. `l10n_br_openeducat_capes_diploma`

* **Escopo:** Garante a conformidade jurídica de encerramento de percurso e expedição documental de graus acadêmicos em conformidade com o MEC (Portaria nº 70/2025).
* **Modelos Estendidos/Criados:** `op.student.transcript.br`.
* **Responsabilidade Técnica:** Renderizar relatórios QWeb consolidados de históricos parciais/finais auto-autenticados com Hash SHA-256 e QR Code, gerar arquivos XML estruturados de diplomas de pós-graduação e documentação acadêmica digital, e orquestrar rotinas criptográficas Python para aplicação de assinaturas avançadas XAdES ICP-Brasil (Certificado A3/HSM) com Carimbos de Tempo.

## 3. Matriz de Dependências e Manifestos do Odoo (`__manifest__.py`)

Para assegurar a integridade do monorepo e a correta carga de dados no banco relacional PostgreSQL, a árvore de dependências do Odoo é rigorosamente respeitada. Cada submódulo possui um arquivo descriptor `__manifest__.py` indicando suas dependências obrigatórias de inicialização:

```text
[openeducat_core]
^
|
[l10n_br_openeducat_capes_core] <---------------------------------------+
^                     ^                                          |
|                     |                                          |
[l10n_br_openeducat_capes_admission] <───┐                         |
^                                │                         |
|                                │                         |
[l10n_br_openeducat_capes_academic] <---+│                         |
^                                |│                        |
|                                ||                        |
[l10n_br_openeducat_capes_research]     ||                        |
^                                |│                        |
|                                ||                        |
[l10n_br_openeducat_capes_thesis] ------+┘                        |
^                                ^                         |
|                                |                         |
[l10n_br_openeducat_capes_ptt] ---------+                         |
^                                                          |
|                                                          |
[l10n_br_openeducat_capes_integration]                            |
^                                                          |
|                                                          |
[l10n_br_openeducat_capes_diploma] -------------------------------+

```

Abaixo está a especificação exata das chaves `depends` presentes em cada manifesto de domínio:

| Submódulo Odoo | Módulos Obrigatórios em `depends` | Tipo de Dependência |
| --- | --- | --- |
| `l10n_br_openeducat_capes_core` | `['openeducat_core']` | Extensão Base de Infraestrutura |
| `l10n_br_openeducat_capes_admission` | `['l10n_br_openeducat_capes_core']` | Extensão do Fluxo de Admissão e Plano de Trabalho |
| `l10n_br_openeducat_capes_academic` | `['l10n_br_openeducat_capes_core']` | Motor Curricular, Regimentos e CPG |
| `l10n_br_openeducat_capes_research` | `['l10n_br_openeducat_capes_academic', 'project']` | Integração Odoo Projects e Fomento |
| `l10n_br_openeducat_capes_thesis` | `['l10n_br_openeducat_capes_academic', 'l10n_br_openeducat_capes_admission', 'l10n_br_openeducat_capes_research']` | Ritos Bipartidos, Plano de Trabalho e Qualificação |
| `l10n_br_openeducat_capes_ptt` | `['l10n_br_openeducat_capes_core', 'l10n_br_openeducat_capes_academic', 'l10n_br_openeducat_capes_thesis']` | Qualis, Eixos GTPT e Trava PTT |
| `l10n_br_openeducat_capes_integration` | `['l10n_br_openeducat_capes_core', 'l10n_br_openeducat_capes_ptt']` | Barramento RESTful e OAI-PMH |
| `l10n_br_openeducat_capes_diploma` | `['l10n_br_openeducat_capes_core', 'l10n_br_openeducat_capes_academic', 'l10n_br_openeducat_capes_thesis']` | Conformidade MEC, Teses e Criptografia |

## 4. Modelo de Extensibilidade e Herança Estrita (`_inherit`)

A arquitetura baseia-se prioritariamente no mecanismo de herança de tabelas e objetos (`_inherit`) nativo do ORM do Odoo, preservando o núcleo original e injetando modificações nas tabelas relacionais do PostgreSQL sem corromper a integridade dos dados originais.

* **Herança Clássica (`_inherit = 'res.partner'`):** Adotada para embutir de maneira transparente as extensões de PIDs biográficos e civis sem alterar as capacidades originais de faturamento, CRM ou contabilidade associadas à classe de contatos nativa do Odoo.
* **Herança Funcional de Workflow:** Submódulos avançados estendem as máquinas de estado originais reescrevendo métodos Python em instâncias como `op.admission.register`, injetando decoradores `@api.constrains` para bloquear transições de estado lineares caso inconsistências com regulamentos ou ausência de validação de proficiências sejam detectadas no banco de dados.
