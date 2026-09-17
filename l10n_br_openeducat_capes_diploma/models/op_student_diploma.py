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

    diploma_ids = fields.One2many(
        'capes.digital.diploma',
        'student_id',
        string='Diplomas Digitais Homologados (MEC)'
    )
    diploma_count = fields.Integer(
        string='Diplomas Digitais',
        compute='_compute_diploma_count'
    )

    @api.depends('diploma_ids')
    def _compute_diploma_count(self):
        for record in self:
            record.diploma_count = len(record.diploma_ids)

    def action_view_diplomas(self):
        self.ensure_one()
        return {
            'name': f'Diplomas Digitais MEC - {self.name}',
            'type': 'ir.actions.act_window',
            'res_model': 'capes.digital.diploma',
            'view_mode': 'list,form',
            'domain': [('student_id', '=', self.id)],
            'context': {'default_student_id': self.id},
        }

    def action_print_transcript(self):
        self.ensure_one()
        report = self.env.ref('l10n_br_openeducat_capes_diploma.action_report_student_transcript_br', raise_if_not_found=False)
        if report:
            return report.report_action(self)
        return False
