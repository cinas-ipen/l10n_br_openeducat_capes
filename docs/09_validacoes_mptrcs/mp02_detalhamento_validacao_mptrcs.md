# **Documento de Validação Técnica e Funcional: Macroprocesso 02 (MP2)**

## **Admissão, Seleção, Proficiência, Matrícula e Plano de Trabalho Discente**

### **1. Finalidade do Macroprocesso 02 (MP2)**

O Macroprocesso 02 (MP2) rege a porta de entrada e a consolidação do vínculo discente no ecossistema OpenEduCat CAPES BR (l10n_br_openeducat_capes_admission).

Ao contrário de sistemas educacionais comerciais privados (que adotam inscrição direta e *rolling admission*), a pós-graduação *Stricto Sensu* pública e comunitária no Brasil exige estrito cumprimento aos princípios da **impessoalidade, isonomia, publicidade e transparência**, materializados na figura jurídica do **Edital de Seleção Pública**.

Sua finalidade principal abrange:

* **Governança do Certame Público:** Garantir a rastreabilidade total das inscrições, notas por fase, aplicação de ações afirmativas (cotas) e homologação do resultado final.
* **Auditabilidade e Segurança do Ingresso:** Assegurar que nenhum candidato seja convertido em aluno regular sem o cumprimento dos requisitos de entrada (diploma de graduação, PIDs universais e proficiência linguística, quando exigida no ingresso).
* **Desbloqueio Estruturado da Carreira Acadêmica:** Conectar a conversão da matrícula à formalização da orientação e à aprovação do **Plano de Trabalho Discente**, estabelecendo a linha de base científica da pesquisa e as travas éticas de Comitê de Ética em Pesquisa (CEP/CEUA).

### **2. A Arquitetura de Admissão e o Fluxo do Plano de Trabalho**

A inteligência de seleção e ingresso é articulada por duas entidades transacionais centrais: o **Edital de Seleção (op.admission.edital)** e o **Plano de Trabalho Discente (op.student.work_plan)**.

```text
+-------------------------------------------------------------------------+
|                         EDITAL DE SELEÇÃO                               |
|                       op.admission.edital                               |
|  - Período e Taxas                 - Vagas Globais / p/ Linha/Orientador|
|  - Versão Curricular Vinculada     - Percentual de Ações Afirmativas    |
+-------------------------------------------------------------------------+
                                 │ 1
                                 │ N (One2many)
                                 ▼
+-------------------------------------------------------------------------+
|                        FASES DE SELEÇÃO DINÂMICAS                       |
|                          op.edital.phase                                |
|  - Fase 1: Análise Documental      - Fase 3: Entrevista e Rubrica CPG   |
|  - Fase 2: Provas / Lattes         - Botão de Soberania (is_override)   |
+-------------------------------------------------------------------------+
                                 │
                                 │ (Aprovação e Conversão)
                                 ▼
+-------------------------------------------------------------------------+
|                         PERFIL DO DISCENTE                              |
|                             op.student                                  |
|  - Data de Início do Relógio       - Status de Proficiência Linguística |
|  - Vínculo com Turma (Cohort)      - Orientador e Coorientador          |
+-------------------------------------------------------------------------+
                                 │ 1
                                 │ 1 (One2one)
                                 ▼
+-------------------------------------------------------------------------+
|                      PLANO DE TRABALHO DISCENTE                         |
|                        op.student.work_plan                             |
|  - Título, Resumo e Linha          - OK Eletrônico do Orientador        |
|  - Previsão de Tipologia PTT       - Parecerista CPG + Trava CEP/CEUA   |
+-------------------------------------------------------------------------+
```

### **3. Detalhamento dos 7 Subprocessos do Macroprocesso 02**

Abaixo, cada um dos 7 subprocessos do MP2 é detalhado considerando a **Lógica de Workflow**, a **Configuração para o MPTRCS/IPEN (Stakeholders Principais)** e a **Matriz de Parametrização para Outras IES/PPGs**.

#### **Subprocesso 2.1: Parametrização do Certame, Vagas e Gestão de Turmas (Cohorts)**

* **Descrição Operacional:** A Secretaria Acadêmica cadastra o edital no ERP (op.admission.edital), estabelece o cronograma de inscrições, publica os critérios e associa obrigatoriamente o certame à versão vigente do regimento (curriculum_version_id). O edital cria a entidade de agrupamento "Turma" (*Cohort*), que atua como âncora cronológica para todos os ingressantes daquele ciclo.
* **Configuração Específica MPTRCS/IPEN:** 
  * *Nome do Edital:* "Edital de Seleção MPTRCS 2026/1". 
  * *Vinculação Regimental:* "Regulamento MPTRCS 2020 (Revisado CTA)". 
  * *Ações Afirmativas:* Reserva obrigatória de **20% das vagas** para candidatos autodeclarados pretos, pardos, indígenas ou pessoas com deficiência (PcD). 
  * *Distribuição de Vagas:* Oferta em caráter **global para o programa**, sem alocação/fracionamento prévio de cotas de vagas por orientador no momento da publicação do certame. 
  * *Edital de Vagas Remanescentes:* Suporta duplicação das regras caso haja ociosidade. Os aprovados no certame remanescente são vinculados à mesma "Turma" original, equalizando os prazos de titulação. 
