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


class OpFaculty(models.Model):
    _inherit = 'op.faculty'

    work_regime = fields.Selection([
        ('exclusive', 'Dedicação Exclusiva (DE)'),
        ('fulltime', 'Tempo Integral (40h)'),
        ('parttime', 'Tempo Parcial (<40h)')
    ], string='Regime de Dedicação', default='fulltime')

    workload = fields.Integer(
        string='Carga Horária Semanal (horas)',
        default=40,
        help='Carga horária semanal dedicada à instituição'
    )
    faculty_status = fields.Selection([
        ('active', 'Ativo'),
        ('inactive', 'Inativo'),
        ('deceased', 'Falecido')
    ], string='Situação Docente', default='active')

    is_retired = fields.Boolean(
        string='Indicação de Aposentadoria',
        default=False
    )
    degree_area = fields.Char(
        string='Área de Conhecimento da Titulação',
        help='Área do conhecimento da maior titulação'
    )
    degree_level = fields.Selection([
        ('master', 'Mestrado'),
        ('phd', 'Doutorado')
    ], string='Nível Acadêmico da Titulação Máxima', default='phd')

    degree_ies = fields.Char(
        string='IES da Titulação',
        help='Instituição onde obteve o título máximo'
    )

    @api.constrains('workload')
    def _check_workload(self):
        for record in self:
            if record.workload < 0:
                raise ValidationError("A carga horária semanal do docente não pode ser negativa.")
