# **Validação Técnica MP5 - Gestão de PTTs (Mestrados Profissionais)**

## **1. Introdução e Finalidade**

O **Macroprocesso 05** é exclusivo para os Programas de Pós-Graduação Profissionais, sendo a espinha dorsal da titulação no MPTRCS/IPEN. Sua função é orquestrar todo o ciclo de vida do **Produto Técnico-Tecnológico (PTT)** — desde a sua proposição no Plano de Trabalho, passando pela validação de aderência, até a estratificação de qualidade (Qualis Tecnológico).

Para o MPTRCS, o PTT não é um item acessório, mas uma **condição estrutural de titulação**. O sistema foi desenhado para que a homologação do PTT atue como uma "chave de desbloqueio" sistêmica: sem a homologação do PTT, o ERP bloqueia automaticamente o rito de defesa final da dissertação.

## **2. Taxonomia Oficial e Eixos (GTPT / Medicina II)**

Para garantir a padronização e o sucesso na coleta da CAPES, o sistema proíbe a inserção manual de categorias de produtos. A ontologia é baseada no GTPT (*Grupo de Trabalho de Produção Técnica*) e nas subcategorias do Comitê Medicina II.

### **2.1. Os 4 Eixos Estruturantes (capes.ptt.axis)**

Toda produção deve ser obrigatoriamente vinculada a um eixo primário:

* **Eixo 1 (Produtos e Processos):** Inovação tangível (patentes, softwares, hardwares, metodologias clínicas e tecnologias sociais).  
* **Eixo 2 (Formação):** Impacto na capacitação (cursos de qualificação, materiais didáticos complexos, manuais).  
* **Eixo 3 (Divulgação e Difusão):** Democratização do conhecimento técnico (eventos, exposições, curadoria de dados).  
* **Eixo 4 (Serviços Técnicos):** Assessoria ao Estado/indústria, laudos nucleares, normas técnicas.

### **2.2. Tipologias Medicina II (Configuração MPTRCS/IPEN)**

O sistema está parametrizado com as 10 subcategorias de entrega críticas para o IPEN:

1. **Ativos de Propriedade Intelectual:** Patente ou Software (*Exige anexo de comprovante INPI*).  
2. **Artigo Científico em Periódico Indexado:** Web of Science / Scopus.  
3. **Empresa ou Organização Social Inovadora:** *Spin-offs* acadêmicas.  
4. **Curso de Formação Profissional:** Capacitação (presencial/EAD).  
5. **Norma ou Marco Regulatório:** Diretrizes CNEN/ANVISA.  
6. **Relatório Técnico Conclusivo:** Laudos de qualidade/pareceres.  
7. **Manual / Protocolo Clínico:** POP/Radioproteção.  
8. **Base de Dados Técnico-Científica:** Data lakes/imagens médicas.  
9. **Produto de Editoração:** Livros/Capítulos.  
10. **Processos e Materiais Não Patenteáveis:** Metodologias de calibração.

## **3. Workflow de Validação (O Motor de Regras)**

A forma como a CPG aprova o PTT é definida por parametrização na versão curricular. Para o MPTRCS, o sistema adota o **Workflow V1 (Checklist + CPG)**:

### **3.1. Workflow V1: Checklist + Homologação CPG (MPTRCS)**

Este fluxo é integrado à rotina de agendamento de defesa para garantir que o produto esteja pronto no momento do rito final:

1. **Indicação e Evidências:** No requerimento de agendamento de defesa, o aluno seleciona o PTT no checklist e anexa as evidências (ex: link para repositório, PDF do manual, comprovante de depósito).  
2. **Dupla Anuência:** O Orientador e o Coorientador (quando houver) validam o PTT no sistema. Sem este "ok" eletrônico, o workflow não avança.  
3. **Triagem:** A secretaria valida a conformidade técnica dos anexos e altera o status para ready_for_agenda (Apto para Pauta).  
4. **Pauta CPG:** O requerimento é incluído na pauta da reunião oficial da CPG (op.cpg.meeting).  
5. **Homologação:** O colegiado avalia se o PTT cumpre o regulamento do programa. A ata é gerada e aprovada com clique auditável.  
6. **Desbloqueio:** A homologação destrava o sistema para o agendamento da Defesa Pública.

## **4. O Motor de Estratificação (Qualis Tecnológico)**

Para limitar a subjetividade das bancas, o algoritmo do Odoo processa o baremo da CAPES através da classe capes.ptt.evaluation, que soma pontos (0 a 100) baseados em 4 dimensões:

* **Impacto e Demanda (30 pts):** Raio de impacto (Local, Regional, Nacional).  
* **Inovação e Originalidade (25 pts):** Cruza a novidade com o nível de maturidade (TRL - *Technology Readiness Level*).  
* **Aplicabilidade e Replicabilidade (25 pts):** Facilidade de adoção por terceiros.  
* **Complexidade (20 pts):** Infraestrutura e multidisciplinaridade.

O sistema classifica o produto de **T1 (mais elevado)** a **T5 (menor impacto)**, ou **TNC (Trabalho Não Conforme)** caso não atinja o mínimo.

## **5. Parâmetros e Flexibilidade (Para os Stakeholders)**

O sistema é 100% parametrizável via op.curriculum.version, permitindo que o MPTRCS mantenha suas regras e outros PPGs configurem as deles:

* **Modo de Validação:** A CPG pode escolher entre cpg_checklist (modelo atual do IPEN) ou qualis_prior (exige estrato atribuído antes da defesa).  
* **Obrigatoriedade:** Pode ser habilitado ou desabilitado via ptt_validation_mode.  
* **Trava Ética:** O sistema pode ser parametrizado para impedir qualquer defesa caso produtos envolvendo humanos/animais não tenham parecer do CEP.

## **6. Integração com o Histórico (Ato Jurídico Perfeito)**

Ao retornar do trancamento ou migrar de currículo, o sistema preserva o Ato Jurídico Perfeito dos créditos já conquistados via PTT/APO, garantindo que o discente não perca o patrimônio acadêmico já validado, mas respeite as normas vigentes para as etapas futuras, vedando o hibridismo normativo.

### **Resumo de Validação para Stakeholders (IPEN)**

| Funcionalidade | Configuração MPTRCS | Benefício / Regra de Ouro |
| :---- | :---- | :---- |
| **Workflow** | cpg_checklist | Validação integrada à defesa, sem câmara prévia externa. |
| **Obrigatoriedade** | Obrigatório para Defesa | Sem PTT homologado, não há banca. |
| **Créditos (APO)** | Injeção automática | Créditos bonificados no Livro-Razão após homologação. |
| **Responsáveis** | Orientador + Coorientador | Anuência eletrônica obrigatória para segurança do Orientador. |
| **Auditabilidade** | Clique Auditável | Todas as deliberações da CPG são rastreáveis por IP/User/Timestamp. |

*Este detalhamento técnico blinda o programa IPEN contra futuras auditorias, garantindo que cada "Produto" registrado seja, de fato, um resultado auditável da pesquisa realizada, com a chancela do colegiado registrada de forma indelével no sistema.*