* **Matriz de Parametrização no ERP:** Permite parametrização livre de cotas (ex: 0% a 50%), editais por fluxo contínuo ou por oferta semestral/anual fechada, e controle de vagas **globais do programa (modelo MPTRCS)** ou **fracionadas por Linha de Pesquisa / Orientador** (op.faculty), caso outro PPG prefira.

#### **Subprocesso 2.2: Captação e Triagem Documental (Portal do Candidato)**

* **Descrição Operacional:** O candidato realiza o auto-cadastro no Portal de Admissão, preenche a ficha biográfica e faz upload dos documentos probatórios em PDF. 
* **Configuração Específica MPTRCS/IPEN:** 
  * *Exigência de PIDs:* Preenchimento obrigatório da URL do Currículo Lattes e do número do ORCID (com validação de formato). 
  * *Documentação Probatória:* Upload do Diploma de Graduação (ou Atestado de Conclusão), Histórico Escolar da Graduação, Documentos Civis e Foto 3x4. 
  * *Documentação Técnica:* Submissão da Proposta de Pré-Projeto de Pesquisa (indicando Área de Concentração, Linha de Pesquisa pretendida e sugestão de Orientador), juntamente com o Termo de Compromisso assinado atestando disponibilidade de carga horária presencial. 
  * *Proficiência:* Upload do Certificado de Proficiência em Língua Inglesa (e Português para candidatos estrangeiros). 
* **Matriz de Parametrização no ERP:** Permite configurar a lista de documentos obrigatórios e facultativos por edital, incluindo checklists específicos para estrangeiros ou optantes de cotas.

#### **Subprocesso 2.3: Workflow de Avaliação Seletiva, Rubricas e Botão de Override**

* **Descrição Operacional:** O certame executa as fases de seleção configuradas na tabela op.edital.phase. As notas são lançadas no sistema e consolidam uma pontuação ponderada final para ranqueamento classificatório e eliminatório.  
* **Configuração Específica MPTRCS/IPEN:** 
  * *Fase 1 - Homologação Documental:* Verificação e deferimento dos anexos e da proficiência pela Secretaria Acadêmica. 
  * *Fase 2 - Análise de Currículo Lattes e Prova:* Computação objetiva da planilha de pontuação do Lattes e lançamento de nota da prova escrita de conhecimentos. 
  * *Fase 3 - Entrevista Qualitativa com a CPG:* Painel no ERP (Rubrica de Avaliação) no qual os examinadores atribuem nota de 1 a 5 em três dimensões: 
    1. *Maturidade Profissional.* 
    2. *Alinhamento com o Setor Produtivo e Linha de Pesquisa.* 
    3. *Potencial de Geração do Produto Técnico-Tecnológico (PTT).* 
  * *Gatilho de Soberania do Coordenador (is_override):* Em situações excepcionais de relevante interesse tecnológico/acadêmico, o Coordenador do Programa possui a prerrogativa de acionar o botão "Aprovação em Caráter Excepcional (Override)". O ERP altera a flag is_override = True, exige o preenchimento da justificativa técnica em campo de texto livre e grava o selo de auditoria com ID do usuário, timestamp e IP. 
* **Matriz de Parametrização no ERP:** Quantidade de fases totalmente configurável (1 a N fases), com pesos percentuais customizáveis, notas de corte por fase e fórmulas de médias ponderadas.

#### **Subprocesso 2.4: Conversão em Aluno Regular, Trava de Proficiência e Evasão Precoce**

* **Descrição Operacional:** Com a publicação da lista final de aprovados, a Secretaria aciona o comando de conversão de candidato em aluno regular (op.student). O Odoo valida os pré-requisitos de entrada, gera o registro cadastral, atribui o número de matrícula e inicia o relógio cronológico oficial. 
* **Configuração Específica MPTRCS/IPEN:** 
  * *Trava Dura de Proficiência na Matrícula (proficiency_stage = 'admission'):* Por se tratar da regra IPEN/USP, o Odoo bloqueia a geração da matrícula caso o comprovante de proficiência em Inglês (e Português para estrangeiros) não esteja deferido no dossiê. 
  * *Início do Relógio:* A efetivação da matrícula marca o dia 0 e inicia a contagem improrrogável dos **24 meses** de prazo máximo de titulação. 
  * *Gatilho de Evasão Precoce:* O ERP monitora a assiduidade nas **3 primeiras semanas letivas**. Ingressantes sem registro de presença ou sem justificativa formal homologada no portal têm a matrícula cancelada automaticamente como "Desistente", notificando a Secretaria para convocação imediata do próximo candidato da lista de espera.  
