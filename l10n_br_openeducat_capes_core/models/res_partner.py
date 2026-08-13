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

import re
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    capes_id = fields.Integer(
        string='Identificador CAPES',
        help='ID numérico único no cadastro da CAPES'
    )
    internal_code = fields.Char(
        string='Código Institucional',
        help='Matrícula ou número funcional no sistema da IES'
    )
    fiscal_name = fields.Char(
        string='Nome Fiscal',
        help='Nome completo conforme constando no cadastro da Receita Federal'
    )
    cpf = fields.Char(
        string='CPF',
        size=14,
        help='Cadastro de Pessoas Físicas (11 dígitos numéricos)'
    )
    mother_name = fields.Char(
        string='Nome da Mãe'
    )
    birth_date = fields.Date(
        string='Data de Nascimento'
    )
    gender = fields.Selection([
        ('female', 'Feminino'),
        ('male', 'Masculino'),
        ('intersex', 'Intersexo'),
        ('not_declared', 'Não declarado')
    ], string='Sexo Biológico')

    race_color = fields.Selection([
        ('white', 'Branca'),
        ('black', 'Preta'),
        ('brown', 'Parda'),
        ('yellow', 'Amarela'),
        ('indigenous', 'Indígena'),
        ('not_declared', 'Não declarada')
    ], string='Raça/Cor')

    has_disability = fields.Boolean(
        string='Pessoa com Deficiência',
        default=False
    )
    nationality = fields.Char(
        string='Nacionalidade',
        default='Brasileira'
    )
    birth_country_id = fields.Many2one(
        'res.country',
        string='País de Nascimento'
    )
    birth_state = fields.Selection([
        ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'),
        ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'),
        ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'),
        ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')
    ], string='UF de Nascimento')

    birth_city_name = fields.Char(
        string='Município de Nascimento'
    )
    social_url = fields.Char(
        string='URL de Perfil Social / Profissional'
    )
    is_internal = fields.Boolean(
        string='Pertence ao Quadro da IES',
        default=True,
        help='Indica se a pessoa pertence ao corpo docente/discente/técnico da própria IES'
    )

    # Identificadores Persistentes (PIDs)
    orcid = fields.Char(
        string='Identificador ORCiD',
        help='Formato de 16 dígitos ou URL completo (ex: 0000-0002-1825-0097)'
    )
    lattes_url = fields.Char(
        string='URL / ID Lattes',
        help='Link ou ID de 16 dígitos do Currículo Lattes CNPq'
    )
    researcher_id = fields.Char(
        string='ResearcherID (Web of Science)'
    )
    scopus_id = fields.Char(
        string='Scopus Author ID'
    )

    # Formação Acadêmica Geral
    academic_level = fields.Selection([
        ('elem', 'Ensino Fundamental'),
        ('sec', 'Ensino Médio'),
        ('grad', 'Graduação'),
        ('post', 'Pós-Graduação')
    ], string='Nível Acadêmico Geral')

    highest_degree = fields.Selection([
        ('bachelor', 'Bacharelado / Licenciatura'),
        ('spec', 'Especialização'),
        ('master', 'Mestrado'),
        ('phd', 'Doutorado')
    ], string='Maior Grau Acadêmico Obtido')

    @api.constrains('cpf')
    def _check_cpf_validity(self):
        for record in self:
            if not record.cpf:
                continue
            digits = re.sub(r'\D', '', record.cpf)
            if len(digits) != 11:
                raise ValidationError("O CPF deve conter exatamente 11 dígitos numéricos.")
            if digits == digits[0] * 11:
                raise ValidationError("O CPF informado é inválido.")
            
            # Validação Módulo 11 do CPF
            d1 = sum(int(digits[i]) * (10 - i) for i in range(9)) % 11
            d1 = 0 if d1 < 2 else 11 - d1
            if int(digits[9]) != d1:
                raise ValidationError("O CPF informado possui dígito verificador inválido.")
                
            d2 = sum(int(digits[i]) * (11 - i) for i in range(10)) % 11
            d2 = 0 if d2 < 2 else 11 - d2
            if int(digits[10]) != d2:
                raise ValidationError("O CPF informado possui dígito verificador inválido.")

    @api.constrains('orcid')
    def _check_orcid_validity(self):
        orcid_regex = re.compile(r'^(https?://orcid\.org/)?\d{4}-\d{4}-\d{4}-\d{3}[\dX]$')
        for record in self:
            if record.orcid and not orcid_regex.match(record.orcid.strip()):
                raise ValidationError("O formato do ORCiD é inválido. Utilize o formato 0000-0000-0000-0000 ou o URL completo.")
