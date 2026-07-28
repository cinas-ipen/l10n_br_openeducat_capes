# **Validação Técnica MP3 - Vida Estudantil e Matrículas**

## **1. Introdução**

Este documento detalha o **Macroprocesso 3: Vida Estudantil e Matrículas** do ecossistema l10n_br_openeducat_capes. O objetivo desta especificação é fornecer aos *stakeholders* do MPTRCS uma visão clara, didática e auditável de como o ERP OpenEduCat gerencia o ciclo letivo, garantindo conformidade com as exigências da CAPES e a imutabilidade dos registros acadêmicos.

Este processo é a espinha dorsal da "Fonte Prata" de dados acadêmicos, onde a vida cotidiana do estudante é transposta para registros digitais que alimentam a governança do programa.

## **2. Estrutura de Oferta e Turmas (op.batch e op.session)**

O sistema abandona a oferta manual e adota uma estrutura parametrizável que garante a consistência das turmas.

### **2.1. Parâmetros da Turma**

Para cada disciplina, a secretaria configura uma instância de op.batch (Turma). Os parâmetros chave incluem:

* **Capacidade Mínima (Quórum):** O sistema impede a consolidação de turmas que não atingem o número mínimo de inscritos, evitando o desperdício de recursos e a abertura de turmas "fantasmas".  
* **Composição Docente:** A turma pode vincular até 4 docentes (1 Coordenador e até 3 auxiliares), todos portadores de título de Doutor, garantindo a conformidade com as diretrizes do Comitê Medicina II/Ensino.  
* **Indicador de PHEA:** Parametrização específica para o uso de metodologias híbridas (PHEA), atendendo às novas regulamentações de ensino na pós-graduação.

## **3. Fluxos de Matrícula e Travas de Controle**

A matrícula não é um processo apenas administrativo, mas um gatilho de auditoria.

### **3.1. Calouros e Carga Inicial Obrigatória**

O sistema aplica uma **Trava de Carga Inicial**. O algoritmo verifica automaticamente se a seleção de disciplinas do ingressante respeita o parâmetro min_first_semester_credits definido no currículo (ex: 24 créditos). Caso o aluno selecione menos que o mínimo regimental, o sistema bloqueia a finalização da matrícula, forçando o ajuste imediato.

### **3.2. Matrícula de Acompanhamento (Pesquisa)**

Para evitar a "inatividade fictícia" (um dos maiores pontos de atenção da CAPES), o sistema institui a **Matrícula de Acompanhamento**. Após o cumprimento dos créditos teóricos, o aluno deve se matricular obrigatoriamente na atividade de "Elaboração de Dissertação/Tese". Isso mantém o aluno com status "Ativo" no banco de dados, crucial para a coleta passiva da Fonte Prata.

### **3.3. Cancelamento sem Prejuízo (Artigo 41º do MPTRCS e Anuência Tácita)**

O processo de desistência de disciplinas segue o Artigo 41º do regulamento, com salvaguardas tecnológicas:

1. **Solicitação:** O aluno solicita o cancelamento via portal dentro do prazo do calendário acadêmico.  
2. **Anuência do Orientador:** O sistema roteia o pedido automaticamente para o orientador.  
3. **SLA e Anuência Tácita:** O orientador possui um prazo (SLA de 5 dias úteis) para aprovar ou indeferir.  
   * **Default Sistêmico:** Se o prazo expirar sem manifestação do orientador, o sistema aplica a **Anuência Tácita = True**, processando o cancelamento automaticamente para proteger o aluno de impedimentos burocráticos.  
4. **Efeitos:** O registro é removido das pautas sem atribuir conceito reprovativo "R". O cancelamento **não altera a contagem dos prazos regimentais** (não tem efeito suspensivo).

## **4. O Livro-Razão Acadêmico (op.student.credit.ledger)**

Este é o componente mais crítico para a segurança jurídica e acadêmica do programa.

### **4.1. Arquitetura *Append-Only***

Ao final do semestre, após o lançamento de notas e frequências (mínimo de 75%), a secretaria consolida a turma. Neste instante, o sistema realiza a **Injeção de Créditos**. Estes dados entram na tabela op.student.credit.ledger, que é **imutável**.

* **Por que é imutável?** Para impedir que cálculos retroativos ou alterações indevidas de notas corrompam o histórico do aluno.  
* **O que é registrado?** Tipo de crédito (disciplina, APO, milestone de qualificação), carga horária e conceito.

## **5. Fluxos de Exceção: Ajustes Retroativos Auditados**

Para situações como demandas judiciais ou retificações da CPG, criamos o fluxo de **Ajuste Manual Retroativo (op.academic.request.grade_adjustment)**:

1. **Abertura:** Docente ou secretaria abre chamado justificando (com upload de prova documental).  
2. **Aprovação:** O requerimento é roteado para a Coordenação do Programa.  
3. **Auditoria:** Após o clique do Coordenador, a secretaria executa a retificação. O sistema **não apenas altera o dado**, mas gera um selo de auditoria indelével no histórico, que registra quem alterou, quando e por qual motivo. Isso blinda o programa contra auditorias da CAPES.

## **6. Resumo para Stakeholders (MPTRCS)**

| Funcionalidade | Benefício para o Programa |
| :---- | :---- |
| **Travas Automáticas** | Elimina erros humanos na carga horária inicial (calouros). |
| **Matrícula de Acompanhamento** | Mantém a produtividade ativa perante a CAPES durante a pesquisa. |
| **Anuência Tácita (Art. 41º)** | Agiliza o cancelamento, protegendo o aluno de omissões do orientador. |
| **Livro-Razão Imutável** | Garante a integridade absoluta do histórico escolar contra fraudes. |
| **Auditoria de Ajustes** | Protege a coordenação em casos de retificações solicitadas. |
| **Integração GoPG** | Dados prontos para o robô da CAPES (sem redigitação). |

Este detalhamento assegura que todos os subprocessos da Vida Estudantil sejam executados com rigor técnico, eliminando a dependência de métodos manuais arcaicos e posicionando o MPTRCS na vanguarda da governança de dados acadêmicos.