* **Matriz de Parametrização no ERP:** 
  * *Gatilho de Proficiência:* 'admission' (IPEN/USP), 'qualification' (Mackenzie) ou 'defense'. 
  * *Janela de Evasão Precoce:* Ajustável (ex: 1 a 4 semanas) ou desativável.

#### **Subprocesso 2.5: Formalização Eletrônica do Vínculo de Orientação**

* **Descrição Operacional:** Formaliza a associação acadêmica entre o discente e seu orientador (e coorientador, quando houver), garantindo que a responsabilidade pela condução da pesquisa esteja atribuída perante os órgãos de ensino e a CAPES. 
* **Configuração Específica MPTRCS/IPEN:** 
  * *Prazo Limite de Formalização:* Até o **3º mês letivo** de ingresso. 
  * *Workflow no Portal:* 
    1. O estudante acessa o Portal do Aluno e solicita o vínculo selecionando o docente credenciado. 
    2. O Orientador recebe a notificação no painel do ERP e emite o aceite eletrônico ("Aceitar Orientação"). 
    3. A Secretaria Acadêmica efetua a triagem final, auditando se o docente respeita o teto de orientação do programa (**máximo de 8 orientandos ativos no IPEN**, conforme diretrizes do Comitê Medicinas II da CAPES), e homologa o vínculo. 
* **Matriz de Parametrização no ERP:** Teto de orientandos por docente ajustável por regimento (ex: 6, 8 ou 10 alunos), com suporte a coorientação nacional ou internacional (cotutela).

#### **Subprocesso 2.6: Submissão, Workflow de Avaliação e CEP do Plano de Trabalho (op.student.work_plan)**

* **Descrição Operacional:** Estabelece a proposta formal do projeto de pesquisa, o cronograma de execução e a previsão da tipologia do Produto Técnico-Tecnológico (PTT). A evolução acadêmica do aluno e a liberação de bancas intermediárias ficam estritamente condicionadas à homologação deste plano. 
* **Workflow Operacional Passo a Passo:**

```text
[Discente: Preenche Metadados + Anexa PDF no Portal]
                           │
                           ▼ 
[Orientador Principal: Revisão e OK Eletrônico] ──(Inadequado)──► [Devolvido ao Aluno]
                           │
                           ▼
[Secretaria Acadêmica: Triagem (ready_for_agenda)]
                           │
                           ▼ 
[Pauta da Reunião CPG: Designação do Parecerista / Avaliador]
                           |
                           ▼
[Avaliador: Emite Parecer Eletrônico no ERP]
                           │
            ┌──────────────┼───────────────┐
            │              │               │
            ▼              ▼               ▼ 
   [a) Aprovado]     [b) Aprovado c/]   [c) Pendência] ──► [Upload Parecer CEP]
         │             [Revisões]         [  CEP/CEUA ]              │
         │                 │                 │                       │
         │           [Ajustes + OK]          └─────────┬─────────────┘
         │           [ Orientador ]                    │
         │                 │                           │
         └─────────────────┴──────────┬────────────────┘
                                      │ 
                                      ▼ 
                         [d) Reprovado s/ Direito] ──► [Desligamento / Novo Plano]
                                      │
                                      ▼
                      [Homologação Final em Ata CPG]
                                      │ 
                                      ▼
                    [Chave de Desbloqueio da Carreira]
```

* **As 4 Categorias de Parecer do Avaliador:** 
  1. **a) Aprovado:** Plano satisfatório, liberado diretamente para homologação da CPG. 
  2. **b) Aprovado com Revisões:** Exige ajustes no texto ou cronograma. O aluno realiza as correções, o orientador emite novo OK e o avaliador faz a checagem final. 
  3. **c) Aprovado com Pendência de CEP:** O plano técnico é correto, mas envolve seres humanos, animais ou biossegurança/radioproteção. O Odoo atribui o status **"Aprovado Condicional"** e **bloqueia o agendamento de bancas de qualificação/seminários** até que o discente anexe o Parecer Consubstanciado do CEP/CEUA aprovado. 
  4. **d) Reprovado sem Direito a Revisão:** Inviabilidade técnica ou falta de aderência grave. Encaminhado à CPG para deliberação sobre concessão de prazo extraordinário para novo tema ou desligamento. 
* **Homologação:** O plano atinge o estado homologated após a chancela formal na Ata de Reunião da CPG (op.cpg.meeting), atuando como chave de desbloqueio para a carreira acadêmica.

