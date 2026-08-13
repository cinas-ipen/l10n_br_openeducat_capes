Para expandir e adequar a documentação técnica do ecossistema de localização brasileira (`l10n_br_openeducat_capes`) no Odoo, a estrutura de arquivos do diretório `docs/` deve ser remodelada. Esta nova organização reflete de forma fidedigna a complexidade regulatória do *Stricto Sensu*, os requisitos do programa GoPG da CAPES, o Qualis Tecnológico e as regras de conformidade documental do Ministério da Educação (MEC).

Abaixo está a nova topologia completa da árvore de documentação do projeto e o detalhamento analítico do conteúdo que cada arquivo deve conter.

---

### Nova Estrutura do Diretório `docs/`

```text
docs/
├── 01_arquitetura_sistemica/
│   ├── 01_visao_geral_e_gopg.md              # Paradigma GoPG, RICA|PG e a hierarquia de fontes de dados
│   └── 02_topologia_do_monorepo.md           # Mapeamento de submódulos do Odoo e dependências internas
├── 02_governanca_regimental_e_creditos/
│   ├── 01_motor_de_versionamento.md         # Estrutura do op.curriculum.version e parametrização dinâmica
│   ├── 02_ato_juridico_perfeito_e_hibridismo.md # Regras de transição, direito de opção e travas lógicas
│   └── 03_livro_razao_e_integralizacao.md    # O modelo op.student.credit.ledger e regras de créditos (IPEN/Mackenzie/CDTN)
├── 03_dicionarios__de_dados_dav/
│   ├── modulo_01_dados_basicos_e_infraestrutura.md # Mapeamento Módulo 1 DAV (IES, Campus, PPG, Linhas)
│   ├── modulo_02_pessoas_e_papel_academico.md      # Mapeamento Módulo 2 DAV (PIDs, Docentes, Discentes, Afastamentos)
│   ├── modulo_03_formacao_e_disciplinas.md         # Mapeamento Módulo 3 DAV (Disciplinas, Turmas, Ofertas, PHEA)
│   ├── modulo_04_trabalhos_de_conclusao.md         # Mapeamento Módulo 4 DAV (Teses, Dissertações e Bancas)
│   ├── modulo_05_projetos_e_pesquisa.md            # Mapeamento Módulo 5 DAV (Projetos, Cooperações e CRediT)
│   └── modulo_06_producao_intelectual.md           # Mapeamento Módulo 6 DAV (Produções e Identificadores DOI/Handle)
├── 04_processos_da_vida_academica/
│   ├── 01_editais_de_admissao.md             # Modelagem do op.admission.edital e fases de seleção dinâmicas
│   ├── 02_matricula_de_acompanhamento.md     # Paradigma da inscrição compulsória pós-créditos teóricos
│   ├── 03_motor_cronologico_e_trava_de_prazos.md # Cron Jobs, vedações a trancamentos e fluxo de jubilamento
│   └── 04_portal_e_requerimentos_self_service.md # Módulo op.academic.request e aprovações multinível (mail.thread)
├── 05_produtos_tecnico_tecnologicos_ptt/
│   ├── 01_taxonomia_eixos_e_tipos.md         # Mapeamento dos 4 eixos estruturantes e as 21 tipologias do GTPT
│   ├── 02_qualis_tecnologico_e_workflow.md   # Entidade capes.ptt.product, capes.ptt.evaluation e motor de aderência
│   └── 03_calculo_de_estratos_e_bi.md         # Lógica Python de cálculo de notas, estrato (T1-T5) e Views analíticas
├── 06_titulacao_e_conformidade_documental/
│   ├── 01_rito_bipartido_e_bancas.md         # Qualificação, Defesa, regras de impedimento e especialistas externos
│   ├── 02_historico_escolar_consolidado.md   # Relatório op.student.transcript.br (QWeb combinando ledger e tese)
│   └── 03_diploma_digital_nato_digital.md    # Portaria MEC 70/2025, XML estruturado, assinatura XAdES e RVDD
├── 07_padroes_de_interoperabilidade_externa/
│   ├── 01_apis_rest_json_fonte_prata.md      # Endpoints expostos do Odoo, tokens de segurança e conformidade LGPD
│   └── 02_gopg_coleta_e_crosswalk_dspace.md  # Mapeamento XSLT OAI-PMH, contexto oai_capes e PIDs (DOI, ORCID, ROR)
├── 08_macroprocessos/
│   └── macro-processos.md                    # Modelagem integrada e integral dos 10 Macroprocessos Acadêmicos
└── 09_validacoes_mptrcs/
    ├── mp01_detalhamento_validacao_mptrcs.md # Validação técnica do MP1 (Setup Curricular e Versionamento)
    ├── mp02_detalhamento_validacao_mptrcs.md # Validação técnica do MP2 (Admissão e Plano de Trabalho)
    ├── mp03_detalhamento_validacao_mptrcs.md # Validação técnica do MP3 (Vida Estudantil e Livro-Razão)
    ├── mp04_detalhamento_validacao_mptrcs.md # Validação técnica do MP4 (Prazos, Trancamentos e Jubilamento)
    ├── mp05_detalhamento_validacao_mptrcs.md # Validação técnica do MP5 (Gestão de PTTs e Qualis Tecnológico)
    ├── mp06_detalhamento_validacao_mptrcs.md # Validação técnica do MP6 (Ritos de Titulação e Bancas)
    ├── mp07_detalhamento_validacao_mptrcs.md # Validação técnica do MP7 (Expedição de Diplomas e Integração USP)
    ├── mp08_detalhamento_validacao_mptrcs.md # Validação técnica do MP8 (Interoperabilidade GoPG e DSpace)
    ├── mp09_detalhamento_validacao_mptrcs.md # Validação técnica do MP9 (Governança Docente e Timeline)
    └── mp10_detalhamento_validacao_mptrcs.md # Validação técnica do MP10 (Governança CPG e Atas QWeb)
```

