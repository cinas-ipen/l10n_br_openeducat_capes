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

    thesis_ids = fields.One2many(
        'capes.thesis',
        'student_id',
        string='Trabalhos de Conclusão / Ritos Acadêmicos'
    )
    thesis_count = fields.Integer(
        string='Ritos / Defesas',
        compute='_compute_thesis_count'
    )

    @api.depends('thesis_ids')
    def _compute_thesis_count(self):
        for record in self:
            record.thesis_count = len(record.thesis_ids)

    def action_view_theses(self):
        self.ensure_one()
        return {
            'name': f'Trabalhos de Conclusão e Ritos - {self.name}',
            'type': 'ir.actions.act_window',
            'res_model': 'capes.thesis',
            'view_mode': 'list,form',
            'domain': [('student_id', '=', self.id)],
            'context': {'default_student_id': self.id},
        }
