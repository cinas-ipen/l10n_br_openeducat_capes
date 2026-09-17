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

    ptt_ids = fields.One2many(
        'capes.ptt.product',
        'student_id',
        string='Produtos Técnicos e Tecnológicos (PTT)'
    )
    ptt_count = fields.Integer(
        string='Produtos PTT',
        compute='_compute_ptt_count'
    )

    @api.depends('ptt_ids')
    def _compute_ptt_count(self):
        for record in self:
            record.ptt_count = len(record.ptt_ids)

    def action_view_ptts(self):
        self.ensure_one()
        return {
            'name': f'Produtos Técnicos e Tecnológicos - {self.name}',
            'type': 'ir.actions.act_window',
            'res_model': 'capes.ptt.product',
            'view_mode': 'list,form',
            'domain': [('student_id', '=', self.id)],
            'context': {'default_student_id': self.id},
        }
