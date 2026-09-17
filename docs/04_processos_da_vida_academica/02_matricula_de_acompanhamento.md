# Documento 02: Operacionalização de Turmas, Matrículas e Ajustes Retroativos

## 1. Oferta de Turmas e Regras de Composição Docente

A oferta semestral de disciplinas em `op.batch` e `op.session` obedece a travas de capacidade e quórum:

* **Quórum Mínimo e Cotas Especiais:** A secretaria cadastra a capacidade mínima da turma. Se a janela de matrícula fechar sem atingir o quórum, o Odoo emite um alerta, cancela a oferta e notifica os alunos para remanejamento. Para turmas que aceitam Alunos Especiais (`allow_special_students = True`), o sistema reserva a cota parametrizada em `special_seats_quota`.
* **Equipe Docente Híbrida e Anuência Prévia:** O sistema permite vincular a uma mesma turma 1 Coordenador (docente permanente) e até 3 outros professores portadores do título de Doutor. Quando ativada a exigência `special_student_instructor_consent_required`, as solicitações de matrícula em disciplinas isoladas são roteadas para o aceite explícito do ministrante responsável.

## 2. Inscrições Semestrais, Trava de Calouros e Matrículas Intra-IES

* **Carga Inicial Obrigatória (Calouros):** No semestre de admissão (calouros), o algoritmo impedirá a finalização da matrícula caso a seleção de disciplinas seja inferior ao mínimo parametrizado no regimento (`min_first_semester_credits`, ex: 24 créditos no IPEN MPTRCS).
* **Matrícula Cruzada Intra-IES (Programas da Mesma IES):**
  * O discente regular de um programa pode se inscrever em disciplinas ofertadas por outros PPGs da mesma IES mantenedora (`res.company`).
  * O requerimento passa pelo crivo eletrônico do orientador (`intra_ies_advisor_approval_required`) e pelo aceite do docente da disciplina.
  * Os créditos cursados com êxito são consolidados no histórico discente no valor integral (100% nominal), sem perda de equivalência, respeitando o limite teto regimental do programa de origem (`max_intra_ies_credits_percent`).
  * *Observação IPEN:* Disciplinas cursadas no programa de Tecnologia Nuclear (USP) não se enquadram neste fluxo automático, sendo tratadas como extra-IES com necessidade de validação formal de equivalência e pauta na CPG do MPTRCS.
* **Inscrição em Matrícula de Acompanhamento:** Para resolver o problema da "inatividade fictícia" durante a fase exclusiva de pesquisa e elaboração de dissertação (após o cumprimento dos créditos teóricos), o sistema força a inscrição compulsória semestral na disciplina contínua "Elaboração de Dissertação" (0 créditos teóricos), mantendo o discente com status "Ativo e Matriculado" perante a colheita passiva da CAPES (Fonte Prata).

## 3. Cancelamento de Matrícula em Disciplina (Artigo 41º do MPTRCS e Anuência Tácita)

Em estrita conformidade com o regulamento do programa (Artigo 41º), o estudante pode solicitar o cancelamento da inscrição em uma disciplina. O processo obedece aos seguintes parâmetros e salvaguardas sistêmicas:

* **Parametrização Flexível de Prazos:** A CPG-MP define o prazo limite para cancelamento por meio de três opções configuráveis no calendário acadêmico do ERP:
  1. *Dias corridos:* Contados a partir da data de início das aulas de cada disciplina específica.
  2. *Parâmetro Individual por Disciplina:* Janela personalizada de cancelamento vinculada ao plano de ensino da disciplina.
  3. *Data Fixa Global:* Prazo limite uniforme definido no calendário geral do semestre.
* **Anuência Obrigatória do Orientador:** O requerimento submetido pelo discente via Portal do Aluno é encaminhado obrigatoriamente para a anuência eletrônica do orientador, garantindo o controle acadêmico exigido.
* **Proteção Contra Omissão (Anuência Tácita / SLA):** Caso o discente protocole o pedido de cancelamento **dentro do prazo regulamentar**, mas o orientador não se manifeste dentro do SLA estipulado (ex: 5 dias úteis, acionado por razões de viagem ou saúde), o sistema aplica o princípio da **anuência tácita**. O Odoo concede automaticamente o deferimento do cancelamento em favor do aluno, blindando o discente contra prejuízos acadêmicos decorrentes de impasses burocráticos.
* **Efeitos no Histórico e Prazos:** O cancelamento aprovado remove o discente da pauta sem atribuir conceito reprovativo "R" e sem figurar no histórico escolar final. Contudo, o ato **não possui efeito suspensivo** sobre os prazos máximos regimentais de titulação do curso.

## 4. Encerramento de Turmas e Injeção no Livro-Razão

Após o encerramento do semestre, os docentes lançam notas/conceitos (A, B, C, R) e frequências (exigência mínima de 75%). A secretaria revisa os diários e comanda a consolidação. Nesse momento, os créditos são injetados na tabela imutável (*append-only*) `op.student.credit.ledger`, tornando-se definitivos:
* Para alunos regulares em disciplinas do seu próprio PPG: classificados como `subject_internal`.
* Para alunos regulares cursando disciplinas de outros PPGs da IES: classificados como `subject_intra_ies`.
* Para alunos matriculados como especiais: classificados como `subject_special_quarantine` (em quarentena).

## 5. Ajuste Manual Retroativo (Fluxo de Exceção Auditado)

Para atender a determinações judiciais ou retificações homologadas pela CPG, o sistema implementa o formulário de exceção `op.academic.request.grade_adjustment`:

1. O docente ou secretaria abre o chamado informando: Aluno, Disciplina, Semestre, Conceito Original, Conceito Pretendido e Justificativa Detalhada com anexo de provas documentais.
2. O pedido é roteado para aprovação eletrônica do Coordenador do Programa.
3. Após o clique do Coordenador, a secretaria executa a retificação no Livro-Razão. O ERP sobrescreve o dado e gera um selo de auditoria indelével no histórico escolar, registrando o responsável, a data, a hora e o motivo da alteração.
