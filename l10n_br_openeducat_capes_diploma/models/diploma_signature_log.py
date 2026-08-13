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


class CapesDiplomaSignatureLog(models.Model):
    _name = 'capes.diploma.signature.log'
    _description = 'Trilha de Auditoria de Assinaturas Criptográficas e Carimbo de Tempo'
    _order = 'signature_timestamp desc, id desc'

    diploma_id = fields.Many2one(
        'capes.digital.diploma',
        string='Diploma Digital',
        required=True,
        ondelete='cascade'
    )
    signer_name = fields.Char(
        string='Assinante / Entidade Certificadora',
        required=True
    )
    certificate_serial = fields.Char(
        string='Número de Série do Certificado A3/HSM'
    )
    signature_timestamp = fields.Datetime(
        string='Carimbo de Tempo (Timestamp)',
        required=True,
        default=fields.Datetime.now
    )
    signature_hash = fields.Char(
        string='Hash da Assinatura (DigestValue)'
    )
    signature_algorithm = fields.Char(
        string='Algoritmo de Criptografia',
        default='XAdES-BES SHA-256 com Carimbo de Tempo (ICP-Brasil)'
    )
