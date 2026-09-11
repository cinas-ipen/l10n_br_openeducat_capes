# Documento 01: Rito Bipartido, Marcos Intermediários e Validação de Bancas

## 1. A Exigência do Rito Bipartido e Flexibilidade Regimental

A pós-graduação *Stricto Sensu* no Brasil exige um rito de avaliação dividido formalmente em etapas intermediárias de acompanhamento da pesquisa e na avaliação final pública.

O submódulo `l10n_br_openeducat_capes_thesis` estende a máquina de estados nativa do OpenEduCat para suportar múltiplos cenários de parametrização por programa e nível de formação:

* **Programas com apenas Seminário de Área:** Casos como o Mestrado Profissional do IPEN (MPTRCS), onde a qualificação intermediária é cumprida na forma de Seminário de Área.
* **Programas com Exame de Qualificação Clássico:** Cursos que adotam bancas formais de qualificação sem vínculo direto a diário de disciplina.
* **Programas Híbridos (Qualificação + Seminário de Área):** Cursos como o Doutorado Acadêmico do IPEN, que exigem obrigatoriamente ambos os marcos ao longo do percurso.

---

## 2. Subprocesso 3.2: Marcos de Avaliação Intermediária

Os marcos intermediários servem para auditar o progresso da pesquisa (geralmente ao atingir cerca de 75% de execução do projeto) antes de liberar o discente para a fase de redação final e defesa.

### 2.1. Trava do Plano de Trabalho e Elegibilidade

O Odoo bloqueia categoricamente o agendamento de qualquer rito intermediário se o discente não possuir o seu **Plano de Trabalho (`op.student.work_plan`) devidamente homologado pela CPG**. Caso o plano tenha sido aprovado com pendência de Comitê de Ética em Pesquisa (CEP/CEUA), o agendamento permanece travado até a inserção do parecer consubstanciado de aprovação ética no sistema.

### 2.2. A Operacionalização do Seminário de Área como Disciplina

Quando o programa adota o Seminário de Área, o rito é gerido como uma disciplina curricular integrada no submódulo `l10n_br_openeducat_capes_academic`:

* **Alçada do Coordenador da Disciplina:** A aprovação da banca e a presidência da atividade cabem ao Coordenador da Disciplina de Seminário de Área (docente permanente credenciado).
* **Composição da Comissão Avaliadora:** A composição da comissão avaliadora do Seminário de Área segue o parametrizado em `op.curriculum.committee.rule` para o rito `seminar` (ex: 2 Doutores no Mestrado e 3 no Doutorado para o IPEN, ou conforme norma do PPG)


* **Registro de Notas e Créditos:** O resultado do Seminário de Área alimenta o diário eletrônico da disciplina, injetando automaticamente as notas/conceitos e os créditos correspondentes no Livro-Razão Acadêmico (`op.student.credit.ledger`).

### 2.3. Regras de Reprovação e Jubilamento Intermediário

* **1ª Reprovação:** O Odoo altera o status da disciplina/rito para "Reprovado", permitindo que o aluno realize uma única nova inscrição no período letivo imediatamente subsequente.
* **2ª Reprovação:** Ocorrendo duas reprovações no marco intermediário (Seminário de Área ou Exame de Qualificação), o sistema dispara o gatilho automático de desligamento, alterando o status do discente para `pending_dismissal` (Pendente de Desligamento) e interrompendo a exportação para a CAPES.

---

## 3. Rito Final: Defesa Pública de Dissertação ou Tese

A Defesa Final é o rito cartorial e acadêmico culminante do programa. O agendamento da banca exige o cumprimento estrito de pré-requisitos auditados pelo motor de regras do Odoo.

### 3.1. Antecedência e Travas Prévias de Agendamento

O pedido de agendamento da defesa deve ser submetido pelo orientador no Portal do Aluno com no mínimo **15 dias de antecedência** em relação à data da sessão. O Odoo executa uma varredura automática confirmando:

1. **Integralização Teórica e Disciplinas Obrigatórias:** Cumprimento da carga mínima de créditos e aprovação em **todas as disciplinas obrigatórias** configuradas em `op.curriculum.subject.rule` para a versão curricular do aluno, considerando tanto as disciplinas gerais do programa quanto as específicas da sua Área de Concentração (`area_id`).
2. **Proficiência Linguística:** O sistema checa o parâmetro `proficiency_stage` do regimento. Para o IPEN (`proficiency_stage = 'admission'`), essa checagem é automaticamente validada como cumprida por ser requisito de entrada.
3. **Integralização no Livro-Razão (Artigo 39º do Regulamento MP-TRCS):** Para o agendamento da Defesa Final, a engine valida no livro-razão (`op.student.credit.ledger`) se o aluno cumpriu o teto mínimo de créditos em disciplinas do programa (`min_subject_credits`, ex: 40 créditos no MP-TRCS) e o Seminário Geral (`other_mandatory_credits`, ex: 8 créditos).
4. **Validação do Produto Técnico-Tecnológico (PTT):** O Odoo verifica o parâmetro `ptt_validation_mode` do regimento do aluno:
   * *Modo `cpg_checklist` (MPTRCS / V1):* Confirmação de que o requerimento de defesa contendo a indicação do PTT possui o aceite do Orientador, do Coorientador (se houver) e a homologação formal aprovada em Ata de Reunião da CPG.
   * *Modo `qualis_prior`:* Confirmação de que existe PTT registrado no estado `homologated` com estrato Qualis atribuído.
   * *Modo `none`:* Etapa dispensada.
5. **Trava Ética (CEP):** Comprovação de aprovação no CEP/CEUA, se o plano de trabalho assim o exigiu.
6. **Estágio de Docência / Supervisionado (Portaria CAPES nº 221/2025):** Validação parametrizável baseada no campo `teaching_internship_mode` do regimento do aluno:
   * *Programas Profissionais ou `not_applicable`:* Trava automaticamente **desativada e dispensada**.
   * *Modo `scholarship_only`:* Exigido e verificado no Livro-Razão apenas se o discente for/foi bolsista de fomento acadêmico.
   * *Modo `flexible_equivalence`:* O Odoo aceita a aprovação registrada na disciplina de "Estágio de Docência" OU a comprovação averbada de "Estágio Supervisionado" / atividades equivalentes autorizadas pela CPG.

---

## 4. Composição da Comissão Julgadora, Impedimentos e Endogenia

A validade jurídica do título outorgado depende da estrita conformidade da comissão julgadora (`capes.thesis.committee`) com a tabela de regras do regimento do aluno (`op.curriculum.committee.rule`).

### 4.1. Configuração Paramétrica de Quórum e Papéis

O Odoo valida o cadastro da banca checando os parâmetros ativos para o nível (Mestrado/Doutorado) e rito (Qualificação/Defesa):

* **Quórum de Titulares:** 
  * *Mestrados (Geral):* Mínimo de 3 titulares (ex: IPEN, Mackenzie, CDTN, USP).
  * *Doutorados:* Configurável para 3 ou 5 titulares (ex: 5 membros no CDTN e USP).
* **Quórum de Suplentes:**
  * *Regra de Par Fixo (Mackenzie):* Exige 2 suplentes (1 interno e 1 externo).
  * *Regra Proporcional (USP Art. 89 §5º):* Exige 1 suplente para cada membro titular.
* **Papel e Voto do Orientador:**
  * *Modo Votante (`voting_president`):* O orientador preside e vota (MPTRCS/IPEN e Mackenzie).
  * *Modo Não-Votante (`non_voting_president`):* O orientador preside a sessão, mas abstém-se de votar e atribuir nota (Regra CDTN Art. 44 §4º e opção USP).
* **Papel do Coorientador:**
  * Configurado como membro adicional sem direito a voto (Mackenzie/CDTN), ou com participação vedada caso o orientador esteja presente (MPTRCS Art. 10 §3º).

### 4.2. Motor de Impedimentos Éticos e Endogenia

