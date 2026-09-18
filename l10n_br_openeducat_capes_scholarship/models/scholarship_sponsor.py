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

from odoo import models, fields, api


class CapesScholarshipSponsor(models.Model):
    """Agência de Fomento / Entidade Mantenedora de Bolsas de Pós-Graduação."""
    _name = 'capes.scholarship.sponsor'
    _description = 'Agência Mantenedora de Bolsas'
    _order = 'name'

    name = fields.Char(string='Nome da Agência', required=True)
    code = fields.Char(string='Código/Sigla', required=True, index=True)
    sponsor_type = fields.Selection([
        ('federal', 'Federal (CAPES, CNPq)'),
        ('state', 'Estadual (FAPESP, FAPs)'),
        ('institutional', 'Institucional (CNEN, IPEN, USP)'),
        ('private', 'Empresarial / Privado / Fundações'),
    ], string='Tipo de Mantenedora', required=True, default='federal')
    
    website = fields.Char(string='Website Oficial')
    notes = fields.Text(string='Regulamentos e Diretrizes Gerais')
    active = fields.Boolean(string='Ativo', default=True)

    quota_ids = fields.One2many(
        'capes.scholarship.quota',
        'sponsor_id',
        string='Cotas Institucionais'
    )
    total_active_quotas = fields.Integer(
        string='Total de Cotas Ativas',
        compute='_compute_quota_summary'
    )

    @api.depends('quota_ids.active', 'quota_ids.available_slots')
    def _compute_quota_summary(self):
        for rec in self:
            rec.total_active_quotas = sum(
                rec.quota_ids.filtered(lambda q: q.active).mapped('total_slots')
            )