---

### Detalhamento e Especificação do Conteúdo dos Arquivos

#### Diretório 01: Arquitetura Sistêmica

* **`01_visao_geral_e_gopg.md`**
* Detalhamento do Programa de Governança Colaborativa de Informações da Pós-Graduação (GoPG) instituído pela Portaria CAPES nº 158/2023 e Instrução Normativa nº 1/2026.
* Modelagem da coleta ativa e passiva via Rede de Integração da Comunidade Acadêmica da Pós-Graduação (RICA|PG).
* Definição e separação dos três níveis hierárquicos de dados no ecossistema: "Fonte Ouro" (Repositório Institucional DSpace), "Fonte Prata" (Sistema Acadêmico Odoo/OpenEduCat) e "Fonte Bronze" (preenchimento manual residual na Plataforma Sucupira).
* Mapeamento das 5 etapas progressivas de implementação técnica e homologação governamental (T1 a T5).


* **`02_topologia_do_monorepo.md`**
* Descrição da engenharia de requisitos do monorepo Odoo baseado em Domain-Driven Design (DDD).
* Definição de escopo e responsabilidades lógicas de cada diretório/aplicativo interno do ecossistema: `core`, `admission`, `academic`, `research`, `thesis`, `ptt`, `integration` e `diploma`.
* Mapeamento de dependências e heranças estritas entre os módulos (ex: `l10n_br_openeducat_capes_ptt` dependendo obrigatoriamente de `core` e `thesis`).



#### Diretório 02: Governança Regimental e Créditos

* **`01_motor_de_versionamento.md`**
* Especificação técnica da classe `op.curriculum.version` atuando como a entidade centralizadora das regras de negócio mutáveis de um curso.
* Mapeamento de parâmetros dinâmicos de controle como prazo máximo de defesa, créditos mínimos obrigatórios/optativos, exigências de proficiência em inglês e prazos de qualificação.
* Regras para isolar as configurações hardcoded de nível de programa (`op.course`), transferindo-as para instâncias versionadas vinculadas ao aluno por período letivo.


* **`02_ato_juridico_perfeito_e_hibridismo.md`**
* Fundamentação sobre a inexistência de direito adquirido a regimes acadêmicos na jurisprudência brasileira e a aplicação imediata de normas supervenientes a fatos duradouros.
* Definição lógica das travas arquiteturais que impedem o "hibridismo normativo" (combinação casuística de vantagens de regimentos distintos pelo estudante).
* Modelagem do fluxo eletrônico de "Direito de Opção" via portal discente através da máquina de estados do modelo `op.academic.request.regime_migration`.


* **`03_livro_razao_e_integralizacao.md`**
* Modelagem estrutural da classe imutável (padrão *append-only*) `op.student.credit.ledger`, responsável por proteger o Ato Jurídico Perfeito das disciplinas e etapas integralizadas no histórico escolar.
* Arquitetura de parametrização de carga horária variável por unidade de crédito utilizando o decorador Python `@api.depends`.
* Especificação de regras de validação customizadas para atendimento simultâneo aos limites de aproveitamento de créditos de diferentes instituições na mesma base (ex: IPEN com 100 créditos/15h, Mackenzie com 50 créditos/12h e CDTN com 24 ou 47 créditos).



