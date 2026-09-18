###############################################################################
#
#    CINAS Research Group
#    Copyright (C) 2026-TODAY CINAS Research Group(<https://cinas.ipen.br>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
###############################################################################

from odoo import models, fields, api
from collections import defaultdict


class CapesScholarshipEvaluation(models.Model):
    """Ficha de Avaliação da Candidatura por Revisor ou Comissão.
    Suporta o fluxo de múltiplos revisores atuando em paralelo e de forma independente.
    """
    _name = 'capes.scholarship.evaluation'
    _description = 'Ficha de Avaliação de Bolsa'
    _order = 'id desc'

    application_id = fields.Many2one(
        'capes.scholarship.application',
        string='Candidatura',
        required=True,
        ondelete='cascade'
    )
    evaluator_role = fields.Selection([
        ('candidate_self', 'Coluna 1: Autoavaliação do Candidato'),
        ('reviewer_1', 'Coluna 2: Revisor 01'),
        ('reviewer_2', 'Coluna 3: Revisor 02'),
        ('committee', 'Coluna 4: Consolidação da Comissão de Bolsas'),
    ], string='Papel / Via de Avaliação', required=True, default='reviewer_1')

    evaluator_id = fields.Many2one(
        'op.faculty',
        string='Docente Avaliador Responsável',
        ondelete='restrict'
    )
    evaluator_user_id = fields.Many2one(
        'res.users',
        string='Usuário Avaliador',
        compute='_compute_evaluator_user',
        store=True
    )
    line_ids = fields.One2many(
        'capes.scholarship.evaluation.line',
        'evaluation_id',
        string='Linhas Avaliadas'
    )
    total_score = fields.Float(
        string='Pontuação Total Apurada',
        compute='_compute_total_score',
        store=True
    )
    reviewer_comments = fields.Text(string='Parecer Fundamentado do Avaliador')
    state = fields.Selection([
        ('draft', 'Em Andamento'),
        ('completed', 'Concluída / Emitida'),
    ], string='Situação', default='draft')

    @api.depends('evaluator_id.user_id')
    def _compute_evaluator_user(self):
        for rec in self:
            rec.evaluator_user_id = rec.evaluator_id.user_id if rec.evaluator_id else False

    @api.depends('line_ids.calculated_score')
    def _compute_total_score(self):
        for rec in self:
            rubric = rec.application_id.edital_id.rubric_id
            if not rubric:
                rec.total_score = sum(rec.line_ids.mapped('calculated_score'))
                continue

            # Agrupa por categoria para aplicar tetos de categoria
            category_totals = defaultdict(float)
            for line in rec.line_ids:
                category_totals[line.category] += line.calculated_score

            total = 0.0
            for item in rubric.item_ids:
                cat = item.category
                cat_sum = category_totals.get(cat, 0.0)
                if item.category_cap_points > 0:
                    cat_sum = min(cat_sum, item.category_cap_points)
                # Adiciona uma vez por categoria processada
                if cat in category_totals:
                    total += cat_sum
                    del category_totals[cat]

            # Adiciona quaisquer categorias restantes sem regra de teto específica
            total += sum(category_totals.values())

            # Aplica teto global do barema se definido
            if rubric.total_max_points > 0:
                total = min(total, rubric.total_max_points)

            rec.total_score = total

    def _init_lines_from_rubric(self, rubric):
        """Inicializa as linhas da avaliação copiando os itens do barema."""
        self.ensure_one()
        lines = []
        for item in rubric.item_ids:
            lines.append((0, 0, {
                'rubric_item_id': item.id,
                'quantity': 1.0,
            }))
        self.write({'line_ids': lines})

    def action_complete(self):
        for rec in self:
            rec.state = 'completed'
            rec.application_id.consolidate_scores()


class CapesScholarshipEvaluationLine(models.Model):
    """Linha da Ficha de Avaliação com Cálculo de Pontuação e Comprovação."""
    _name = 'capes.scholarship.evaluation.line'
    _description = 'Item Avaliado na Ficha de Bolsa'
    _order = 'rubric_item_id, id'

    evaluation_id = fields.Many2one(
        'capes.scholarship.evaluation',
        string='Ficha de Avaliação',
        required=True,
        ondelete='cascade'
    )
    rubric_item_id = fields.Many2one(
        'capes.scholarship.rubric.item',
        string='Critério do Barema',
        required=True,
        ondelete='restrict'
    )
    category = fields.Selection(related='rubric_item_id.category', string='Categoria', store=True)
    item_name = fields.Char(related='rubric_item_id.name', string='Descrição do Item', readonly=True)
    calculation_formula = fields.Selection(
        related='rubric_item_id.calculation_formula',
        string='Fórmula',
        readonly=True
    )

    quantity = fields.Float(string='Qtd / Ocorrências', default=1.0)
    months = fields.Integer(string='Duração em Meses')
    num_authors = fields.Integer(string='Número de Autores (Rateio)', default=1)
    direct_score = fields.Float(string='Nota Atribuída (1 a 5)')
    dossier_page_ref = fields.Char(string='Folha(s) do Dossiê', help='Ex.: Páginas 15 a 18')

    calculated_score = fields.Float(
        string='Pontuação Calculada',
        compute='_compute_calculated_score',
        store=True
    )

    @api.depends('quantity', 'months', 'num_authors', 'direct_score', 'rubric_item_id')
    def _compute_calculated_score(self):
        for rec in self:
            if rec.rubric_item_id:
                rec.calculated_score = rec.rubric_item_id.calculate_score(
                    quantity=rec.quantity,
                    months=rec.months,
                    num_authors=rec.num_authors,
                    direct_val=rec.direct_score
                )
            else:
                rec.calculated_score = 0.0
