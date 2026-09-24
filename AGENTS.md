# AGENTS.md — Diretrizes Técnicas para Agentes de IA (`l10n_br_openeducat_capes`)

Este documento estabelece as regras arquiteturais, padrões de código e convenções obrigatórias para o desenvolvimento assistido por IA no ecossistema `l10n_br_openeducat_capes`, construído sobre o **Odoo 19.0** e o **OpenEduCat 19.0**.

---

## 1. Stack Tecnológica e Requisitos de Ambiente
* **Framework Base:** Odoo 19.0 (Enterprise / Community) + OpenEduCat 19.0.
* **Linguagem:** Python 3.11+.
* **Banco de Dados:** PostgreSQL 16+ (com extensões `unaccent` e `pg_trgm`).
* **Paradigmas:** Domain-Driven Design (DDD), Programação Orientada a Aspectos via ORM, e Arquitetura *Append-Only* para livros-razão acadêmicos.

---

## 2. Topologia do Monorepo e Dependências

O projeto é dividido em 9 submódulos isolados. Ao criar ou modificar código em um submódulo, **nunca** quebre a árvore de dependências definida nos manifests (`__manifest__.py`):

1. `l10n_br_openeducat_capes_core` (Depende de: `openeducat_core`)
2. `l10n_br_openeducat_capes_academic` (Depende de: `l10n_br_openeducat_capes_core`, `mail`)
3. `l10n_br_openeducat_capes_admission` (Depende de: `l10n_br_openeducat_capes_core`, `l10n_br_openeducat_capes_academic`)
4. `l10n_br_openeducat_capes_research` (Depende de: `l10n_br_openeducat_capes_academic`, `project`)
5. `l10n_br_openeducat_capes_thesis` (Depende de: `l10n_br_openeducat_capes_academic`, `l10n_br_openeducat_capes_admission`, `l10n_br_openeducat_capes_research`)
6. `l10n_br_openeducat_capes_ptt` (Depende de: `l10n_br_openeducat_capes_core`, `l10n_br_openeducat_capes_academic`, `l10n_br_openeducat_capes_thesis`)
7. `l10n_br_openeducat_capes_diploma` (Depende de: `l10n_br_openeducat_capes_core`, `l10n_br_openeducat_capes_academic`, `l10n_br_openeducat_capes_thesis`)
8. `l10n_br_openeducat_capes_integration` (Depende de: `l10n_br_openeducat_capes_core`, `l10n_br_openeducat_capes_ptt`)
9. `l10n_br_openeducat_capes_scholarship` (Depende de: `l10n_br_openeducat_capes_core`, `l10n_br_openeducat_capes_academic`, `l10n_br_openeducat_capes_admission`, `mail`)

### 2.1. Módulos Nativos Estendidos e Impactados
* **OpenEduCat Base (`openeducat_core`):**
  * `op.student`: Estendido com RA institucional perene, CPF, PIDs, orientador, status CAPES, versionamento regimental, livro-razão de créditos e visão 360°.
  * `op.faculty`: Estendido com PIDs, regime de trabalho, titulação, áreas/linhas, vínculos interinstitucionais (`op.faculty.program.link`) e conformidade da Portaria CAPES 81/2016 (máx. 3 programas permanentes).
  * `op.subject`: Estendido com créditos sincronizados com `grade_weightage`, ementa, bibliografia básica/complementar, indicador PHEA, idioma e governança de alunos especiais.
  * `op.batch`: Estendido com associação direta ao programa de pós-graduação (`program_id`).
  * `op.student.course`: Estendido para multi-vínculo com tipo de curso (`course_type`), programa, versão curricular e datas de vigência.
* **Odoo Framework (`base`, `mail`, `project`):**
  * `res.company`: Estendido com PIDs institucionais (CNPJ, e-MEC, código CAPES, ROR, ISNI), georreferenciamento e dados da Pró-Reitoria.
  * `res.partner`: Estendido com censo biográfico e demográfico CAPES/DAV (CPF com Módulo 11, ORCiD, Lattes, raça/cor IBGE, PCD, nacionalidade, filiação materna).
  * `res.users`: Estendido com governança multiprograma (`allowed_program_ids`, `current_program_id`, `is_central_admin`, `action_switch_program`).
  * `ir.http`: Estendido para injetar contexto de programa ativo na sessão web (`session_info`).
  * `project.project`: Integrado com `capes.research.project` via campo `odoo_project_id`.
  * `mail.thread` e `mail.activity.mixin`: Herdados nos modelos transacionais para trilha de auditoria e mensageria.

---

## 3. Regras de Ouro de Arquitetura e Domínio

1. **Consulta Documental Obrigatória:** Antes de implementar qualquer modelo, view ou rota REST, o agente **deve** consultar os arquivos correspondentes na pasta `docs/` para compreender o contexto regulatório (GoPG, DAV, Portarias CAPES e MEC).
2. **Proibição Absoluta de Hardcode Regimental:** Nenhuma regra de prazo, quórum de banca, fator de crédito ou exigência de proficiência pode ser fixa em código Python (*hardcoded*). Todas as validações devem consultar dinamicamente a entidade de versionamento curricular (`op.curriculum.version`) associada ao discente (`curriculum_version_id`).
3. **Imutabilidade (Append-Only):** Tabelas de Livro-Razão (`op.student.credit.ledger` e `op.faculty.category.ledger`) operam estritamente em modo *append-only*. O agente **nunca** deve escrever métodos Python que permitam operações de exclusão (`unlink`) ou recálculo destrutivo nessas tabelas.
4. **Respeito ao Ato Jurídico Perfeito:** Atividades já consolidadas no histórico escolar sob a égide de um regimento anterior não devem ser recalculadas de forma retroativa por alterações em versões futuras do currículo.

---

## 4. Convenções de Código ORM (Odoo 19)

* **Estrutura de Diretórios do Submódulo:**
``` text
l10n_br_openeducat_capes_[modulo]/
├── __init__.py
├── __manifest__.py
├── data/           # Dados XML / CSV estáticos (ex: taxonomia PTT)
├── models/         # Classes Python herdando de models.Model
├── security/       # ir.model.access.csv e regras de acesso
├── views/          # Views XML (tree, form, search, kanban, pivot, graph)
└── controllers/    # Controladores HTTP / REST APIs (/api/capes/v1/)
```

* **Segurança Obrigatória:** Todo novo modelo criado em Python **deve** obrigatoriamente possuir sua linha correspondente de permissão no arquivo `security/ir.model.access.csv` do respectivo submódulo. O agente nunca deve gerar modelos sem controle de acesso.
* **Decoradores e Desempenho:** 
  * Utilize `@api.depends` estritamente com os campos afetados para campos computados.
  * Utilize `@api.constrains` para validações lógicas e bloqueios de workflow baseados em regras de negócio.
* **Herança Segura:** Utilize prioritariamente `_inherit` para estender classes nativas do Odoo ou do OpenEduCat sem corromper as tabelas originais do banco de dados relacional.

---

## 5. Instruções de Execução para o Agente

Quando solicitado a implementar uma funcionalidade:
1. **Planeje em etapas:** Identifique qual submódulo do monorepo receberá a alteração.
2. **Verifique os Manifests:** Confirme se o `__manifest__.py` possui todas as dependências necessárias para a nova classe.
3. **Escreva o Código Limpo:** Produza os arquivos Python e XML seguindo os padrões do Odoo 19.
4. **Valide a Sintaxe:** Certifique-se de que não há erros de indentação, falta de importações ou chamadas a métodos depreciados.
