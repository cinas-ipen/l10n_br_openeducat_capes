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


class CapesProjectMember(models.Model):
    _name = 'capes.project.member'
    _description = 'Membro de Projeto de Pesquisa e Taxonomia CRediT'
    _order = 'link_start desc, id'

    project_id = fields.Many2one(
        'capes.research.project',
        string='Projeto de Pesquisa',
        required=True,
        ondelete='cascade'
    )
    partner_id = fields.Many2one(
        'res.partner',
        string='Pesquisador / Membro (Pessoa)',
        required=True
    )
    faculty_id = fields.Many2one(
        'op.faculty',
        string='Docente (se aplicável)',
        help='Vínculo direto se o membro for docente credenciado da instituição'
    )
    student_id = fields.Many2one(
        'op.student',
        string='Discente (se aplicável)',
        help='Vínculo direto se o membro for estudante de pós-graduação'
    )

    role = fields.Selection([
        ('coordinator', 'Coordenador Principal'),
        ('vice_coordinator', 'Vice-Coordenador'),
        ('researcher', 'Pesquisador / Docente'),
        ('student_researcher', 'Pesquisador Discente'),
        ('external_collaborator', 'Colaborador Externo')
    ], string='Função no Projeto', default='researcher', required=True)

    # Taxonomia CRediT (Contributor Roles Taxonomy)
    contrib_type = fields.Selection([
        ('conceptualization', 'Conceitualização (Conceptualization)'),
        ('methodology', 'Metodologia (Methodology)'),
        ('software', 'Desenvolvimento de Software (Software)'),
        ('validation', 'Validação (Validation)'),
        ('formal_analysis', 'Análise Formal (Formal Analysis)'),
        ('investigation', 'Investigação e Coleta (Investigation)'),
        ('resources', 'Recursos e Infraestrutura (Resources)'),
        ('data_curation', 'Curadoria de Dados (Data Curation)'),
        ('writing_original', 'Escrita - Redação Original (Writing - Original Draft)'),
        ('writing_review', 'Escrita - Revisão e Edição (Writing - Review & Editing)'),
        ('visualization', 'Visualização e Grafismo (Visualization)'),
        ('supervision', 'Supervisão e Orientação (Supervision)'),
        ('project_admin', 'Administração do Projeto (Project Administration)'),
        ('funding_acquisition', 'Captação de Recursos (Funding Acquisition)')
    ], string='Tipo de Contribuição (Taxonomia CRediT)', required=True, default='investigation',
       help='Classificação oficial da contribuição científica conforme o padrão CRediT')

    link_start = fields.Date(
        string='Início do Vínculo',
        required=True,
        default=fields.Date.context_today
    )
    link_end = fields.Date(
        string='Encerramento do Vínculo'
    )

    area_name = fields.Char(
        string='Área de Concentração do PPG',
        help='Área de concentração do PPG associada à atuação do membro'
    )
    research_line = fields.Char(
        string='Linha de Pesquisa do PPG',
        help='Linha de pesquisa do PPG vinculada à contribuição'
    )

    @api.constrains('link_start', 'link_end')
    def _check_member_dates(self):
        for record in self:
            if record.link_start and record.link_end and record.link_end < record.link_start:
                raise ValidationError("A data de encerramento do vínculo do membro deve ser posterior à data de início.")
