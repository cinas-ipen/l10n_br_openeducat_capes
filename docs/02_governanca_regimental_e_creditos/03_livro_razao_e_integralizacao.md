# Documento 03: Livro-Razão e Integralização Parametrizada de Créditos

## 1. O Livro-Razão Acadêmico (`op.student.credit.ledger`)
Para garantir a imutabilidade do Ato Jurídico Perfeito e blindar a instituição contra cálculos retroativos indevidos causados pela alteração do cadastro de disciplinas, a arquitetura abandona consultas fluídas de notas e implementa a entidade `op.student.credit.ledger` (Livro-Razão de Créditos).

Este modelo obedece ao padrão de arquitetura de software *append-only* (apenas inserção). Quando uma turma é consolidada e fechada, o sistema realiza os lançamentos oficiais dos créditos conquistados pelo aluno nesta tabela. A ausência de permissões para ações nativas de `unlink` (deleção) ou recálculos em lote garante que eventos consolidados no passado tornem-se imutáveis.

## 2. A Variação Institucional e a Matriz de Integração Híbrida
A arquitetura do livro-razão foi projetada para lidar com a extrema variação nas regras de integralização exigidas pelos institutos de pesquisa e universidades brasileiras dentro da mesma base de dados, utilizando o motor de cálculo atrelado à versão do currículo.

Através de campos calculados via framework Odoo (decorador Python `@api.depends`), o sistema processa múltiplos cenários de forma independente:

* **Cálculo Paramétrico de Carga Horária:** O algoritmo interpreta que 1 crédito equivale a 15 horas de trabalho para os discentes submetidos aos regimentos do IPEN e do CDTN, mas computa 1 crédito como 12 horas para estudantes vinculados às matrizes curriculares do Mestrado Profissional do Mackenzie.
* **Metas de Integralização Distintas:** O motor afere automaticamente se o aluno atingiu a meta de integralização baseada no seu vínculo: 100 unidades de crédito exigidas no IPEN, 50 unidades no Mackenzie, e variações de 24 (Mestrado) ou 47 (Doutorado) créditos no CDTN.

## 3. Classificação e Aproveitamento de Atividades
O livro-razão no `l10n_br_openeducat_capes` extrapola a medição de disciplinas convencionais em sala de aula. A entidade categoriza e injeta os lançamentos obedecendo às tipologias regulamentares refinadas para o ambiente multi-programas e multi-vínculos:

```python
# Mapeamento oficial dos tipos de lançamento no Livro-Razão de Créditos
class OpStudentCreditLedger(models.Model):
    _name = 'op.student.credit.ledger'
    _description = 'Livro-Razão Acadêmico de Créditos (Append-Only)'
    _order = 'date_earned desc, id desc'

    credit_type = fields.Selection([
        ('subject', 'Disciplinas Regulares'),
        ('subject_internal', 'Disciplinas do Próprio Programa'),
        ('subject_intra_ies', 'Disciplinas de outros PPGs da mesma IES (100% Equivalência)'),
        ('subject_special_quarantine', 'Créditos em Quarentena (Aluno Especial)'),
        ('subject_special_incorporated', 'Créditos de Aluno Especial Incorporados (Homologados CPG)'),
        ('subject_extra_ies', 'Disciplinas Externas de Outras IES (Com Equivalência)'),
        ('apo', 'Atividades Programadas Obrigatórias (APO) / PTT'),
        ('milestone', 'Créditos por Qualificação e Defesa'),
        ('external', 'Aproveitamento de Créditos Externos')
    ], string='Natureza do Crédito', required=True, index=True)

    incorporation_request_id = fields.Many2one(
        'op.special.credit.incorporation.request',
        string='Requerimento de Incorporação CPG'
    )
    original_program_id = fields.Many2one(
        'op.program.capes',
        string='Programa Ofertante de Origem'
    )
```

