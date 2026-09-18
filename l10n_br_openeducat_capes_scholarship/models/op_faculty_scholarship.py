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


class OpFaculty(models.Model):
    """Extensão da Ficha do Docente com Pareceres de Editais de Bolsas."""
    _inherit = 'op.faculty'

    scholarship_evaluation_ids = fields.One2many(
        'capes.scholarship.evaluation',
        'evaluator_id',
        string='Avaliações de Bolsas Atribuídas'
    )
    assigned_scholarship_reviews_count = fields.Integer(
        string='Pareceres de Bolsas',
        compute='_compute_scholarship_reviews'
    )

    @api.depends('scholarship_evaluation_ids.state')
    def _compute_scholarship_reviews(self):
        for rec in self:
            rec.assigned_scholarship_reviews_count = len(rec.scholarship_evaluation_ids)

    def action_view_assigned_scholarship_reviews(self):
        self.ensure_one()
        return {
            'name': 'Avaliações de Bolsas Designadas',
            'type': 'ir.actions.act_window',
            'res_model': 'capes.scholarship.evaluation',
            'view_mode': 'list,form',
            'domain': [('evaluator_id', '=', self.id)],
            'context': {'default_evaluator_id': self.id},
        }
