# Ecossistema `l10n_br_openeducat_capes`
### Módulos de Localização Brasileira do OpenEduCat para Pós-Graduação *Stricto Sensu* (Odoo 19.0)

[![Odoo Version](https://img.shields.io/badge/Odoo-19.0-purple.svg)](https://www.odoo.com/)
[![OpenEduCat Version](https://img.shields.io/badge/OpenEduCat-19.0-blue.svg)](https://openeducat.org/)
[![GoPG CAPES](https://img.shields.io/badge/CAPES-GoPG%20Compliant-green.svg)](https://www.gov.br/capes/)
[![Portaria MEC 70/2025](https://img.shields.io/badge/MEC-Portaria%2070%2F2025%20(Diploma%20Digital)-orange.svg)](https://www.in.gov.br/)
[![License LGPL-3.0](https://img.shields.io/badge/License-LGPL--3.0-blue.svg)](LICENSE)
[![Docker Ready](https://img.shields.io/badge/Docker-Ready-blue?logo=docker)](https://www.docker.com/)

O **`l10n_br_openeducat_capes`** é uma suíte completa de módulos de localização brasileira para o **Odoo 19.0** e **OpenEduCat 19.0**, projetada para qualquer Programa de Pós-Graduação *Stricto Sensu* (Mestrado Acadêmico, Mestrado Profissional, Doutorado e Doutorado Direto) de Instituições de Ensino Superior (IES) e Institutos de Pesquisa no Brasil.

O ecossistema atende integralmente às diretrizes do **Programa GoPG da CAPES (Portaria nº 158/2023)**, à **Instrução Normativa nº 1/2026 (RICA|PG)**, ao **Qualis Tecnológico (Diretrizes GTPT)**, às regras de **Concessão e Acúmulo de Bolsas de Estudo (Portaria CAPES nº 133/2023)** e às exigências de **Diplomas Digitais Nato-Digitais (Portaria MEC nº 70/2025)** sob o paradigma constitucional do **Ato Jurídico Perfeito (CF/88)**.

---

## 🏛️ Topologia do Monorepo (9 Submódulos)

O monorepo está estruturado sob os princípios de *Domain-Driven Design* (DDD) em 9 submódulos desacoplados com dependências estritas:

```text
l10n_br_openeducat_capes/
├── l10n_br_openeducat_capes_core         # Identidade Soberana Discente (RA perene), PIDs biográficos (ORCiD, Lattes, CPF), IES, PPGs (Código SNPG)
├── l10n_br_openeducat_capes_admission    # Editais de Seleção Pública, Cotas Sociais/Raciais, Fases Ponderadas e Conversão com Preservação de RA
├── l10n_br_openeducat_capes_academic     # Versionamento Regimental (op.curriculum.version), Multi-Vínculo, Aluno Especial, Trânsito Intra-IES e Livro-Razão (append-only)
├── l10n_br_openeducat_capes_research     # Projetos de Pesquisa, Linhas de Pesquisa e Taxonomia Internacional CRediT
├── l10n_br_openeducat_capes_thesis       # Ritos Bipartidos (Seminários/Qualificação/Defesa), Bancas Examinadoras com Auditoria Cível e Depósito DSpace
├── l10n_br_openeducat_capes_ptt          # Produtos Técnico-Tecnológicos, 4 Eixos, 21 Tipologias CAPES, Maturidade TRL 1-9 e Qualis Tecnológico
├── l10n_br_openeducat_capes_integration  # Barramento REST JSON v1 (Fonte Prata) e Crosswalk DSpace OAI-PMH (Fonte Ouro)
├── l10n_br_openeducat_capes_diploma      # Histórico Consolidado QWeb, Diploma Nato-Digital (MEC 70/2025) e Registro Externo (IPEN -> USP)
└── l10n_br_openeducat_capes_scholarship  # Gestão de Cotas de Bolsas (CAPES/CNPq/CNEN/FAPs), Editais, Avaliação Paralela e Termos de Outorga
```

### Matriz de Dependências entre Submódulos

| Submódulo Odoo | Dependências Obrigatórias (`depends`) | Responsabilidade Central |
| :--- | :--- | :--- |
| `l10n_br_openeducat_capes_core` | `['openeducat_core']` | Identidade Soberana, PIDs e Infraestrutura Base |
| `l10n_br_openeducat_capes_admission` | `['l10n_br_openeducat_capes_core']` | Editais de Ingresso e Planos de Trabalho |
| `l10n_br_openeducat_capes_academic` | `['l10n_br_openeducat_capes_core']` | Motor Curricular, Livro-Razão e Governança CPG |
| `l10n_br_openeducat_capes_research` | `['l10n_br_openeducat_capes_academic', 'project']` | Projetos de Fomento e Papéis CRediT |
| `l10n_br_openeducat_capes_thesis` | `['academic', 'admission', 'research']` | Ritos Intermediários/Finais e Bancas |
| `l10n_br_openeducat_capes_ptt` | `['core', 'academic', 'thesis']` | Produtos Tecnológicos e Qualis T1-T5 |
| `l10n_br_openeducat_capes_integration` | `['core', 'ptt']` | Barramento RESTful RICA\|PG e DSpace |
| `l10n_br_openeducat_capes_diploma` | `['core', 'academic', 'thesis']` | Histórico Consolidado e Diploma MEC 70/2025 |
| `l10n_br_openeducat_capes_scholarship` | `['core', 'academic', 'admission']` | Livro de Cotas, Baremas e Termos de Bolsas |

---

## 🐳 Execução via Docker e Docker Compose

O ecossistema dispõe de ambiente Docker conteinerizado pré-configurado com **Odoo 19.0** e **PostgreSQL 16** (com extensões `unaccent` e `pg_trgm`).

### 1. Pré-requisitos
- Docker Engine $\ge 24.0$
- Docker Compose Plugin $\ge 2.20$
- Git

### 2. Baixar Dependências do OpenEduCat
Antes de iniciar os contêineres, execute o script para baixar e preparar a dependência `openeducat_core` na pasta `external_addons/`:

```bash
./scripts/fetch_dependencies.sh
```

### 3. Configurar Variáveis de Ambiente
Copie o arquivo de exemplo `.env.example` para `.env` e ajuste as senhas e portas conforme necessário:

```bash
cp .env.example .env
```

### 4. Iniciar o Ambiente Docker
Para construir a imagem customizada do Odoo 19 e subir o stack de serviços:

```bash
docker compose up -d --build
```

### 5. Acessar a Aplicação
- **URL do Odoo:** [http://localhost:8069](http://localhost:8069)
- **Master Password (para gerenciar Bancos de Dados):** Constante no `.env` (`ODOO_ADMIN_PASSWD`).

---

## 🧪 Cenários de Dados Sintéticos e Validação Experimental

O repositório fornece ferramentas completas para geração e carga de dados sintéticos realistas, permitindo testar e demonstrar todas as funcionalidades do sistema sem expor dados pessoais reais.

### Como os Dados Sintéticos Foram Gerados
Os conjuntos de dados são gerados pelo script procedural `scripts/gerador_dados_sinteticos.py`:
1. **Reprodutibilidade Matemática Estrita:** Executado com semente determinística fixa (`random.Random(2026)`). Qualquer nova geração sob a mesma seed reproduz exatamente o mesmo dataset relacional.
2. **Onomástica Brasileira Real e 100% Única:** Os nomes de alunos e docentes são gerados a partir de combinações reais da onomástica brasileira particionados em `first_name`, `middle_name` e `last_name`, garantindo que **nenhum discente ou docente compartilhe o mesmo nome completo**, eliminando sufixos artificiais e ambiguidades.
3. **Censo Completo da CAPES (305 Metadados DAV):** Inclui filiação materna, raça/cor (IBGE), declaração de deficiência (PCD), naturalidade com código IBGE de municípios, nacionalidade, títulos de graduação, links canônicos do Currículo Lattes e PIDs biográficos universais (ORCiD e CPF com validação Módulo 11).
4. **Cenários Pré-Construídos Disponíveis em `import_templates/datasets_sinteticos/`:**
   * **`mptrcs_ipen`:** Cenário de referência do Mestrado Profissional em Tecnologia das Radiações em Saúde do IPEN-CNEN/SP (Turmas T1 a T4, 60 discentes, 12 docentes, áreas/linhas de pesquisa, livro-razão de créditos, bancas examinadoras, produtos PTT, governança de atas CPG e registro de diplomas na USP).
   * **`universidade_xyzq`:** Cenário de universidade multicampi com 4 programas (3 acadêmicos e 1 profissional, turmas T1 a T9).

### Como Carregar o Cenário Sintético no Sistema
Para carregar o cenário completo do MPTRCS com todos os seus vínculos, livro-razão e reuniões de CPG diretamente no banco Odoo:

```bash
# Executa a carga via API ORM do Odoo dentro do contêiner
docker compose exec odoo python3 /workspace/scripts/carregar_cenario_mptrcs.py
```

### Perfis de Usuário Pré-Configurados para Testes (Cenário MPTRCS)

| Login | Perfil / Papel | Senha de Teste | Atribuições Principais |
| :--- | :--- | :--- | :--- |
| `admin` | Administrador de TI / Sistema | `admin` | Gestão de parâmetros globais, base de dados e módulos Odoo. |
| `secretaria` | Secretaria Acadêmica | `secretaria123` | Matrículas, cadastros discentes, livro-razão, bolsas, históricos e diplomas. |
| `coordenador` | Coordenador do Programa | `coordenador123` | Presidência da CPG, homologação de bancas, acompanhamento de prazos e bolsas. |
| `vicecoordenador` | Vice-Coordenador do Programa | `vicecoordenador123` | Apoio à coordenação e substituição em deliberações colegiadas. |
| `professor` | Docente e Orientador | `professor123` | Diário de classe, notas, planos de trabalho, bancas e pareceres de bolsas. |

---

## 🧹 Como Zerar a Base e Colocar em Produção de Verdade

Após experimentar e validar o sistema com os dados sintéticos, utilize um dos procedimentos abaixo para limpar os registros de teste e preparar o ambiente para produção real:

### Procedimento A: Criação de Nova Base Limpa via Gerenciador Web (Recomendado)
1. Acesse o Gerenciador de Bancos de Dados: [http://localhost:8069/web/database/manager](http://localhost:8069/web/database/manager).
2. Localize a base de dados de testes (ex.: `mptrcs_ipen_prod`) e clique em **Delete / Drop Database** informando a Master Password.
3. Clique em **Create Database**:
   * **Database Name:** Nome oficial de produção (ex.: `ppg_producao` ou `mptrcs_oficial`).
   * **Email / Senha:** E-mail oficial e senha mestra forte do administrador institucional.
   * **Language:** `Portuguese (BR) / Português (BR)`.
   * **Country:** `Brazil / Brasil`.
   * **Demo data:** ⏹️ **DEIXAR DESMARCADO (UNCHECKED)**. *Nunca ative demo data em produção.*
4. Acesse **Aplicativos**, atualize a lista de apps, remova o filtro "Aplicativos" e instale o módulo topo:
   * **`l10n_br_openeducat_capes_scholarship`** ou **`l10n_br_openeducat_capes_diploma`** (que instalará automaticamente em cascata todos os submódulos necessários).
5. Siga a sequência oficial de cadastros descrita na **Parte I do Manual Unificado do Usuário**.

### Procedimento B: Reinicialização Total do Stack Docker (Purga de Volumes)
Caso deseje purgar completamente o banco PostgreSQL e reinstalar do zero:

```bash
# 1. Parar contêineres e remover volumes persistentes do PostgreSQL
docker compose down -v

# 2. Reconstruir e subir o ambiente limpo
docker compose up -d --build

# 3. Acessar http://localhost:8069/web/database/manager e criar a base sem demo data
```

---

## 🔄 Principais Destaques Arquiteturais

1. **Identidade Soberana Discente (RA Perene):** Cada aluno possui um Registro Acadêmico único e vitalício por IES/empresa (`res.company`), indexado por CPF. Ex-alunos especiais convertidos em regulares mantêm seu número de RA original.
2. **Ciclo de Vida do Aluno Especial & Decadência de 36 Meses:** Disciplinas cursadas no regime especial entram no Livro-Razão como `subject_special_quarantine`. Possuem validade máxima de 36 meses para incorporação formal via CPG. Na emissão do histórico final regular, registros em quarentena não aproveitados são omitidos automaticamente (`omit_on_regular`).
3. **Trânsito Acadêmico Intra-IES vs. Extra-IES:** Disciplinas de outros programas da mesma IES entram com 100% do valor nominal (`subject_intra_ies`). No caso específico IPEN/USP, o programa de Tecnologia Nuclear da USP constitui juridicamente outra IES perante o MPTRCS (IPEN), computando como créditos externos (`subject_extra_ies`).
4. **Governança de Cotas e Editais de Bolsas (`scholarship`):**
   * **Desvinculação Financeira:** O PPG não processa a folha bancária (o pagamento é direto entre a agência — CAPES, CNPq, CNEN, FAPs — e o discente). O sistema gerencia o Livro de Cotas, editais, vigências, limite máximo (24m Mestrado / 48m Doutorado) e assiduidade ($\ge 80\%$).
   * **Avaliação em 4 Colunas com Revisores Paralelos:** Candidato preenche a autoavaliação (Coluna 1); Revisor 01 (Coluna 2) e Revisor 02 (Coluna 3) avaliam concomitantemente e às cegas; Comissão de Bolsas / CPG consolida a nota final (Coluna 4).
   * **Conformidade com a Portaria CAPES nº 133/2023:** Controle de acúmulo de bolsa com vínculo empregatício e deliberação da CPG.
   * **Ações Afirmativas:** Vagas reservadas para Pretos, Pardos e Indígenas (PPI) com regra de reversão de cotas remanescentes para ampla concorrência.
5. **Ato Jurídico Perfeito no Livro-Razão (`op.student.credit.ledger`):** Registros acadêmicos operam estritamente em modo *append-only* (`unlink` bloqueado), blindando integralizações históricas contra alterações retroativas de regimento.
6. **Governança da CPG por Clique Auditável (`op.cpg.approval.log`):** Mandato de 6 membros titulares e 4 suplentes com registro perene de User ID, Timestamp e IP dos votantes nas reuniões mensais.
7. **Visão 360° Discente e Docente:** Navegação instantânea por smart buttons e botão direto no cabeçalho discente para emissão do Histórico Escolar Oficial com QR Code e Hash SHA-256.

---

## 📚 Documentação Oficial do Ecossistema (`docs/`)

A suíte documental completa está disponível e estruturada no diretório [`docs/`](docs):

- **[Portal da Documentação (`index.html`)](docs/index.html):** Hub central com navegação estruturada e estilizada para todos os documentos técnicos.
- **[Manual Unificado do Usuário (Quarto Book)](docs/11_manuais_operacionais/manual_do_usuario_posgraduacao.html):** Manual completo no modelo livro separado em 5 Partes (Administração em Base Zerada, Secretaria, Coordenação/CPG, Professores e Alunos) em arquivo HTML 100% autocontido (`embed-resources: true`).
- **[Documentação Executiva e Arquitetural (Quarto)](docs/documentacao_executiva_capes.html):** Visão executiva de alto nível com diagramas de processos, fontes de dados e matriz GoPG.
- **[01_arquitetura_sistemica](docs/01_arquitetura_sistemica):** Paradigma GoPG, Fontes Ouro/Prata e Topologia do Monorepo.
- **[02_governanca_regimental_e_creditos](docs/02_governanca_regimental_e_creditos):** Motor de Versionamento Curricular, Aluno Especial e Livro-Razão.
- **[03_dicionarios__de_dados_dav](docs/03_dicionarios__de_dados_dav):** Dicionários de Dados da DAV Módulos 01 a 06 (305 metadados CAPES).
- **[04_processos_da_vida_academica](docs/04_processos_da_vida_academica):** Editais de Admissão, Gestão de Bolsas e Motor Cronológico de Prazos.
- **[05_produtos_tecnico_tecnologicos_ptt](docs/05_produtos_tecnico_tecnologicos_ptt):** Taxonomia GTPT, Qualis Tecnológico (T1 a T5) e TRL 1-9.
- **[06_titulacao_e_conformidade_documental](docs/06_titulacao_e_conformidade_documental):** Ritos de Qualificação/Defesa, Histórico Escolar e Diplomas Digitais (MEC 70/2025).
- **[07_padroes_de_interoperabilidade_externa](docs/07_padroes_de_interoperabilidade_externa):** APIs RESTful Fonte Prata e Crosswalk XSLT DSpace (`oai_capes`).
- **[10_implantacao_e_migracao](docs/10_implantacao_e_migracao):** Guia de Inicialização em Banco Zerado e Protocolo de Carga CSV (Passos 01 a 16).

---

## 🛠️ Comandos Rápidos

```bash
# Baixar dependências do OpenEduCat
./scripts/fetch_dependencies.sh

# Subir ambiente Docker
docker compose up -d --build

# Carregar cenário sintético completo do MPTRCS
docker compose exec odoo python3 /workspace/scripts/carregar_cenario_mptrcs.py

# Acompanhar logs do Odoo
docker compose logs -f odoo

# Parar serviços
docker compose down

# Purgar ambiente para reiniciar com banco zerado
docker compose down -v
```

---

## 📄 Licença

Este projeto é um software livre distribuído sob os termos da licença **GNU Lesser General Public License v3.0 (LGPL-3.0)**. Consulte o arquivo [`LICENSE`](LICENSE) para mais detalhes.
