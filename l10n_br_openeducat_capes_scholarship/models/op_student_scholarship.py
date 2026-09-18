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


class OpStudent(models.Model):
    """Extensão da Ficha 360° do Discente com Histórico de Bolsas."""
    _inherit = 'op.student'

    scholarship_assignment_ids = fields.One2many(
        'capes.scholarship.assignment',
        'student_id',
        string='Concessões de Bolsa'
    )
    scholarship_application_ids = fields.One2many(
        'capes.scholarship.application',
        'student_id',
        string='Candidaturas em Editais de Bolsa'
    )
    active_scholarship_count = fields.Integer(
        string='Bolsas Ativas',
        compute='_compute_scholarship_info'
    )
    has_active_scholarship = fields.Boolean(
        string='Bolsista Ativo',
        compute='_compute_scholarship_info'
    )
    scholarship_status_badge = fields.Char(
        string='Status de Fomento',
        compute='_compute_scholarship_info'
    )

    @api.depends('scholarship_assignment_ids.state', 'scholarship_assignment_ids.sponsor_id')
    def _compute_scholarship_info(self):
        for rec in self:
            active_assignments = rec.scholarship_assignment_ids.filtered(lambda a: a.state in ('active', 'suspended'))
            rec.active_scholarship_count = len(active_assignments)
            rec.has_active_scholarship = bool(active_assignments)
            if active_assignments:
                sponsors = ', '.join(active_assignments.mapped('sponsor_id.code'))
                rec.scholarship_status_badge = f"Bolsista {sponsors}"
            else:
                rec.scholarship_status_badge = "Sem Bolsa Ativa"

    def action_view_scholarships(self):
        self.ensure_one()
        return {
            'name': 'Bolsas de Estudo do Discente',
            'type': 'ir.actions.act_window',
            'res_model': 'capes.scholarship.assignment',
            'view_mode': 'list,form',
            'domain': [('student_id', '=', self.id)],
            'context': {'default_student_id': self.id},
        }