1. **Vedação de Voto Simultâneo / Conflito:** Orientador e Coorientador não podem computar votos cumulativos na fração votante.
2. **Validação de Endogenia (Membros Externos):**
   * *Mínimo 1 Externo:* Exige pelo menos 1 doutor externo ao PPG e à IES (MPTRCS / Mackenzie).
   * *Mínimo 2 Externos:* Exige pelo menos 2 doutores externos ao PPG (Doutorado CDTN).
   * *Maioria Externa (USP Art. 89 §4º):* Valida se a maioria simples dos examinadores votantes é externa ao PPG e pelo menos 1 externo à Unidade.
3. **Trava de Impedimento Cível (USP Art. 89 §3º):** O sistema impede o cadastro de membros com parentesco em linha reta ou colateral até 4º grau com o discente ou orientador.
4. **Exceção de Notória Especialização:** Permite incluir especialistas de mercado sem o título de Doutor, mediante fluxo de aprovação com alçada parametrizada (Aprovação CPG simples, 2/3 da CPG, ou Aprovação CPG + Conselho Superior).

### 4.3. Dinâmica Temporal e Modalidade da Sessão

* **Cronometria Parametrizada:** Os tempos limite de exposição do candidato (ex: 50 min no IPEN, 45 min no CDTN) e de arguição por examinador (ex: 40 min) são definidos na versão curricular e gravados na ata QWeb.
* **Política de Presença (`defense_location_policy`):**
  * *Presencial / Híbrida:* Presença física obrigatória do aluno e presidente, permitindo examinadores remotos (IPEN / Mackenzie).
  * *Totalmente Remota:* Permite sessões 100% virtuais mediante justificativa e autorização do colegiado (CDTN Art. 49 / USP).

---

## 5. Homologação Final, Depósito no Repositório (DSpace) e Titulação

Após a aprovação na defesa pública, o rito transita para o estado `deposit_pending` (Pendente Envio Versão Final Aluno).

```text
[Defesa Pública Aprovada na Banca]
               │
               ▼
   [Status: deposit_pending]
               │
               ▼
[Discente: Upload da Versão Final PDF no Portal Odoo (Prazo Regimental)]
               │
               ▼
[Status: final_version_submitted]
               │
               ▼
[Secretaria Acadêmica: Triagem de Formatação & Ficha Catalográfica]
               │
               ▼
[Clique: "Validar Versão Final & Titular (Secretaria OK)"]
               │
               ├─────────────────────────────────────────┐
               ▼                                         ▼
 [Status Discente: TITULADO]             [Geração do Manifesto DSpace (XML)]
 (Histórico Congelado e Elegível                 │
  ao Diploma Digital MEC 70/2025)                ▼
                                  [Envio PDF + Manifesto à Biblioteca Central]
                                                 │
                                                 ▼
                                  [Biblioteca: Upload Oficial no DSpace]
                                                 │
                                                 ▼
                                  [Averbação do Handle (repository_url)]
```

1. **Upload da Versão Final pelo Discente:** O discente dispõe do prazo regimental pós-defesa (ex: 30 dias) para aplicar as revisões recomendadas pela banca e realizar o upload da versão final corrigida do PDF no Portal do Aluno Odoo (contendo capa, folha de aprovação e ficha catalográfica), alterando o status para `final_version_submitted`.
2. **Validação da Secretaria e Titulação Instantânea:** A Secretaria Acadêmica efetua a triagem documental e, ao confirmar a conformidade do arquivo, aciona a ação de validação (`secretariat_approval = True`). O sistema altera imediatamente o status do rito para `homologated` e o discente para **Titulado**, selando a data de titulação no histórico escolar e habilitando a esteira do Diploma Digital Nato-Digital.
3. **Geração do Manifesto e Depósito na Biblioteca:** Simultaneamente à titulação, o Odoo gera o manifesto de metadados acadêmicos (`library_manifest_payload`). A Secretaria encaminha a Ordem de Serviço com o PDF e os metadados para a Biblioteca Central, responsável exclusiva pela submissão do trabalho no DSpace (Fonte Ouro) e posterior averbação do Handle (`repository_url`).