#### Diretório 03: Dicionários de Dados DAV (Mapeamento Semântico)

* **`modulo_01_dados_basicos_e_infraestrutura.md`**
* Extensão de `res.company` e `res.partner` para capturar os metadados do Módulo 1 da DAV: códigos e-MEC, código da IES na CAPES, CNPJ, sigla, categoria administrativa, organização acadêmica e PIDs organizacionais (ISNI e ROR).
* Estruturação relacional de endereços georreferenciados contendo latitude, longitude e códigos oficiais do IBGE e SIAFI.
* Modelagem da classe `op.program.capes` contendo Código SNPG (8+5 dígitos), modalidade (Acadêmica/Profissional), regime letivo, situação e árvore hierárquica do conhecimento da CAPES (Grande Área, Área Básica, Subárea e Especialidade).


* **`modulo_02_pessoas_e_papel_academico.md`**
* Injeção de PIDs biográficos na classe base `res.partner`: campos estruturados e validados para ORCiD, URL do currículo Lattes, ResearcherID e Scopus Author ID.
* Extensão da classe `op.faculty` (Docente) mapeando a categoria de vínculo (Permanente, Visitante, Colaborador), regime de dedicação, carga horária de atuação, indicador booleano de aposentadoria e histórico cronológico.
* Extensão da classe `op.student` (Discente) com diferenciação entre "Aluno Regular" e "Aluno Especial / Matrícula Não Vinculada", além de tabela relacionada para gestão de afastamentos (motivação por CID, licenças e saúde).
* Mapeamento da entidade transacional `capes.student.professional.profile` para captação da linha de base (*baseline*) profissional e de inserção no mercado do discente no momento do ingresso, contemplando dados da organização empregadora, setor, porte, cargo, faixa salarial (sob sigilo estatístico) e o termo de consentimento obrigatório para auditoria de impacto de egressos exigido pela CAPES.



* **`modulo_03_formacao_e_disciplinas.md`**
* Modelagem de catálogos e ementários em `op.subject` (Disciplina), adicionando código interno do PPG, bibliografias básicas, carga horária, créditos e indicador de obrigatoriedade.
* Mapeamento de turmas e ofertas em `op.batch` e `op.session`, contemplando ano acadêmico, período letivo, idioma veicular da oferta, bibliografia complementar e indicador de utilização de PHEA (ensino híbrido).


* **`modulo_04_trabalhos_conclusao.md`**
* Especificação de metadados transacionais em `capes.thesis`: data da defesa, título final aprovado exato, tipo de documento (Dissertação, Tese, Produto Tecnológico) e amarração ao *Handle* ou URL persistente do Repositório Institucional.
* Modelagem da comissão examinadora em `capes.thesis.committee`, regulando o papel na banca (Orientador, Avaliador Interno, Externo).


* **`modulo_05_projetos_pesquisa.md`**
* Estruturação de `capes.research.project` integrada ao módulo nativo Odoo Projects, adicionando natureza da pesquisa (Básica/Aplicada), tipo de projeto, situação e flags de cooperação interinstitucional.
* Mapeamento da equipe de pesquisa em `capes.project.member` implementando rigorosamente a Taxonomia CRediT (Conceitualização, Metodologia, Validação, Escrita) para tipificação de contribuições.


* **`modulo_06_producao_intelectual.md`**
* Modelagem do barramento de produções intelectuais em `capes.intellectual.production` mapeado para interoperabilidade com as tabelas de tipo de documento COAR.
* Estruturação de metadados de acesso (aberto, embargado, restrito) e campos para identificadores únicos globais (`uid_uri`) como DOI, Handle ou ISBN.



#### Diretório 04: Processos da Vida Acadêmica

* **`01_editais_de_admissao.md`**
* Substituição do modelo linear nativo de admissão do OpenEduCat pelo modelo parametrizável de editais `op.admission.edital`.
* Arquitetura de tabelas relacionais One2many para `op.edital.phase` gerenciando fases dinâmicas configuráveis (análise de currículo Lattes, provas escritas, entrevistas ranqueadas e validação de proficiência em inglês por exames como TOEFL/IELTS).
* Regras lógicas para restringir inscrições automáticas de candidatos a vagas específicas segmentadas por linhas de pesquisa e orientadores cadastrados.


