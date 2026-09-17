# Manual Operacional do Usuário: Secretaria do Programa de Pós-Graduação
## Ecossistema l10n_br_openeducat_capes (Odoo 19.0)

Este manual destina-se aos servidores técnicos, secretários acadêmicos e analistas responsáveis pelo suporte operacional e gestão do cotidiano acadêmico do Programa de Pós-Graduação.

---

## 1. Perfil de Acesso e Ambiente de Trabalho

* **Grupo de Segurança Odoo:** `openeducat_core.group_op_back_office_admin` (Back-Office Acadêmico)
* **Usuário Padrão de Homologação/Treinamento:** `secretaria` / Senha: `secretaria123`
* **Menus Principais de Atuação:**
  * **OpenEduCat $ightarrow$ Alunos** e **Professores** (Fichas cadastrais com Visão 360°)
  * **OpenEduCat $ightarrow$ Configuração** (Anos Acadêmicos, Períodos/Termos, Cursos, Turmas/Lotes, Departamentos, Categorias)
  * **Ensino CAPES $ightarrow$ Discentes & Vínculos**
  * **Ensino CAPES $ightarrow$ Matrículas & Turmas**
  * **Ensino CAPES $ightarrow$ Requerimentos & CPG**
  * **Ensino CAPES $ightarrow$ Bancas & Titulação**
  * **Ensino CAPES $ightarrow$ Livro-Razão Acadêmico**

---

## 2. Atividades do Cotidiano da Secretaria

### 2.1. Processamento de Editais e Conversão de Candidatos
Ao finalizar as etapas de um processo seletivo (`op.admission.edital`):
1. Acesse **Ensino CAPES $ightarrow$ Editais de Admissão**.
2. Abra o edital vigente e clique na aba **Candidatos Aprovados**.
3. Selecione o candidato homologado e clique em **Converter em Aluno**:
   * O sistema verifica automaticamente se o CPF já possui um `op.student` cadastrado na IES (por exemplo, discente que foi Aluno Especial no passado).
   * Se já existir, seu Registro Acadêmico (RA perene) é preservado integralmente, atualizando a categoria para `regular` e criando uma nova linha de vínculo (`op.student.course`).
   * Se for um aluno inédito na instituição, o Odoo aciona a sequência automática e emite um novo RA vitalício.

### 2.2. Gestão de Matrículas Semestrais e Trânsito Intra-IES
1. No início de cada período letivo, acesse **Matrículas $ightarrow$ Matrículas Semestrais**.
2. **Matrícula em Disciplinas do Programa:** Validação das escolhas submetidas pelos alunos regulares via portal.
3. **Matrícula Cruzada Intra-IES:**
   * Quando um discente de outro programa da mesma IES solicita matrícula em disciplinas do seu PPG, verifique se a disciplina possui cota aberta e se o orientador deu o aceite.
   * Confirme a inscrição. O sistema efetuará o lançamento automático com tipo `subject_intra_ies`.
4. **Matrícula de Acompanhamento (Dissertação/Tese):**
   * Alunos que já integralizaram os créditos em disciplinas e estão dedicados à pesquisa devem ser matriculados no código de acompanhamento semestral para evitar abandono de curso.

### 2.3. Gestão de Alunos Especiais e Quarentena de Créditos
1. Para cursos cujo regimento autoriza Alunos Especiais (`allow_special_students = True`):
   * O cadastro do discente é gerado com `student_category = 'special'`.
   * Ao lançar o resultado das disciplinas cursadas no regime especial, o Livro-Razão grava automaticamente o lançamento como **`subject_special_quarantine`**.
2. **Importante:** A secretaria **nunca** deve alterar manualmente lançamentos em quarentena para torná-los regulares. O aproveitamento ocorre exclusivamente por requerimento formal via CPG.

### 2.4. Tramitação de Requerimentos de Aproveitamento de Créditos Especiais
Quando um ex-aluno especial ingressa como discente regular:
1. O discente submete o pedido via Portal ou balcão da secretaria.
2. A secretaria autua em **Requerimentos $ightarrow$ Incorporação de Créditos Especiais** (`op.special.credit.incorporation.request`):
   * Seleciona o discente e as disciplinas pretendidas.
   * O sistema audita automaticamente se a data de conclusão da disciplina está dentro do prazo decadencial de **36 meses (3 anos)**. Se tiver mais de 3 anos, o sistema bloqueia o avanço.
   * Verifica o limite regimental de disciplinas aproveitáveis (ex: até 2 disciplinas).
