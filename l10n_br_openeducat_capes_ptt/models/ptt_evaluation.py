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
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class CapesPttEvaluation(models.Model):
    _name = 'capes.ptt.evaluation'
    _description = 'Avaliação Qualis Tecnológico de PTT'
    _order = 'total_score desc, id desc'

    product_id = fields.Many2one(
        'capes.ptt.product',
        string='Produto Avaliado',
        required=True,
        ondelete='cascade'
    )
    evaluator_id = fields.Many2one(
        'res.partner',
        string='Avaliador (Docente / Perito Externo)',
        required=True
    )
    evaluation_date = fields.Date(
        string='Data da Avaliação',
        required=True,
        default=fields.Date.context_today
    )

    # 4 Dimensões Ponderadas do Baremo CAPES
    dim_impact = fields.Float(
        string='Demanda e Impacto (0 a 30 pts)',
        default=0.0,
        help='Avalia a indução e alcance social/econômico (máx: 30 pts)'
    )
    dim_innovation = fields.Float(
        string='Inovação e Originalidade (0 a 25 pts)',
        default=0.0,
        help='Novidade técnica cruzada com nível de maturidade TRL (máx: 25 pts)'
    )
    dim_applicability = fields.Float(
        string='Aplicabilidade e Replicabilidade (0 a 25 pts)',
        default=0.0,
        help='Facilidade de adoção do produto por terceiros (máx: 25 pts)'
    )
    dim_complexity = fields.Float(
        string='Complexidade Técnica (0 a 20 pts)',
        default=0.0,
        help='Exigência de infraestrutura e multidisciplinaridade (máx: 20 pts)'
    )

    total_score = fields.Float(
        string='Pontuação Total Calculada',
        compute='_compute_final_stratum',
        store=True,
        help='Soma das 4 dimensões ponderadas (máximo: 100 pontos)'
    )
    final_stratum = fields.Selection([
        ('T1', 'T1 - Excelente (90-100 pts)'),
        ('T2', 'T2 - Muito Bom (75-89 pts)'),
        ('T3', 'T3 - Bom (60-74 pts)'),
        ('T4', 'T4 - Regular (45-59 pts)'),
        ('T5', 'T5 - Fraco (30-44 pts)'),
        ('TNC', 'TNC - Produto Não Classificado (<30 pts ou Não Aderente)')
    ], string='Estrato Final Calculado', compute='_compute_final_stratum', store=True)

    notes = fields.Text(
        string='Parecer Consubstanciado do Avaliador'
    )

    @api.depends('dim_impact', 'dim_innovation', 'dim_applicability', 'dim_complexity', 'product_id.is_adherent')
    def _compute_final_stratum(self):
        for record in self:
            # Trava Lógica de Aderência: O requisito primário
            if not record.product_id or not record.product_id.is_adherent:
                record.total_score = 0.0
                record.final_stratum = 'TNC'
                continue

            score = sum([record.dim_impact, record.dim_innovation, record.dim_applicability, record.dim_complexity])
            record.total_score = score

            # Classificação por Corte Paramétrico do Baremo CAPES
            if score >= 90.0:
                record.final_stratum = 'T1'
            elif score >= 75.0:
                record.final_stratum = 'T2'
            elif score >= 60.0:
                record.final_stratum = 'T3'
            elif score >= 45.0:
                record.final_stratum = 'T4'
            elif score >= 30.0:
                record.final_stratum = 'T5'
            else:
                record.final_stratum = 'TNC'

    @api.constrains('dim_impact', 'dim_innovation', 'dim_applicability', 'dim_complexity')
    def _check_dimension_limits(self):
        for record in self:
            if record.dim_impact < 0 or record.dim_impact > 30:
                raise ValidationError("A dimensão Demanda e Impacto deve estar entre 0 e 30 pontos.")
            if record.dim_innovation < 0 or record.dim_innovation > 25:
                raise ValidationError("A dimensão Inovação e Originalidade deve estar entre 0 e 25 pontos.")
            if record.dim_applicability < 0 or record.dim_applicability > 25:
                raise ValidationError("A dimensão Aplicabilidade e Replicabilidade deve estar entre 0 e 25 pontos.")
            if record.dim_complexity < 0 or record.dim_complexity > 20:
                raise ValidationError("A dimensão Complexidade Técnica deve estar entre 0 e 20 pontos.")
