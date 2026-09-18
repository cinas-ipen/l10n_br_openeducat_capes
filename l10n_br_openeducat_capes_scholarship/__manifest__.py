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
###############################################################################

{
    'name': 'Localização Brasileira OpenEduCat CAPES - Gestão e Editais de Bolsas',
    'version': '19.0.1.0.0',
    'category': 'Education',
    'summary': 'Gestão de cotas de bolsas (CAPES, CNPq, CNEN, FAPs), editais, baremas parametrizados, avaliação paralela e termos de compromisso.',
    'author': 'CINAS / IPEN-CNEN/SP',
    'license': 'LGPL-3',
    'depends': [
        'l10n_br_openeducat_capes_core',
        'l10n_br_openeducat_capes_academic',
        'l10n_br_openeducat_capes_admission',
        'mail',
    ],
    'data': [
        'security/scholarship_security.xml',
        'security/ir.model.access.csv',
        'security/scholarship_rules.xml',
        'data/scholarship_sponsor_data.xml',
        'data/scholarship_rubric_data.xml',
        'views/scholarship_sponsor_views.xml',
        'views/scholarship_quota_views.xml',
        'views/scholarship_rubric_views.xml',
        'views/scholarship_edital_views.xml',
        'views/scholarship_application_views.xml',
        'views/scholarship_evaluation_views.xml',
        'views/scholarship_assignment_views.xml',
        'views/op_student_scholarship_views.xml',
        'views/op_faculty_scholarship_views.xml',
        'views/scholarship_menus.xml',
        'reports/report_commitment_term.xml',
    ],
    'installable': True,
    'application': True,
}