* **`02_matricula_de_acompanhamento.md`**
* Mecanismo algorítmico focado em solucionar a inatividade fictícia de alunos em fase exclusiva de pesquisa.
* Desenho do fluxo automatizado que consulta o livro-razão de créditos e força a inscrição compulsória semestral do discente em entidades de "Acompanhamento de Pesquisa" ou "Elaboração de Dissertação".


* **`03_motor_cronologico_e_trava_de_prazos.md`**
* Especificação de Ações Agendadas do Odoo (Cron Jobs) atuando como guardiões cronológicos dos limites temporais de titulação (prazos de mestrado e doutorado).
* Programação de regras de negócio em Python que bloqueiam o requerimento de trancamento de matrícula via Portal do Aluno caso o discente esteja no primeiro semestre, usufruindo de prorrogação ou sem anexo de atestado médico com CID.
* Fluxo de transição automática do estado do discente para `pending_dismissal` (Pendente de Desligamento/Jubilamento) em casos de abandono, estouro de prazos sem depósito ou dupla reprovação nos exames de qualificação.


* **`04_portal_e_requerimentos_self_service.md`**
* Modelagem da classe `op.academic.request` herdando o comportamento de rastreabilidade de mensagens e logs do componente `mail.thread` do Odoo.
* Desenho da máquina de estados para fluxos de aprovação multinível baseados na hierarquia da instituição (Aprovação do Orientador $\rightarrow$ Secretaria $\rightarrow$ Coordenador/Colegiado do PPG).



#### Diretório 05: Produtos Técnico-Tecnológicos (PTT)

* **`01_taxonomia_eixos_e_tipos.md`**
* Documentação das tabelas de classificação estática pré-populadas via XML de dados (`capes.ptt.axis` e `capes.ptt.type`) que representam as diretrizes oficiais do Grupo de Trabalho de Produção Técnica (GTPT) da CAPES.
* Mapeamento exaustivo dos 4 grandes eixos estruturantes (Produtos e Processos, Formação, Divulgação, Serviços Técnicos) e das 21 tipologias oficiais homologadas pelo CTC-ES (de T01 a T21, como T13-Patente e T19-Software).


* **`02_qualis_tecnologico_e_workflow.md`**
* Especificação da classe transacional central `capes.ptt.product`, mapeando autoria principal (discente), orientação, coautores (`res.users`), níveis de Maturidade Tecnológica (escala TRL de 1 a 9) e campo de justificativa de aderência.
* Modelagem da ficha de avaliação `capes.ptt.evaluation` para simulação do "Qualis Tecnológico", estabelecendo a verificação do campo booleano `is_adherent` como fator eliminatório rigoroso.


* **`03_calculo_de_estratos_e_bi.md`**
* Especificação lógica do método Python estruturado sob o decorador `@api.depends` para processar em tempo real as notas das quatro dimensões ponderadas (Demanda e Impacto, Inovação, Abrangência e Complexidade).
* Definição de regras de estratificação em intervalos rígidos de pontuação: T1 (90-100 pontos) a T5 (30-44 pontos), cravando automaticamente o status `TNC` (Produto Não Classificado) se a pontuação for insuficiente ou se houver glosa por falta de aderência.
* Arquitetura de design de interface (UI/UX) detalhando as visualizações Kanban de fluxo, Pivot de cruzamento (TRL vs Inovação) e Graph de densidade de estratos para inteligência gerencial.



#### Diretório 06: Titulação e Conformidade Documental

* **`01_rito_bipartido_e_bancas.md`**
* Modelagem do fluxo de validação acadêmica dividido rigidamente entre duas etapas obrigatórias: Exame de Qualificação e Defesa Final.
* Regras de verificação automatizadas que desativam permissões de agendamento de bancas se o motor de regras detectar pendências de créditos ou proficiências linguísticas pendentes.
* Programação das rotinas em Python para validação automática de comissões julgadoras, aplicando restrições de impedimento (vedação de orientador e coorientador atuarem simultaneamente como votantes) e checagem de afiliações (`is_internal`) para garantir proporção de membros externos.
* Regras de exceção para Mestrados Profissionais que autorizam a inclusão de especialistas e técnicos de mercado sem o título de Doutor na comissão avaliadora.


* **`02_historico_escolar_consolidado.md`**
* Desenho arquitetural do relatório final unificado em nível *Stricto Sensu* utilizando o sistema nativo de relatórios QWeb do Odoo para a classe `op.student.transcript.br`.
* Especificação lógica do algoritmo de cruzamento e consolidação de dados que realiza o *join* entre o livro-razão imutável de créditos, dados do ementário cumprido, versão do regimento vigente, título exato homologado da tese e nomes da comissão examinadora.


