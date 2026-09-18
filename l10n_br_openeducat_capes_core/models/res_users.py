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

from odoo import models, fields, api, _
from odoo.exceptions import AccessError


class ResUsers(models.Model):
    _inherit = 'res.users'

    allowed_program_ids = fields.Many2many(
        'op.program.capes',
        'res_users_program_capes_rel',
        'user_id',
        'program_id',
        string='Programas Autorizados',
        help='Programas de pós-graduação aos quais o usuário tem permissão de acesso.'
    )
    current_program_id = fields.Many2one(
        'op.program.capes',
        string='Programa Ativo',
        help='Programa de pós-graduação atualmente ativo na sessão de trabalho.'
    )
    is_central_admin = fields.Boolean(
        string='Administrador Central',
        default=False,
        help='Usuário com privilégios centrais da Pró-Reitoria de Pós-Graduação, com visão global irrestrita.'
    )

    @api.model
    def action_switch_program(self, program_id):
        """Alterna o programa ativo na sessão do usuário atual."""
        user = self.env.user
        is_admin = (
            user.is_central_admin
            or user.has_group('l10n_br_openeducat_capes_core.group_capes_central_admin')
        )
        prog_id = int(program_id) if program_id else False
        allowed_ids = user.sudo().allowed_program_ids.ids

        if not is_admin and prog_id not in allowed_ids:
            raise AccessError(_("Você não possui permissão para acessar o programa selecionado."))

        user.sudo().write({'current_program_id': prog_id})
        self.env.registry.clear_cache()
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