* **Disciplinas Intra-IES:** Cursadas pelo aluno regular em outros programas da mesma instituição (`res.company`). Integram-se com 100% do valor nominal de carga horária e créditos, respeitando o limite parametrizado em `max_intra_ies_credits_percent`.
* **Disciplinas Extra-IES (Casos Externos e USP/IPEN):** Disciplinas cursadas fora da instituição mantenedora. No caso do MPTRCS (IPEN), disciplinas cursadas no programa de Tecnologia Nuclear (titulado pela USP) são tratadas formalmente como `subject_extra_ies`, exigindo parecer e aprovação da CPG e respeitando a trava de teto `max_external_credits_percent` (ex: máx. 50% de `min_subject_credits`, limitando a 20.0 créditos no IPEN).
* **Atividades Programadas (APO):** Suporta a modelagem de atividades extraclasse exigidas em programas profissionais, convertendo publicações de artigos, depósitos de patentes ou desenvolvimento de software em unidades de crédito essenciais.
* **Injeção Automática de Ritos:** Ao aprovar transições de estado nas máquinas de workflow de qualificação e defesa (módulo `capes.thesis`), o sistema injeta automaticamente os créditos bonificados previstos nos regimentos diretamente no livro-razão.
* **Validação por Categoria para Titulação (Artigos 31º e 39º do Regulamento MP-TRCS):** Para o agendamento da Defesa Final, a engine valida no livro-razão se o discente cumpriu separadamente os `min_subject_credits` (40 créditos em disciplinas) e os `other_mandatory_credits` (8 créditos do Seminário Geral de Área), além da meta total de `min_credits` (100 créditos).

## 4. O Ciclo de Quarentena e Incorporação de Créditos de Aluno Especial

Para estudantes admitidos inicialmente como Alunos Especiais (disciplinas isoladas):

1. **Lançamento Primitivo em Quarentena:** As disciplinas concluídas com aprovação recebem o tipo `subject_special_quarantine`. Esses créditos não são somados ao total de integralização de nenhum curso regular e servem exclusivamente para a emissão de Certidão de Estudos Isolados.
2. **Requerimento de Incorporação (`op.special.credit.incorporation.request`):** Quando o aluno ingressa regularmente em um PPG (ex: MPTRCS), o aproveitamento não é automático. O discente submete um requerimento formal indicando quais disciplinas deseja integralizar.
3. **Travas Sistêmicas de Admissibilidade:**
   * *Verificação Decadencial:* O sistema calcula o intervalo entre a data de conclusão da disciplina e a data de ingresso regular. Caso supere o limite regimental (`special_credit_validity_months`, padrão de **36 meses / 3 anos**), o sistema rejeita a linha como "Crédito Prescrito".
   * *Verificação de Teto:* O sistema bloqueia requisições que excedam o limite máximo de disciplinas isoladas permitido pelo regimento (`max_special_subjects_limit`).
4. **Deliberação Colegiada:** O pedido tramita com parecer do orientador e julgamento pela CPG, registrando o número da resolução e a data da reunião.
5. **Efeito Append-Only no Livro-Razão:** Ao deferir o pedido, o sistema gera lançamentos adicionais no livro-razão com tipologia `subject_special_incorporated`, vinculados ao `curriculum_version_id` ativo do aluno e com apontador para o requerimento deferido, mantendo a linha original de quarentena intacta para fins de auditoria.

## 5. Governança Append-Only e Retificações de Lançamento

Em observância ao princípio da imutabilidade e rastreabilidade total:
* **Bloqueio Irrevogável de Deleção (`unlink`):** O método `unlink()` da classe `OpStudentCreditLedger` dispara um `UserError` bloqueando qualquer exclusão direta via interface web, scripts de lote ou orquestração externa.
* **Retificações Administrativas:** Caso um lançamento tenha ocorrido por equívoco administrativo ou revisão de nota homologada pela CPG, o sistema proíbe a edição ou deleção do registro original. A correção exige a inserção de um **novo lançamento retificador compensatório** com observações auditáveis no campo `notes` e vinculação documental em `origin_ref`, garantindo que toda a linha do tempo histórica do discente permaneça intacta e auditável por órgãos de controle e pela CAPES.

