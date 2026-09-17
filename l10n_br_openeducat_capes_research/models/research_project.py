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


class CapesResearchProject(models.Model):
    _name = 'capes.research.project'
    _description = 'Projeto de Pesquisa Científica (CAPES / Fomento)'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'start_date desc, name'

    capes_id = fields.Integer(
        string='Identificador CAPES',
        help='ID do projeto de pesquisa no cadastro da CAPES / Sucupira'
    )
    name = fields.Char(
        string='Nome do Projeto de Pesquisa',
        required=True,
        tracking=True,
        help='Título oficial do projeto de pesquisa'
    )
    description = fields.Text(
        string='Descrição e Objetivos',
        help='Resumo descritivo e objetivos científicos da investigação'
    )
    project_type = fields.Selection([
        ('scientific', 'Científica'),
        ('extension', 'Extensão'),
        ('innovation', 'Inovação'),
        ('teaching', 'Ensino')
    ], string='Tipo de Projeto', required=True, default='scientific', tracking=True)

    research_nature = fields.Selection([
        ('basic', 'Pesquisa Básica'),
        ('applied', 'Pesquisa Aplicada')
    ], string='Natureza da Pesquisa', required=True, default='applied', tracking=True)

    is_cooperation = fields.Boolean(
        string='Projeto em Cooperação Interinstitucional',
        default=False,
        tracking=True,
        help='Indica se o projeto envolve parceria com IES ou centros de pesquisa externos'
    )
    foreign_ies = fields.Char(
        string='Nome da IES / Instituição Estrangeira',
        help='Denominação da instituição estrangeira parceira'
    )
    foreign_country_id = fields.Many2one(
        'res.country',
        string='País da IES Estrangeira'
    )

    funding_agency = fields.Char(
        string='Agência / Órgão de Fomento',
        help='Ex: CNPq, CAPES, FAPESP, FINEP, IAEA'
    )
    funding_process = fields.Char(
        string='Número do Processo de Fomento / Grant',
        help='Número do processo de concessão de auxílio à pesquisa'
    )

    status = fields.Selection([
        ('ongoing', 'Em Andamento'),
        ('completed', 'Concluído'),
        ('suspended', 'Suspenso'),
        ('cancelled', 'Cancelado')
    ], string='Situação do Projeto', default='ongoing', required=True, tracking=True)

    status_date = fields.Date(
        string='Data da Situação',
        default=fields.Date.context_today
    )
    start_date = fields.Date(
        string='Data de Início do Projeto',
        required=True,
        default=fields.Date.context_today
    )
    end_date = fields.Date(
        string='Data de Encerramento'
    )

    program_id = fields.Many2one(
        'op.program.capes',
        string='Programa de Pós-Graduação (PPG)',
        required=True,
        tracking=True
    )
    research_line_id = fields.Many2one(
        'op.program.research.line',
        string='Linha de Pesquisa',
        help='Linha de pesquisa oficial do PPG à qual o projeto se vincula'
    )
    coordinator_id = fields.Many2one(
        'op.faculty',
        string='Coordenador do Projeto',
        required=True,
        tracking=True
    )
    odoo_project_id = fields.Many2one(
        'project.project',
        string='Projeto Odoo (Task Board)',
        help='Vínculo com o módulo nativo de projetos do Odoo para acompanhamento de tarefas'
    )

    member_ids = fields.One2many(
        'capes.project.member',
        'project_id',
        string='Equipe de Pesquisadores / Membros'
    )

    @api.constrains('start_date', 'end_date')
    def _check_project_dates(self):
        for record in self:
            if record.start_date and record.end_date and record.end_date < record.start_date:
                raise ValidationError("A data de encerramento do projeto de pesquisa deve ser posterior à data de início.")
