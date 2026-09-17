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


class OpFaculty(models.Model):
    _inherit = 'op.faculty'

    program_link_ids = fields.One2many(
        'op.faculty.program.link',
        'faculty_id',
        string='Credenciamentos CPG nos Programas'
    )
    accreditation_count = fields.Integer(
        string='Credenciamentos CPG',
        compute='_compute_accreditation_count'
    )

    @api.depends('program_link_ids')
    def _compute_accreditation_count(self):
        for record in self:
            record.accreditation_count = len(record.program_link_ids)

    def action_view_accreditations(self):
        self.ensure_one()
        return {
            'name': f'Credenciamentos CPG - {self.name}',
            'type': 'ir.actions.act_window',
            'res_model': 'op.faculty.program.link',
            'view_mode': 'list,form',
            'domain': [('faculty_id', '=', self.id)],
            'context': {'default_faculty_id': self.id},
        }
