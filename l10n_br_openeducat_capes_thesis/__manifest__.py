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
    'name': 'Localização Brasileira OpenEduCat CAPES - Ritos, Teses e Bancas',
    'version': '19.0.1.0.0',
    'category': 'Education',
    'summary': 'Gestão dos ritos acadêmicos (Seminário, Qualificação, Defesa), bancas examinadoras e depósito no DSpace.',
    'author': 'CINAS / IPEN-CNEN/SP',
    'license': 'LGPL-3',
    'depends': [
        'l10n_br_openeducat_capes_academic',
        'l10n_br_openeducat_capes_admission',
        'l10n_br_openeducat_capes_research',
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/thesis_rules.xml',
        'views/thesis_views.xml',
        'views/thesis_committee_views.xml',
        'views/op_student_thesis_views.xml',
        'views/op_faculty_thesis_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
