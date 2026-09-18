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


class OpProgramCapes(models.Model):
    _name = 'op.program.capes'
    _description = 'Programa de Pós-Graduação (CAPES/SNPG)'
    _order = 'snpg_code, name'

    capes_id = fields.Integer(
        string='Identificador CAPES',
        help='Identificador numérico do programa na CAPES / Sucupira'
    )
    snpg_code = fields.Char(
        string='Código SNPG',
        required=True,
        help='Código único no Sistema Nacional de Pós-Graduação (ex: 33002010001P0)'
    )
    name = fields.Char(
        string='Nome do Programa',
        required=True,
        help='Nome oficial do PPG cadastrado na CAPES'
    )
    short_name = fields.Char(
        string='Sigla do Programa',
        help='Sigla usual do PPG (ex: MPTRCS, PPGCC)'
    )
    lang = fields.Selection([
        ('pt', 'Português'),
        ('en', 'Inglês'),
        ('es', 'Espanhol')
    ], string='Idioma do Nome', default='pt')

    phone = fields.Char(
        string='Telefone do PPG'
    )
    website = fields.Char(
        string='Website do PPG'
    )
    modality = fields.Selection([
        ('academic', 'Acadêmica'),
        ('professional', 'Profissional')
    ], string='Modalidade do Programa', required=True, default='academic')

    teaching_modal = fields.Selection([
        ('onsite', 'Ensino Presencial'),
        ('distance', 'Ensino a Distância')
    ], string='Modalidade de Ensino', default='onsite')

    operation_form = fields.Selection([
        ('singular', 'Singular'),
        ('assoc_inter', 'Associação Interinstitucional'),
        ('assoc_intra', 'Associação Intrainstitucional')
    ], string='Forma de Atuação', default='singular')

    ies_role = fields.Selection([
        ('coordinator', 'Coordenadora'),
        ('associate', 'Associada'),
        ('nucleating', 'Nucleadora'),
        ('collaborator', 'Colaboradora')
    ], string='Atuação da IES / Campus', default='coordinator')

    school_term = fields.Selection([
        ('bimonthly', 'Bimestral'),
        ('trimonthly', 'Trimestral'),
        ('quadrimonthly', 'Quadrimestral'),
        ('semestral', 'Semestral'),
        ('annual', 'Anual')
    ], string='Regime Letivo do Programa', default='semestral')

    status = fields.Selection([
        ('project', 'Em Projeto'),
        ('active', 'Em Funcionamento'),
        ('deactivating', 'Em Desativação'),
        ('deactivated', 'Desativado'),
        ('loss_efficacy', 'Perda de Eficácia'),
        ('suspended', 'Suspensão')
    ], string='Situação do Programa', default='active')

    start_date = fields.Date(
        string='Data de Início do Programa'
    )
    end_date = fields.Date(
        string='Data de Encerramento'
    )
    recommend_date = fields.Date(
        string='Data de Recomendação CAPES'
    )
    recognize_date = fields.Date(
        string='Data de Reconhecimento MEC'
    )

    company_id = fields.Many2one(
        'res.company',
        string='IES / Campus Sede',
        default=lambda self: self.env.company,
        required=True
    )
    general_coord_id = fields.Many2one(
        'op.faculty',
        string='Coordenador Geral do PPG'
    )
    local_coord_id = fields.Many2one(
        'op.faculty',
        string='Coordenador Local do PPG'
    )

    # Classificação e Áreas de Avaliação CAPES
    evaluation_area = fields.Char(
        string='Área de Avaliação CAPES',
        help='Ex: Medicina II, Engenharia I, Computação'
    )
    broad_area = fields.Char(
        string='Grande Área (Nível 1)'
    )
    basic_area = fields.Char(
        string='Área Básica (Nível 2)'
    )
    subarea = fields.Char(
        string='Subárea (Nível 3)'
    )
    specialty = fields.Char(
        string='Especialidade (Nível 4)'
    )
    capes_grade = fields.Selection([
        ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'),
        ('5', '5'), ('6', '6'), ('7', '7'), ('A', 'A')
    ], string='Nota CAPES')

    grade_year = fields.Integer(
        string='Ano Base Atribuição da Nota'
    )

    is_current_program = fields.Boolean(
        string='Programa Ativo na Sessão',
        compute='_compute_is_current_program',
        search='_search_is_current_program'
    )
    can_switch_to_program = fields.Boolean(
        string='Pode Alternar para este Programa',
        compute='_compute_can_switch_to_program'
    )
    session_status = fields.Char(
        string='Sessão',
        compute='_compute_is_current_program'
    )

    def _search_is_current_program(self, operator, value):
        current_id = self.env.user.current_program_id.id
        if (operator == '=' and value) or (operator == '!=' and not value):
            return [('id', '=', current_id)] if current_id else [('id', '=', -1)]
        return [('id', '!=', current_id)] if current_id else [(1, '=', 1)]

    def _compute_is_current_program(self):
        current_id = self.env.user.current_program_id.id
        for record in self:
            is_cur = (record.id == current_id)
            record.is_current_program = is_cur
            record.session_status = 'Programa Ativo' if is_cur else 'Disponível'

    def _compute_can_switch_to_program(self):
        user = self.env.user
        is_admin = (
            user.is_central_admin
            or user.has_group('l10n_br_openeducat_capes_core.group_capes_central_admin')
        )
        allowed_ids = user.allowed_program_ids.ids
        for record in self:
            record.can_switch_to_program = is_admin or (record.id in allowed_ids)

    def action_select_as_current(self):
        """Define este programa como o programa ativo na sessão do usuário."""
        self.ensure_one()
        self.env['res.users'].action_switch_program(self.id)
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

    _sql_constraints = [
        ('snpg_code_unique', 'unique(snpg_code)', 'O Código SNPG do Programa de Pós-Graduação deve ser único.')
    ]

    @api.constrains('start_date', 'end_date')
    def _check_program_dates(self):
        for record in self:
            if record.start_date and record.end_date:
                if record.end_date < record.start_date:
                    raise ValidationError("A data de encerramento do programa deve ser posterior à data de início.")
