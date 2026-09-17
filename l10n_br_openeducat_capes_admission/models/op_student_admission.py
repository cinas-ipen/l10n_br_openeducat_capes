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

    work_plan_ids = fields.One2many(
        'op.student.work_plan',
        'student_id',
        string='Planos de Trabalho Discente'
    )
    work_plan_count = fields.Integer(
        string='Planos de Trabalho',
        compute='_compute_work_plan_count'
    )

    @api.depends('work_plan_ids')
    def _compute_work_plan_count(self):
        for record in self:
            record.work_plan_count = len(record.work_plan_ids)

    def action_view_work_plans(self):
        self.ensure_one()
        return {
            'name': f'Planos de Trabalho - {self.name}',
            'type': 'ir.actions.act_window',
            'res_model': 'op.student.work_plan',
            'view_mode': 'list,form',
            'domain': [('student_id', '=', self.id)],
            'context': {'default_student_id': self.id},
        }
