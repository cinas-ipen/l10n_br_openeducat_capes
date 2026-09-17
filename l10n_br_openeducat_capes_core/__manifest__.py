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
    'name': 'Localização Brasileira OpenEduCat CAPES - Core',
    'version': '19.0.1.0.0',
    'category': 'Education',
    'summary': 'Infraestrutura base, ontologia CAPES/SNPG, PIDs governamentais e biográficos.',
    'author': 'CINAS / IPEN-CNEN/SP',
    'license': 'LGPL-3',
    'depends': [
        'openeducat_core',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'views/res_company_views.xml',
        'views/res_partner_views.xml',
        'views/op_program_capes_views.xml',
        'views/op_program_concentration_views.xml',
        'views/op_faculty_views.xml',
        'views/op_student_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
