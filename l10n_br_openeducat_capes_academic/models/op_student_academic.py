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


class OpStudent(models.Model):
    _inherit = 'op.student'

    credit_ledger_ids = fields.One2many(
        'op.student.credit.ledger',
        'student_id',
        string='Histórico do Livro-Razão de Créditos'
    )
    special_request_ids = fields.One2many(
        'op.special.credit.incorporation.request',
        'student_id',
        string='Requerimentos de Aproveitamento'
    )

    credit_ledger_count = fields.Integer(
        string='Lançamentos de Crédito',
        compute='_compute_academic_counts'
    )
    special_req_count = fields.Integer(
        string='Aproveitamentos',
        compute='_compute_academic_counts'
    )

    total_disciplinas_credits = fields.Float(
        string='Créditos em Disciplinas',
        compute='_compute_student_credits'
    )
    total_complementar_credits = fields.Float(
        string='Créditos Complementares',
        compute='_compute_student_credits'
    )
    total_conferred_credits = fields.Float(
        string='Total de Créditos Convalidados',
        compute='_compute_student_credits'
    )

    @api.depends('credit_ledger_ids', 'special_request_ids')
    def _compute_academic_counts(self):
        for record in self:
            record.credit_ledger_count = len(record.credit_ledger_ids)
            record.special_req_count = len(record.special_request_ids)

    @api.depends('credit_ledger_ids.credits', 'credit_ledger_ids.credit_type', 'credit_ledger_ids.is_approved')
    def _compute_student_credits(self):
        for record in self:
            approved = record.credit_ledger_ids.filtered(lambda l: l.is_approved)
            subject_types = (
                'subject',
                'subject_internal',
                'subject_intra_ies',
                'subject_special_incorporated',
                'subject_extra_ies'
            )
            record.total_disciplinas_credits = sum(
                approved.filtered(lambda l: l.credit_type in subject_types).mapped('credits')
            )
            record.total_complementar_credits = sum(
                approved.filtered(lambda l: l.credit_type not in subject_types).mapped('credits')
            )
            record.total_conferred_credits = sum(approved.mapped('credits'))

    def action_view_credit_ledger(self):
        self.ensure_one()
        return {
            'name': f'Livro-Razão de Créditos - {self.name}',
            'type': 'ir.actions.act_window',
            'res_model': 'op.student.credit.ledger',
            'view_mode': 'list,form',
            'domain': [('student_id', '=', self.id)],
            'context': {'default_student_id': self.id},
        }

    def action_view_special_requests(self):
        self.ensure_one()
        return {
            'name': f'Requerimentos de Aproveitamento - {self.name}',
            'type': 'ir.actions.act_window',
            'res_model': 'op.special.credit.incorporation.request',
            'view_mode': 'list,form',
            'domain': [('student_id', '=', self.id)],
            'context': {'default_student_id': self.id},
        }
