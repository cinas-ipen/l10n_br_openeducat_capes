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


class OpStudent(models.Model):
    _inherit = 'op.student'

    student_category = fields.Selection([
        ('regular', 'Regular'),
        ('special', 'Especial / Não-Vinculado')
    ], string='Categoria Discente', default='regular')

    curriculum_version_id = fields.Many2one(
        'op.curriculum.version',
        string='Versão Regimental (Ato Jurídico Perfeito)',
        help='Regimento ao qual o estudante foi vinculado no momento do ingresso'
    )
    capes_status = fields.Selection([
        ('enrolled', 'Matriculado'),
        ('abandon', 'Abandono'),
        ('dismissed', 'Desligado'),
        ('pending_dismissal', 'Desligamento Em Andamento'),
        ('graduated', 'Titulado'),
        ('deceased', 'Falecido')
    ], string='Situação Discente CAPES', default='enrolled')

    admission_date = fields.Date(
        string='Data de Ingresso Oficial',
        required=True,
        default=fields.Date.context_today,
        help='Data de efetivação da primeira matrícula regular'
    )
    status_date = fields.Date(
        string='Data da Situação',
        default=fields.Date.context_today,
        help='Data da última alteração de status do discente'
    )

    advisor_id = fields.Many2one(
        'op.faculty',
        string='Orientador Principal',
        help='Docente credenciado atuando como orientador principal'
    )
    coadvisor_id = fields.Many2one(
        'op.faculty',
        string='Coorientador',
        help='Docente credenciado atuando como coorientador'
    )

    # Controle de Proficiência Linguística (GoPG / DAV)
    english_proficiency_status = fields.Selection([
        ('pending', 'Pendente'),
        ('approved', 'Aprovado'),
        ('exempt', 'Isento')
    ], string='Proficiência em Inglês', default='pending', required=True)

    portuguese_proficiency_status = fields.Selection([
        ('not_applicable', 'Não Aplicável'),
        ('pending', 'Pendente'),
        ('approved', 'Aprovado')
    ], string='Proficiência em Português (Estrangeiros)', default='not_applicable', required=True)

    @api.constrains('advisor_id', 'coadvisor_id')
    def _check_advisor_coadvisor(self):
        for record in self:
            if record.advisor_id and record.coadvisor_id and record.advisor_id == record.coadvisor_id:
                raise ValidationError("O orientador principal e o coorientador não podem ser a mesma pessoa.")
