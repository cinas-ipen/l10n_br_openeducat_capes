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


class OpProgramConcentrationArea(models.Model):
    _name = 'op.program.concentration.area'
    _description = 'Área de Concentração do Programa de Pós-Graduação'
    _order = 'program_id, name'

    name = fields.Char(
        string='Nome da Área de Concentração',
        required=True,
        help='Denominação oficial da área de concentração do PPG'
    )
    code = fields.Char(
        string='Código / Sigla',
        help='Identificador curto da área de concentração'
    )
    program_id = fields.Many2one(
        'op.program.capes',
        string='Programa de Pós-Graduação',
        required=True,
        ondelete='cascade',
        index=True
    )
    description = fields.Text(
        string='Descrição e Escopo Temático'
    )
    research_line_ids = fields.One2many(
        'op.program.research.line',
        'area_id',
        string='Linhas de Pesquisa'
    )
    faculty_ids = fields.Many2many(
        'op.faculty',
        'op_area_faculty_rel',
        'area_id',
        'faculty_id',
        string='Docentes Credenciados na Área'
    )
    faculty_count = fields.Integer(
        string='Docentes',
        compute='_compute_counts'
    )
    research_line_count = fields.Integer(
        string='Qtd. Linhas de Pesquisa',
        compute='_compute_counts'
    )
    active = fields.Boolean(default=True)

    @api.depends('faculty_ids', 'research_line_ids')
    def _compute_counts(self):
        for record in self:
            record.faculty_count = len(record.faculty_ids)
            record.research_line_count = len(record.research_line_ids)


class OpProgramResearchLine(models.Model):
    _name = 'op.program.research.line'
    _description = 'Linha de Pesquisa do Programa de Pós-Graduação'
    _order = 'area_id, name'

    name = fields.Char(
        string='Nome da Linha de Pesquisa',
        required=True,
        help='Denominação oficial da linha de pesquisa'
    )
    code = fields.Char(
        string='Código / Sigla',
        help='Código ou sigla identificadora da linha de pesquisa'
    )
    area_id = fields.Many2one(
        'op.program.concentration.area',
        string='Área de Concentração',
        required=True,
        ondelete='cascade',
        index=True
    )
    program_id = fields.Many2one(
        'op.program.capes',
        string='Programa de Pós-Graduação',
        related='area_id.program_id',
        store=True,
        readonly=True,
        index=True
    )
    description = fields.Text(
        string='Descrição e Objetivos de Investigação'
    )
    faculty_ids = fields.Many2many(
        'op.faculty',
        'op_line_faculty_rel',
        'line_id',
        'faculty_id',
        string='Docentes Atuantes na Linha'
    )
    faculty_count = fields.Integer(
        string='Docentes Atuantes',
        compute='_compute_counts'
    )
    active = fields.Boolean(default=True)

    @api.depends('faculty_ids')
    def _compute_counts(self):
        for record in self:
            record.faculty_count = len(record.faculty_ids)