#### **Subprocesso 2.7: Admissão de Alunos Especiais (Disciplinas Isoladas)**

* **Descrição Operacional:** Gerencia o fluxo de admissão para candidatos interessados em cursar disciplinas avulsas sem vínculo regular de pós-graduação. 
* **Configuração Específica MPTRCS/IPEN:** 
  * *Teto de Créditos:* O ERP limita a inscrição a no máximo **8 unidades de crédito** em disciplinas isoladas. 
  * *Restrição de Direitos:* Alunos especiais não possuem orientador, não submetem plano de trabalho e não recebem status de aluno regular. Ao final do período, o sistema emite apenas uma Certidão / Declaração de Aproveitamento de Estudos. 
* **Matriz de Parametrização no ERP:** Teto de créditos avulsos parametrizável por programa (ex: 8, 12 ou 16 créditos) e regra de aproveitamento futuro em caso de aprovação posterior no processo seletivo regular.

### **4. Tabela de Parametrização para Validação com Stakeholders (MPTRCS)**

A tabela abaixo deve ser revisada e formalmente chancelada durante a reunião de trabalho do MP2 com a Coordenação, Comissão de Pós-Graduação (CPG) e Secretaria do MPTRCS/IPEN:

| Item de Admissão / Parâmetro | Campo Técnico no Odoo | Configuração Padrão MPTRCS (IPEN) | Outras Opções Suportadas pelo ERP |
| :---- | :---- | :---- | :---- |
| **Distribuição de Vagas** | `edital_quota_mode` | **Vagas Globais do Programa** | Fracionadas por Linha ou por Docente |
| **Gatilho de Proficiência** | `proficiency_stage` | 'admission' (Exigido na Entrada) | 'qualification' ou 'defense' |
| **Reserva de Ações Afirmativas** | `affirmative_action_percent` | **20% das vagas** (Cotista / PcD) | Parametrizável (0% a 50%) |
| **Mínimo de Créditos no 1º Semestre** | `min_first_semester_credits` | **24 Créditos** (Calouros MPTRCS) | Parametrizável conforme a carga do PPG |
| **Aprovação Excepcional (Override)** | `is_override` / `override_justif` | **Habilitado** (Atuação do Coordenador) | Ativado / Desativado por perfil de acesso |
| **Janela de Evasão Precoce** | `early_dropout_weeks` | **3 Semanas** (Assiduidade Inicial) | Parametrizável (ex: 1 a 4 semanas) |
| **Prazo Limite de Orientação** | `max_months_advisor_link` | **3º Mês Letivo** | Configurável (ex: 1º ao 6º mês) |
| **Teto de Orientandos por Docente** | `max_active_advisees` | **8 Alunos Ativos** (Medicina II) | Configurable por área de avaliação CAPES |
| **Trava Ética no Plano de Trabalho** | `cep_required_gate` | **Habilitado** (Bloqueia Bancas s/ CEP) | Ativado / Desativado |
| **Teto de Créditos Aluno Especial** | `max_special_student_credits` | **8 Créditos** | Configurable (ex: 8, 12 ou 16 créditos) |
| **Declaração de Perfil (Baseline)** | `capes.student.professional.profile` | **Obrigatório no Ingresso** (Monitoramento CAPES) | Ativado por padrão para Programas Profissionais |

### **5. Roteiro Prático para a Reunião de Validação (Checklist CPG-MP)**

Para conduzir a pauta de homologação do Macroprocesso 02 com a CPG e a Secretaria do MPTRCS, recomenda-se deliberar sobre os seguintes quatro pontos de confirmação:

1. **Confirmar Oferta de Vagas Globais e Trava de Proficiência na Entrada:** 
   * Ratificar a oferta de vagas globais sem reserva por orientador e a manutenção do parâmetro proficiency_stage = 'admission'. 
2. **Aprovação das Fases de Seleção e Rubrica de Entrevista:** 
   * Validar as 3 fases do certame (Documental, Prova/Lattes, e Entrevista com notas de 1 a 5 para Maturidade, Alinhamento e Potencial de PTT) e o mecanismo de auditabilidade do botão de Override da Coordenação. 
3. **Chancela da Regra de Evasão Precoce e Vínculo de Orientação:** 
   * Confirmar o cancelamento automático da matrícula por ausência injustificada nas 3 primeiras semanas e o limite até o 3º mês para formalização eletrônica da orientação no portal. 
4. **Homologação do Workflow do Plano de Trabalho Discente:** 
   * Validar o fluxo de tramitação do Plano de Trabalho (Discente → OK Orientador → Triagem Secretaria → Parecerista CPG → Homologação em Ata), incluindo as 4 categorias de parecer e a trava de bloqueio de bancas para projetos com pendência no CEP/CEUA.