3. Encaminha para parecer do orientador (`action_submit`).
4. Após o parecer do orientador, inclui o requerimento na pauta da próxima reunião da CPG.

### 2.5. Organização de Reuniões da CPG e Emissão de Atas
1. Acesse **Governança CPG $ightarrow$ Reuniões da CPG** (`op.cpg.meeting`).
2. Cadastre uma nova reunião indicando: Data, Horário, Local e Pauta (processos autuados, bancas, aproveitamentos).
3. Registre os membros presentes e o quórum regulamentar.
4. Após as votações, registre as resoluções homologadas e clique em **Gerar Ata da Reunião**:
   * O sistema compila automaticamente o documento em formato QWeb PDF para assinatura eletrônica dos membros.

### 2.6. Organização de Bancas de Defesa e Titulação
1. Acesse **Bancas & Titulação $ightarrow$ Trabalhos Finais** (`capes.thesis`).
2. Ao receber a solicitação de agendamento de defesa:
   * O sistema realiza a pré-validação do Art. 39º (Verificação se créditos mínimos em disciplinas foram cumpridos, seminário geral aprovado, proficiência liberada e CEP/CEUA liberado).
   * Se houver pendências, o botão de avanço é bloqueado com mensagem explicativa.
3. Cadastre a Composição da Banca (Membros Titulares e Suplentes). O sistema audita se há membros com impedimento cível (`civil_relationship_flag`) ou déficit de examinadores externos (endogenia).
4. Emita o **Edital de Convocação de Banca** e a **Folha de Julgamento**.

### 2.7. Recepção da Versão Final e Comunicação com a Biblioteca Central
1. Após a defesa aprovada, o aluno envia o PDF definitivo corrigido via portal.
2. A secretaria confere a formatação, capa e ficha catalográfica e clica em **Validar Versão Final & Titular**:
   * O status da defesa (`capes.thesis`) passa para `homologated`, o vínculo de curso (`op.student.course`) é concluído (`state = 'finished'`) e o discente (`op.student`) é categorizado como egresso/titulado (`student_category = 'alumni'`).
   * O histórico escolar é automaticamente congelado para evitar edições futuras.
   * É gerado o Manifesto XML (`library_manifest_payload`).
3. A secretaria remete a ordem de serviço com o manifesto e o PDF para a Biblioteca Central providenciar o upload oficial no repositório institucional DSpace.
4. Ao receber o Handle permanente (URI) emitido pela Biblioteca, insira no campo `repository_url`.

### 2.8. Emissão de Histórico Escolar Oficial e Dossiê de Diploma
1. Em **Bancas & Titulação $ightarrow$ Dossiês e Diplomas Digitais**:
   * Clique em **Gerar Pacote de Titulação**.
   * O sistema compila o histórico consolidado oficial.
   * Conforme a regra `omit_on_regular`, o sistema exclui automaticamente quaisquer disciplinas mantidas em quarentena (não incorporadas) e eventuais reprovações do período de aluno especial.
2. **Encaminhamento para Registro:**
   * Se a instituição tiver autonomia registradora direta (Universidades): gera o XML do Diploma Digital (MEC 70/2025).
   * Se for Instituto de Pesquisa sem autonomia universitária (como o **IPEN-CNEN/SP**): o sistema gera a Guia de Remessa e Ofício de Encaminhamento para registro externo na **USP**, com número de protocolo e livro/folha de escrituração.

### 2.9. Operação com Visão 360° do Discente e do Docente
Para atendimento rápido ao público e auditoria interna:
1. **Visão 360° do Discente (`op.student`):**
   * Ao abrir a ficha do aluno, utilize o botão **"Imprimir Histórico Escolar"** no cabeçalho para gerar o documento oficial sem necessidade de navegar até os relatórios de diploma.
   * Consulte os **Smart Buttons** no topo do formulário: veja instantaneamente a quantidade de cursos/vínculos, lançamentos no livro-razão, bancas agendadas/aprovadas, produtos PTT associados, chamados de requerimento e diplomas.
   * Consulte a aba **Livro-Razão de Créditos** para auditar notas, conceitos e créditos de cada disciplina em tempo real.
2. **Visão 360° do Docente (`op.faculty`):**
   * Ao abrir a ficha do professor, visualize os smart buttons com a contagem de orientandos ativos, egressos titulados, disciplinas ministradas e participações em bancas examinadoras.
