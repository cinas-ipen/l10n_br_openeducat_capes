# Manual Operacional do Usuário: Corpo Docente e Orientadores
## Ecossistema l10n_br_openeducat_capes (Odoo 19.0)

Este manual é destinado aos professores, pesquisadores e orientadores credenciados perante os Programas de Pós-Graduação, orientando suas atividades didáticas e de orientação científica.

---

## 1. Perfil de Acesso e Portal Docente

* **Grupo de Segurança:** `openeducat_core.group_op_faculty` (Corpo Docente)
* **Usuário Padrão de Homologação/Treinamento:** `professor` / Senha: `professor123`
* **Acesso:** Interface web do Odoo ou Portal do Professor (`/my`).
* **Visão 360° do Docente:** Ao acessar sua ficha em **OpenEduCat $ightarrow$ Professores**, visualize nos smart buttons do topo:
  * **Orientandos Ativos:** Alunos regulares sob sua orientação direta em curso.
  * **Orientandos Titulados:** Egressos que defenderam dissertação ou tese sob sua orientação.
  * **Disciplinas Lecionadas:** Turmas sob sua regência pedagógica.
  * **Linhas de Pesquisa:** Linhas do programa às quais seu perfil está associado.
  * **Bancas Examinadoras:** Participações como presidente ou avaliador em comissões julgadoras.
* **PIDs Biográficos Obrigatórios:** No primeiro acesso, certifique-se de que seu cadastro em **Meu Perfil** contenha:
  * **CPF** (11 dígitos, validação Módulo 11).
  * **ORCiD ID** (no padrão `0000-0000-0000-0000`).
  * **Currículo Lattes** (Link canônico ou ID Lattes de 16 dígitos).

---

## 2. Gestão Didática das Disciplinas

### 2.1. Diário de Classe e Frequência
1. Acesse **Portal Docente $ightarrow$ Minhas Disciplinas**.
2. Selecione a turma ativa no período letivo:
   * **Plano de Ensino:** Cadastre a ementa, bibliografia básica e complementar, e cronograma das aulas.
   * **Frequência e Presença:** Registre os lançamentos de presença por aula ministrada.

### 2.2. Lançamento de Notas e Conceitos Finais
1. Ao término do semestre letivo, acesse a aba **Avaliações & Notas**.
2. Lance as notas numéricas ou conceitos regimentais (ex: `A`, `B`, `C` - Aprovado; `D`, `R` - Reprovado).
3. Clique em **Consolidar e Enviar para a Secretaria**:
   * O sistema realiza a validação de consistência e grava os lançamentos definitivos no Livro-Razão Acadêmico do discente.
   * *Atenção:* Uma vez consolidado, qualquer alteração posterior exige processo formal de retificação de notas homologado pela CPG.

### 2.3. Anuência para Alunos Especiais e Matrículas Intra-IES
* Se a sua disciplina estiver configurada com a exigência de consentimento prévio do docente (`special_student_instructor_consent_required = True`):
  1. Você receberá uma notificação no sistema informando a solicitação de vaga formulada por aluno especial ou aluno de outro programa da IES.
  2. Acesse **Minhas Disciplinas $ightarrow$ Solicitações de Inscrição**.
  3. Clique em **Conceder Anuência** ou **Recusar Justificadamente**.

---

## 3. Gestão da Orientação Discente

### 3.1. Acompanhamento do Plano de Trabalho Discente
1. Acesse **Ensino CAPES $ightarrow$ Meus Orientandos**.
2. Ao receber a submissão do Plano de Trabalho Discente (`op.student.work_plan`):
   * Analise o cronograma de atividades, aderência à linha de pesquisa do PPG e orçamento.
   * Verifique as pendências éticas: se a pesquisa envolver seres humanos ou animais, marque a necessidade de submissão ao **CEP** (Plataforma Brasil) ou **CEUA**.
   * Emita o parecer e clique em **Aprovar Plano de Trabalho**.

### 3.2. Parecer de Aproveitamento de Créditos Especiais
1. Quando seu orientando solicita a incorporação de disciplinas cursadas como Aluno Especial:
   * Você receberá o processo com status `submitted`.
   * Acesse **Meus Orientandos $ightarrow$ Requerimentos de Créditos**.
   * Avalie se a disciplina cursada possui mérito científico, aderência à dissertação/tese e se foi concluída há **menos de 36 meses**.
   * Emita o parecer fundamentado e clique em **Aprovar como Orientador** (`action_advisor_approve`). O processo é então encaminhado à CPG.

### 3.3. Solicitação de Prorrogação de Prazo de Defesa
1. Caso o orientando necessite de prazo adicional para concluir a pesquisa:
   * Acesse o prontuário do orientando e clique em **Solicitar Prorrogação de Prazo**.
   * Indique o número de dias solicitados (respeitando o limite regimental do curso, ex: 90 dias no MPTRCS).
   * Anexe o relatório de qualificação e cronograma detalhado de finalização.
   * Encaminhe para julgamento da CPG.

---

## 4. Projetos de Pesquisa e Taxonomia CRediT

1. Acesse **Pesquisa $ightarrow$ Projetos de Pesquisa** (`capes.research.project`).
2. Vincule seu orientando ao projeto de pesquisa correspondente.
3. Para cada membro da equipe, atribua a contribuição científica segundo a taxonomia internacional **CRediT** (14 papéis: Conceitualização, Metodologia, Software, Validação, Investigação, Redação original, etc.). Essa informação é coletada diretamente pela CAPES na avaliação quadrienal.

---

## 5. Cadastramento de Produtos Técnico-Tecnológicos (PTT)

1. Acesse **Produção Intelectual $ightarrow$ Cadastrar PTT** (`capes.ptt.product`).
2. Indique o Trabalho Final / Discente associado ao produto.
3. Preencha a classificação metodológica nos **4 Eixos** e selecione uma das **21 Tipologias** da CAPES.
4. Indique o nível de maturidade tecnológica (**TRL 1 a 9**, campos `trl_1` a `trl_9`).
5. O sistema simula o estrato Qualis (`final_stratum`: `T1` a `T5`) para conferência antes da submissão à Coordenação.
