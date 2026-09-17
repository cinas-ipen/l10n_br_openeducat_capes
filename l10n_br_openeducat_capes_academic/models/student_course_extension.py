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


class OpStudentCourseExtension(models.Model):
    _inherit = 'op.student.course'

    course_type = fields.Selection([
        ('regular', 'Curso Regular (Stricto Sensu)'),
        ('special', 'Aluno Especial (Disciplinas Isoladas)')
    ], string='Tipo de Vínculo', default='regular', required=True)

    program_id = fields.Many2one(
        'op.program.capes',
        string='Programa de Pós-Graduação',
        help='Programa acadêmico CAPES vinculado a este percurso formativo'
    )
    curriculum_version_id = fields.Many2one(
        'op.curriculum.version',
        string='Versão Curricular do Vínculo',
        help='Regimento específico que rege este vínculo discente'
    )
    admission_date = fields.Date(
        string='Data de Início do Vínculo',
        default=fields.Date.context_today
    )
    completion_date = fields.Date(
        string='Data de Conclusão / Encerramento do Vínculo'
    )
