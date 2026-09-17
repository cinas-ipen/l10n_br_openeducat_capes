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

    ptt_count = fields.Integer(
        string='PTTs Vinculados / Orientados',
        compute='_compute_ptt_count'
    )

    def _compute_ptt_count(self):
        Author = self.env['capes.ptt.author']
        for record in self:
            if record.partner_id:
                record.ptt_count = Author.search_count([('partner_id', '=', record.partner_id.id)])
            else:
                record.ptt_count = 0

    def action_view_faculty_ptts(self):
        self.ensure_one()
        ptts = self.env['capes.ptt.author'].search([('partner_id', '=', self.partner_id.id)]).mapped('product_id')
        return {
            'name': f'Produtos PTT com Participação - {self.name}',
            'type': 'ir.actions.act_window',
            'res_model': 'capes.ptt.product',
            'view_mode': 'list,form',
            'domain': [('id', 'in', ptts.ids)],
        }
