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

from odoo import models, fields


class CapesPttAxis(models.Model):
    _name = 'capes.ptt.axis'
    _description = 'Eixo Estruturante de Produto Técnico-Tecnológico (GTPT/CAPES)'
    _order = 'code, name'

    code = fields.Char(
        string='Código do Eixo',
        required=True,
        help='Ex: E1, E2, E3, E4'
    )
    name = fields.Char(
        string='Nome do Eixo Estruturante',
        required=True
    )
    description = fields.Text(
        string='Descrição Normativa da Diretriz CAPES'
    )

    _sql_constraints = [
        ('code_unique', 'unique(code)', 'O código do Eixo Estruturante deve ser único.')
    ]


class CapesPttType(models.Model):
    _name = 'capes.ptt.type'
    _description = 'Tipologia / Subcategoria de PTT (GTPT / Medicina II)'
    _order = 'axis_id, code, name'

    axis_id = fields.Many2one(
        'capes.ptt.axis',
        string='Eixo Estruturante Vinculado',
        required=True,
        ondelete='cascade'
    )
    code = fields.Char(
        string='Código da Tipologia',
        required=True,
        help='Ex: T13, T19, T08'
    )
    name = fields.Char(
        string='Nome do Tipo de Produto',
        required=True
    )
    req_ip = fields.Boolean(
        string='Exige Propriedade Intelectual (INPI / Registro)',
        default=False,
        help='Se True, exige o anexo do comprovante de depósito ou registro oficial'
    )

    _sql_constraints = [
        ('code_unique', 'unique(code)', 'O código da tipologia PTT deve ser único.')
    ]
