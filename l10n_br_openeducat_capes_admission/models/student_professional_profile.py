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


class CapesStudentProfessionalProfile(models.Model):
    _name = 'capes.student.professional.profile'
    _description = 'Perfil Profissional e Declaração de Impacto (Baseline de Egressos - CAPES)'
    _order = 'acceptance_timestamp desc, id desc'

    student_id = fields.Many2one(
        'op.student',
        string='Discente',
        required=True,
        ondelete='cascade',
        index=True
    )
    company_name = fields.Char(
        string='Nome da Empresa / Empregador',
        required=True,
        help='Nome empresarial da organização empregadora'
    )
    company_city = fields.Char(
        string='Cidade da Empresa',
        help='Município da sede ou filial onde o aluno atua'
    )
    company_sector = fields.Selection([
        ('tech', 'Tecnologia, Inovação e P&D'),
        ('health', 'Saúde e Biotecnologia'),
        ('industry', 'Indústria e Manufatura'),
        ('gov', 'Setor Público / Órgão Regulador'),
        ('education', 'Educação e Pesquisa'),
        ('services', 'Serviços Especializados')
    ], string='Setor de Atuação da Empresa', required=True)

    company_size = fields.Selection([
        ('micro', 'Microempresa (Até 19 funcionários)'),
        ('small', 'Pequena (20 a 99 funcionários)'),
        ('medium', 'Média (100 a 499 funcionários)'),
        ('large', 'Grande (500 a 999 funcionários)'),
        ('enterprise', 'Corporação (Mais de 1.000 funcionários)')
    ], string='Porte da Empresa', required=True)

    current_role = fields.Char(
        string='Cargo / Função Exercida',
        required=True
    )
    professional_area = fields.Char(
        string='Área de Lotação / Departamento'
    )
    mp_alignment = fields.Selection([
        ('yes', 'Sim, Alinhamento Estratégico Direto'),
        ('partial', 'Parcialmente Alinhado'),
        ('no', 'Não Alinhado / Transição de Carreira')
    ], string='Alinhamento com o Mestrado Profissional', required=True, default='yes')

    tenure_range = fields.Selection([
        ('lt_1', 'Menos de 1 ano'),
        ('1_3', '1 a 3 anos'),
        ('3_5', '3 a 5 anos'),
        ('gt_5', 'Mais de 5 anos')
    ], string='Tempo na Empresa', required=True, default='1_3')

    salary_range = fields.Selection([
        ('r1', 'Até 5 salários mínimos'),
        ('r2', '5 a 10 salários mínimos'),
        ('r3', '10 a 15 salários mínimos'),
        ('r4', '15 a 20 salários mínimos'),
        ('r5', 'Acima de 20 salários mínimos')
    ], string='Faixa Salarial Atual (Protegido por Sigilo Estatístico)', required=True)

    capes_terms_accepted = fields.Boolean(
        string='Aceite dos Termos de Compartilhamento CAPES',
        required=True,
        default=False,
        help='Concordância com o compartilhamento de dados estatísticos anonimizados para a CAPES'
    )
    acceptance_timestamp = fields.Datetime(
        string='Carimbo de Tempo do Aceite Digital',
        default=fields.Datetime.now,
        readonly=True
    )

    @api.constrains('capes_terms_accepted')
    def _check_capes_terms(self):
        for record in self:
            if not record.capes_terms_accepted:
                raise ValidationError("O aceite dos termos de compartilhamento de dados estatísticos para a CAPES é obrigatório.")
