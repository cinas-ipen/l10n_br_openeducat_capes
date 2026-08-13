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

{
    'name': 'Localização Brasileira OpenEduCat CAPES - Interoperabilidade e APIs RESTful',
    'version': '19.0.1.0.0',
    'category': 'Education',
    'summary': 'APIs RESTful JSON (/api/capes/v1/), Privacy by Design, produções intelectuais e crosswalk DSpace (oai_capes).',
    'author': 'CINAS / IPEN-CNEN/SP',
    'license': 'LGPL-3',
    'depends': [
        'l10n_br_openeducat_capes_core',
        'l10n_br_openeducat_capes_ptt',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/intellectual_production_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
