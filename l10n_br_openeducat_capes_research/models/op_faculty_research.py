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

    project_ids = fields.One2many(
        'capes.research.project',
        'coordinator_id',
        string='Projetos de Pesquisa Coordenados'
    )
    project_count = fields.Integer(
        string='Projetos de Pesquisa',
        compute='_compute_project_count'
    )

    @api.depends('project_ids')
    def _compute_project_count(self):
        for record in self:
            record.project_count = len(record.project_ids)

    def action_view_projects(self):
        self.ensure_one()
        return {
            'name': f'Projetos de Pesquisa - {self.name}',
            'type': 'ir.actions.act_window',
            'res_model': 'capes.research.project',
            'view_mode': 'list,form',
            'domain': [('coordinator_id', '=', self.id)],
            'context': {'default_coordinator_id': self.id},
        }
