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
O livro-razão no `l10n_br_openeducat_capes` extrapola a medição de disciplinas convencionais em sala de aula. A entidade categoriza e injeta os lançamentos obedecendo às tipologias regulamentares:

```python
# Exemplo conceitual da classificação no Ledger
class OpStudentCreditLedger(models.Model):
    _name = 'op.student.credit.ledger'
    
    credit_type = fields.Selection([
        ('subject', 'Disciplinas Regulares'),
        ('apo', 'Atividades Programadas Obrigatórias (APO) / Produção Técnica'),
        ('milestone', 'Créditos por Qualificação e Defesa'),
        ('external', 'Aproveitamento de Créditos Externos')
    ], string="Natureza do Crédito", required=True)
```

* **Atividades Programadas (APO):** Suporta a modelagem de atividades extraclasse exigidas em programas profissionais, convertendo publicações de artigos, depósitos de patentes ou desenvolvimento de software em unidades de crédito essenciais.
* **Injeção Automática de Ritos:** Ao aprovar transições de estado nas máquinas de workflow de qualificação e defesa (módulo `capes.thesis`), o sistema injeta automaticamente os créditos bonificados previstos nos regimentos do Mackenzie e IPEN diretamente no livro-razão.
* **Limites de Aproveitamento Externo:** Durante o requerimento de aproveitamento de créditos obtidos em outras instituições, as rotinas de validação em Python verificam a propriedade `max_external_credits_percent` configurada no currículo do aluno. O sistema barrará submissões que excedam tetos regulamentares (ex: bloqueando aprovações acima de 40% para o Mackenzie ou 50% para o IPEN).
