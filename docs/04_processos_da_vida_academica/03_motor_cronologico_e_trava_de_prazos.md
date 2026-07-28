# Documento 03: Motor Cronológico, Trava de Prazos e Jubilamento

## 1. O Relógio Implacável da Pós-Graduação

Na avaliação quadrienal da CAPES, o "Tempo Médio de Titulação" é uma métrica central. O ERP atua como um motor cronológico fiscalizador acionado a partir da data oficial de admissão do discente (`admission_date`).

O parâmetro vital de controle é o campo `max_months_defense` registrado no regimento do aluno (`op.curriculum.version`), fixado em **24 meses** para o Mestrado Profissional do IPEN.

## 2. Regras Algorítmicas de Trancamento de Matrícula

O trancamento de matrícula pausa a contagem do relógio cronológico (`max_months_defense`), mas obedece rigorosamente às restrições configuradas na `op.curriculum.version` e ao rito de aprovação da CPG:

* **Categorias Legais Exigidas:** Conforme o regulamento (ex: Art. 22º do MPTRCS), o estudante pode pleitear a suspensão nos casos de Serviço Militar, Problemas de Saúde Incapacitantes (com atestado e CID `cid_code`), Acompanhamento de Cônjuge/Parente de 1º Grau ou Demais casos previstos em lei/excepcionais. **Nenhum trancamento é efetivado de forma automática pelo sistema**: todas as solicitações protocoladas no portal dependem obrigatoriamente de triagem documental prévia da secretaria e de aprovação formal em pauta de reunião da CPG.
* **Flexibilidade de Período (Parametrizável):** Em conformidade com o Art. 22º, §1º, o sistema permite que o pedido seja submetido em qualquer época do curso (sem trava restritiva padrão para o 1º semestre no MPTRCS). Programas que exijam o bloqueio no primeiro semestre devem ativar o parâmetro booleano `block_first_semester_trancamento` = `True` na versão curricular.
* **Limite Contínuo Personalizado:** O algoritmo valida o somatório dos períodos de trancamento com base no parâmetro regimental `max_trancamento_days` (configurado para o teto contínuo de 365 dias no MPTRCS, Art. 22º, §3º).
* **Retorno e Ato Jurídico Perfeito (Art. 23º):** Ao retornar do trancamento, o discente é vinculado à estrutura curricular vigente na data de retorno. O sistema preserva integralmente as notas e créditos obtidos anteriormente no Livro-Razão (`op.student.credit.ledger`), mas submete o aluno às normas vigentes para as etapas futuras, vedando o hibridismo normativo.


## 3. Prorrogações de Prazo e Exceções CAPES (> 90 Dias)

* **Prorrogação Regular:** O aluno e orientador solicitam extensão de prazo via portal. O sistema valida se o aluno já possui o Plano de Trabalho homologado e foi aprovado no Seminário Geral de Área / Exame de Qualificação. As prorrogações regulares são limitadas ao teto configurado no regimento do aluno (`max_extension_days`, ex: 90 dias no IPEN ou até 6/12 meses no CDTN e Mackenzie).
* **Trava Documental para Prorrogações Extraordinárias:** Em situações de contingência nacional (ex: pandemias ou calamidades públicas), a CPG pode conceder prorrogações superiores ao teto configurado no regimento do aluno (`max_extension_days`). Para liberar esta trava no Odoo, a secretaria é obrigada a anexar o arquivo PDF da Portaria ou Comunicado Oficial publicado pela CAPES reconhecendo a excepcionalidade.

## 4. Jubilamento Automático (`pending_dismissal`)

Diariamente, à meia-noite, uma Ação Agendada (Cron Job) do Odoo varre os prazos de todos os discentes ativos:

1. **Estouro de Prazo Limite:** Estudantes que ultrapassarem a data limite de defesa (ingresso + 24 meses + trancamentos + prorrogações) sem depósito registrado da dissertação têm o status alterado para `pending_dismissal`.
2. **Reprovação Dupla:** O sistema monitora reprovações acumuladas. Ocorrendo duas reprovações em disciplinas ou duas reprovações no Seminário Geral de Área / Exame de Qualificação, o Odoo altera o status para `pending_dismissal`.
3. **Desligamento Efetuado:** O status `pending_dismissal` cessa imediatamente a exportação do discente como "Matriculado Ativo" para os endpoints da CAPES (Fonte Prata), isolando o programa contra deterioração nos indicadores estatísticos.

```python
# Lógica Python de Verificação do Jubilamento Automático
def _check_dismissal_deadlines(self):
    active_students = self.env['op.student'].search([('status', '=', 'Matriculado')])
    for student in active_students:
        deadline = student._compute_absolute_deadline() # Ingresso + max_months + prorrogações ativas
        
        if datetime.today().date() > deadline and not student.has_defended():
            student.status = 'pending_dismissal'
            student.message_post(
                body="Transição automática para Pendente de Desligamento: Prazo máximo de defesa excedido sem depósito registrado."
            )

```
