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


class ResCompany(models.Model):
    _inherit = 'res.company'

    name_en = fields.Char(
        string='Nome da IES (Inglês)',
        help='Denominação oficial da Instituição em língua inglesa'
    )
    isni_code = fields.Char(
        string='Código ISNI',
        help='Identificador Internacional Padrão de Nome (https://isni.org/)'
    )
    ror_id = fields.Char(
        string='Registro ROR',
        help='Identificador de Organizações de Pesquisa (https://ror.org/)'
    )
    cnpj = fields.Char(
        string='CNPJ da IES / Campus',
        help='Cadastro Nacional da Pessoa Jurídica (14 dígitos)'
    )
    capes_code = fields.Char(
        string='Código IES CAPES',
        help='Código de cadastro da Instituição na CAPES'
    )
    emec_code = fields.Char(
        string='Código e-MEC',
        help='Código de identificação da IES no sistema e-MEC'
    )
    acronym = fields.Char(
        string='Sigla da IES',
        help='Sigla oficial da Instituição'
    )
    admin_category = fields.Selection([
        ('public_fed', 'Pública Federal'),
        ('public_est', 'Pública Estadual'),
        ('public_mun', 'Pública Municipal'),
        ('private_profit', 'Privada com fins lucrativos'),
        ('private_non_profit', 'Privada sem fins lucrativos'),
        ('special', 'Especial')
    ], string='Categoria Administrativa')

    sub_category = fields.Selection([
        ('community', 'Comunitária'),
        ('confessional', 'Confessional'),
        ('philanthropic', 'Filantrópica')
    ], string='Sub-categoria (Privadas)')

    academic_org = fields.Selection([
        ('faculty', 'Faculdades'),
        ('uni_center', 'Centros Universitários'),
        ('university', 'Universidades'),
        ('if', 'Institutos Federais (IFs)'),
        ('gov_school', 'Escola de Governo')
    ], string='Organização Acadêmica')

    pro_rector_name = fields.Char(
        string='Nome do Pró-Reitor de Pós-Graduação'
    )
    pro_rector_start = fields.Date(
        string='Início da Atuação do Pró-Reitor'
    )
    pro_rector_end = fields.Date(
        string='Fim da Atuação do Pró-Reitor'
    )

    # Dados de Georreferenciamento e Códigos Regionais
    ibge_code = fields.Char(
        string='Código IBGE Município',
        size=7,
        help='Código do município no IBGE (7 dígitos)'
    )
    siafi_code = fields.Char(
        string='Código SIAFI',
        help='Código da unidade no SIAFI'
    )
    mesoregion_id = fields.Char(
        string='Identificador Mesorregião'
    )
    microregion_id = fields.Char(
        string='Identificador Microrregião'
    )
    latitude = fields.Float(
        string='Latitude',
        digits=(10, 7),
        help='Latitude em graus decimais'
    )
    longitude = fields.Float(
        string='Longitude',
        digits=(10, 7),
        help='Longitude em graus decimais'
    )

    @api.constrains('cnpj')
    def _check_cnpj_validity(self):
        for record in self:
            if not record.cnpj:
                continue
            digits = re.sub(r'\D', '', record.cnpj)
            if len(digits) != 14:
                raise ValidationError("O CNPJ da IES deve conter exatamente 14 dígitos numéricos.")
            
            # Validação Módulo 11 do CNPJ
            if digits == digits[0] * 14:
                raise ValidationError("O CNPJ informado é inválido.")
            
            w1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
            d1 = sum(int(digits[i]) * w1[i] for i in range(12)) % 11
            d1 = 0 if d1 < 2 else 11 - d1
            if int(digits[12]) != d1:
                raise ValidationError("O CNPJ informado possui dígito verificador inválido.")
                
            w2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
            d2 = sum(int(digits[i]) * w2[i] for i in range(13)) % 11
            d2 = 0 if d2 < 2 else 11 - d2
            if int(digits[13]) != d2:
                raise ValidationError("O CNPJ informado possui dígito verificador inválido.")

    @api.constrains('pro_rector_start', 'pro_rector_end')
    def _check_pro_rector_dates(self):
        for record in self:
            if record.pro_rector_start and record.pro_rector_end:
                if record.pro_rector_end < record.pro_rector_start:
                    raise ValidationError("A data final de atuação do Pró-Reitor deve ser posterior à data inicial.")
