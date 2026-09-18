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

from odoo import models


class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    def session_info(self):
        result = super().session_info()
        user = self.env.user
        if user and not user._is_public():
            is_admin = (
                user.is_central_admin
                or user.has_group('l10n_br_openeducat_capes_core.group_capes_central_admin')
            )
            programs = user.allowed_program_ids
            if is_admin:
                programs = self.env['op.program.capes'].search([])

            current_prog = user.current_program_id
            if not current_prog and programs:
                current_prog = programs[0]
                user.sudo().write({'current_program_id': current_prog.id})

            result['current_program'] = {
                'id': current_prog.id,
                'name': current_prog.name,
                'short_name': current_prog.short_name or current_prog.name,
            } if current_prog else False

            result['allowed_programs'] = [
                {
                    'id': p.id,
                    'name': p.name,
                    'short_name': p.short_name or p.name,
                }
                for p in programs
            ]
            result['is_central_admin'] = is_admin
        return result
