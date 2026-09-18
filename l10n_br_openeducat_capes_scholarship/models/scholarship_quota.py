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
from odoo.exceptions import ValidationError


class CapesScholarshipQuota(models.Model):
    """Livro de Cotas Institucionais de Bolsas do Programa de Pós-Graduação.
    Nota Arquitetural: O PPG controla as cotas e vigências; a liquidação financeira
    é realizada diretamente entre a agência de fomento e o discente.
    """
    _name = 'capes.scholarship.quota'
    _description = 'Cota Institucional de Bolsa'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'validity_end desc, name'

    name = fields.Char(string='Identificação da Cota', required=True, tracking=True)
    sponsor_id = fields.Many2one(
        'capes.scholarship.sponsor',
        string='Agência Mantenedora',
        required=True,
        ondelete='restrict',
        tracking=True
    )
    course_id = fields.Many2one(
        'op.course',
        string='Programa de Pós-Graduação',
        required=True,
        ondelete='restrict',
        tracking=True
    )
    program_id = fields.Many2one(
        'op.program.capes',
        string='Programa CAPES',
        index=True,
        tracking=True
    )
    level = fields.Selection([
        ('master_acad', 'Mestrado Acadêmico'),
        ('master_prof', 'Mestrado Profissional'),
        ('phd', 'Doutorado'),
        ('direct_phd', 'Doutorado Direto'),
    ], string='Nível da Cota', required=True, tracking=True)

    total_slots = fields.Integer(string='Total de Vagas da Cota', required=True, default=1, tracking=True)
    used_slots = fields.Integer(string='Vagas Ocupadas', compute='_compute_slot_usage', store=True)
    available_slots = fields.Integer(string='Vagas Disponíveis', compute='_compute_slot_usage', store=True)

    monthly_reference_amount = fields.Monetary(
        string='Valor Mensal de Referência (Agência)',
        currency_field='currency_id',
        help='Valor nominal repassado diretamente pela agência ao bolsista.'
    )
    currency_id = fields.Many2one(
        'res.currency',
        string='Moeda',
        default=lambda self: self.env.company.currency_id
    )

    validity_start = fields.Date(string='Início da Vigência', required=True)
    validity_end = fields.Date(string='Término da Vigência', required=True)
    active = fields.Boolean(string='Ativo', default=True)

    assignment_ids = fields.One2many(
        'capes.scholarship.assignment',
        'quota_id',
        string='Concessões Ativas'
    )
    edital_ids = fields.One2many(
        'capes.scholarship.edital',
        'quota_id',
        string='Editais Vinculados'
    )

    @api.depends('total_slots', 'assignment_ids.state')
    def _compute_slot_usage(self):
        for rec in self:
            occupied = len(rec.assignment_ids.filtered(lambda a: a.state in ('active', 'suspended')))
            rec.used_slots = occupied
            rec.available_slots = max(0, rec.total_slots - occupied)

    @api.constrains('total_slots')
    def _check_total_slots(self):
        for rec in self:
            if rec.total_slots < 0:
                raise ValidationError("O total de vagas da cota não pode ser negativo.")
            if rec.total_slots < rec.used_slots:
                raise ValidationError(
                    f"A cota possui {rec.used_slots} bolsa(s) ativa(s). "
                    f"O total de vagas ({rec.total_slots}) não pode ser inferior às concessões vigentes."
                )

    @api.constrains('validity_start', 'validity_end')
    def _check_validity_dates(self):
        for rec in self:
            if rec.validity_start and rec.validity_end and rec.validity_start > rec.validity_end:
                raise ValidationError("A data de início da vigência não pode ser posterior ao término.")