* **`03_diploma_digital_nato_digital.md`**
* Arquitetura do motor de conformidade e integração tecnológica adequado às exigências da Portaria MEC nº 70/2025 para emissão exclusivamente em formato Nato-Digital.
* Fluxo de geração em lote de arquivos estruturados: XML do Diploma Digital e XML da Documentação Acadêmica (Histórico Digital).
* Orquestração de bibliotecas Python de criptografia para aplicação de assinatura eletrônica avançada no padrão XAdES (ICP-Brasil, Certificado A3) e injeção automatizada de Carimbo de Tempo (*Timestamp*).
* Especificação de renderização da Representação Visual do Diploma Digital (RVDD) em formato PDF, com inclusão de chaves públicas de validação e código QR para controle de inalterabilidade externa.



#### Diretório 07: Padrões de Interoperabilidade Externa

* **`01_apis_rest_json_fonte_prata.md`**
* Especificação técnica das rotas públicas seguras `/api/v1/capes/` expostas pelo OpenEduCat para fornecer objetos JSON leves para a malha de robôs coletores governamentais da Sucupira.
* Configuração do protocolo de segurança OAuth 2.0 e geração de tokens de acesso de longa duração (*Bearer Tokens*) segregados em nível de aplicação.
* Diretrizes de conformidade jurídica com a LGPD (*privacy by design*), detalhando rotinas de criptografia em trânsito via túneis TLS 1.2 e minimização de dados sensíveis expostos nos payloads.


* **`02_gopg_coleta_e_crosswalk_dspace.md`**
* Roteiro de parametrização e injeção do arquivo de transformação sintática (planilha de conversão baseada em XSL/XSLT) rodando nas camadas internas de indexação Solr/Tomcat do repositório DSpace.
* Definição e isolamento do contexto e prefixo de metadados exclusivo denominado `oai_capes` sobre o protocolo OAI-PMH básico (Dublin Core), mitigando riscos de corrupção ou conflito de esquemas entre diferentes versões de software open-source (DSpace 6 vs DSpace 7/8).
* Mapeamento matricial relacional ("de / para") validando chaves semânticas obrigatórias como o código indexador CAPES do curso, identificadores persistentes de objetos (DOI), chaves de desambiguação humana (ORCiD) e identificadores institucionais globais (ROR).

#### Diretório 08: Macroprocessos

* **`macro-processos.md`**
* Detalhamento dos 10 macroprocessos acadêmicos que compõem o back-office do ERP Educacional OpenEduCat CAPES.

#### Diretório 09: Detalhamento de Validação Técnica do mp01_detalhamento_validacao_mptrcs

* **`mp01_detalhamento_validacao_mptrcs.md`**: (Governança Regimental e Setup Curricular - MP1)
* **`mp02_detalhamento_validacao_mptrcs.md`**: (Admissão, Seleção, Proficiência e Plano de Trabalho - MP2)
* **`mp03_detalhamento_validacao_mptrcs.md`**: (Vida Estudantil, Matrículas e Livro-Razão - MP3)
* **`mp04_detalhamento_validacao_mptrcs.md`**: (Requerimentos, Vigilância Cronológica e Jubilamento - MP4)
* **`mp05_detalhamento_validacao_mptrcs.md`**: (Gestão de PTTs e Qualis Tecnológico - MP5)
* **`mp06_detalhamento_validacao_mptrcs.md`**:  (Ritos de Titulação, Bancas e Defesas - MP6)
* **`mp07_detalhamento_validacao_mptrcs.md`**: (Expedição Documental e Diploma Digital / Integração USP - MP7)
* **`mp08_detalhamento_validacao_mptrcs.md`**: (Interoperabilidade GoPG, APIs REST e DSpace - MP8)
* **`mp09_detalhamento_validacao_mptrcs.md`**: (Gestão Docente e Timeline de Credenciamento - MP9)
* **`mp10_detalhamento_validacao_mptrcs.md`**: (Governança CPG e Atas QWeb com Clique Auditável - MP10)

---

### Diretrizes de Engenharia de Escrita para o Time

Ao redigir os arquivos acima especificados, o arquiteto deve assegurar que:

1. **Nenhum trecho de código fique solto:** Toda regra em Python ou tag XML de visualização deve estar encapsulada em uma explicação sobre a regra de negócio acadêmica ou regulamentação da CAPES/MEC que ela operacionaliza.
2. **Abordagem pragmática de dados:** Tratar os metadados e PIDs descritos nos arquivos do dicionário DAV como constantes e chaves de validação duras (restrições no banco de dados) e não como textos descritivos opcionais.
