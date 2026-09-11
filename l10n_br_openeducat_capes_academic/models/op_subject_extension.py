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


class OpSubjectExtension(models.Model):
    _inherit = 'op.subject'

    syllabus = fields.Text(
        string='Ementa da Disciplina',
        help='Apresentação concisa do conteúdo programático da disciplina'
    )
    basic_bibliography = fields.Text(
        string='Bibliografia Básica',
        help='Referências bibliográficas principais da disciplina'
    )
    complementary_bibliography = fields.Text(
        string='Bibliografia Complementar',
        help='Referências bibliográficas complementares (Metadado CAPES DAV 305)'
    )
    phea_indicator = fields.Boolean(
        string='Utiliza PHEA (Processos Híbridos de Ensino)',
        default=False,
        help='Indicação de utilização de Processos Híbridos de Ensino e Aprendizagem (CAPES DAV)'
    )
    teaching_language = fields.Selection([
        ('pt', 'Português'),
        ('en', 'Inglês'),
        ('es', 'Espanhol'),
        ('other', 'Outro')
    ], string='Idioma de Oferta', default='pt')
