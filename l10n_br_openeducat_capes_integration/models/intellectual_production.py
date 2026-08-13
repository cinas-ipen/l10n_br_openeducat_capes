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
import xml.etree.ElementTree as ET


class CapesIntellectualProduction(models.Model):
    _name = 'capes.intellectual.production'
    _description = 'Mapeamento Semântico e Guarda de Produção Intelectual'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'publication_year desc, id desc'

    name = fields.Char(
        string='Título da Produção Intelectual / Científica',
        required=True,
        tracking=True
    )
    production_type = fields.Selection([
        ('article', 'Artigo em Periódico Indexado'),
        ('book', 'Livro Técnico-Científico'),
        ('chapter', 'Capítulo de Livro'),
        ('conference', 'Trabalho em Anais de Evento'),
        ('patent', 'Patente / Propriedade Intelectual (PTT)'),
        ('software', 'Software / Aplicativo (PTT)'),
        ('other_ptt', 'Outro Produto Técnico-Tecnológico (PTT)')
    ], string='Tipo de Produção', required=True, default='article', tracking=True)

    student_id = fields.Many2one(
        'op.student',
        string='Discente Autor'
    )
    faculty_id = fields.Many2one(
        'op.faculty',
        string='Docente Autor / Orientador'
    )
    program_id = fields.Many2one(
        'op.program.capes',
        string='Programa PPG Associado',
        required=True
    )

    publication_year = fields.Integer(
        string='Ano de Publicação / Concessão',
        required=True,
        default=lambda self: fields.Date.today().year
    )
    doi = fields.Char(
        string='DOI (Digital Object Identifier)',
        help='Ex: 10.1016/j.radphyschem.2026.101234'
    )
    handle = fields.Char(
        string='Handle URI (DSpace / Fonte Ouro)',
        help='Ex: http://repositorio.ipen.br/handle/12345/6789'
    )
    isbn_issn = fields.Char(
        string='ISBN / ISSN'
    )
    journal_conference_name = fields.Char(
        string='Nome do Periódico / Evento / Concessionário'
    )

    qualis_stratum = fields.Selection([
        ('A1', 'A1'), ('A2', 'A2'), ('A3', 'A3'), ('A4', 'A4'),
        ('B1', 'B1'), ('B2', 'B2'), ('B3', 'B3'), ('B4', 'B4'), ('C', 'C'),
        ('T1', 'T1 - Qualis Tecnológico'), ('T2', 'T2 - Qualis Tecnológico'),
        ('T3', 'T3 - Qualis Tecnológico'), ('T4', 'T4 - Qualis Tecnológico'),
        ('T5', 'T5 - Qualis Tecnológico'), ('TNC', 'TNC - Não Classificado')
    ], string='Estrato Qualis / Qualis Tecnológico', tracking=True)

    oai_pmh_xml_payload = fields.Text(
        string='Payload XML Gerado (Crosswalk oai_capes)',
        readonly=True,
        help='XML formatado sob o namespace oai_capes para alinhamento com DSpace'
    )

    state = fields.Selection([
        ('draft', 'Rascunho'),
        ('validated', 'Validado CPG'),
        ('exported', 'Exportado DSpace / Sucupira')
    ], string='Situação', default='draft', tracking=True)

    def action_generate_oai_payload(self):
        """Gera o payload XML formatado sob o namespace oai_capes para alinhamento com o DSpace."""
        for record in self:
            snpg_code = record.program_id.snpg_code or 'N/A'
            author_name = record.student_id.partner_id.name if record.student_id else (record.faculty_id.partner_id.name if record.faculty_id else 'N/A')
            author_orcid = record.student_id.partner_id.orcid if record.student_id else (record.faculty_id.partner_id.orcid if record.faculty_id else '')
            company = self.env.company
            ror_code = company.ror_id or ''

            xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<oai_capes:thesis xmlns:oai_capes="http://capes.gov.br/oai/oai_capes/">
    <oai_capes:programCode>{snpg_code}</oai_capes:programCode>
    <oai_capes:title>{record.name or ''}</oai_capes:title>
    <oai_capes:publicationYear>{record.publication_year or ''}</oai_capes:publicationYear>
    <oai_capes:identifier>{record.doi or record.handle or ''}</oai_capes:identifier>
    <oai_capes:author>
        <oai_capes:name>{author_name}</oai_capes:name>
        <oai_capes:orcid>{author_orcid or ''}</oai_capes:orcid>
    </oai_capes:author>
    <oai_capes:institutionRor>{ror_code}</oai_capes:institutionRor>
    <oai_capes:qualisStratum>{record.qualis_stratum or ''}</oai_capes:qualisStratum>
</oai_capes:thesis>"""
            record.oai_pmh_xml_payload = xml_content
            record.state = 'validated'

    def action_mark_exported(self):
        for record in self:
            record.state = 'exported'
