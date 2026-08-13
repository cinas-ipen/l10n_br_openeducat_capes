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
from odoo.exceptions import ValidationError


class CapesPttAuthor(models.Model):
    _name = 'capes.ptt.author'
    _description = 'Coautor e Equipe de Criação do PTT'
    _order = 'author_role, id'

    product_id = fields.Many2one(
        'capes.ptt.product',
        string='Produto Técnico-Tecnológico',
        required=True,
        ondelete='cascade'
    )
    partner_id = fields.Many2one(
        'res.partner',
        string='Coautor (Pessoa)',
        required=True
    )
    author_role = fields.Selection([
        ('main_dev', 'Desenvolvedor Principal / Autor'),
        ('advisor', 'Orientador'),
        ('tech_validator', 'Validador Técnico / Testador'),
        ('funder', 'Patrocinador / Financiador')
    ], string='Papel na Criação', default='main_dev', required=True)

    ip_share = fields.Float(
        string='Quota de Propriedade Intelectual (%)',
        default=0.0,
        help='Percentual de titularidade de patente/PI gerada'
    )

    @api.constrains('ip_share')
    def _check_ip_share(self):
        for record in self:
            if record.ip_share < 0.0 or record.ip_share > 100.0:
                raise ValidationError("A quota de propriedade intelectual deve estar entre 0% e 100%.")
