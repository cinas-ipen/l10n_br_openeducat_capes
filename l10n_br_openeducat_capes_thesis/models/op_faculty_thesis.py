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

    committee_count = fields.Integer(
        string='Comissões Examinadoras / Bancas',
        compute='_compute_committee_count'
    )

    def _compute_committee_count(self):
        Committee = self.env['capes.thesis.committee']
        for record in self:
            if record.partner_id:
                record.committee_count = Committee.search_count([('member_id', '=', record.partner_id.id)])
            else:
                record.committee_count = 0

    def action_view_committees(self):
        self.ensure_one()
        theses = self.env['capes.thesis.committee'].search([('member_id', '=', self.partner_id.id)]).mapped('thesis_id')
        return {
            'name': f'Bancas e Comissões Examinadoras - {self.name}',
            'type': 'ir.actions.act_window',
            'res_model': 'capes.thesis',
            'view_mode': 'list,form',
            'domain': [('id', 'in', theses.ids)],
        }
