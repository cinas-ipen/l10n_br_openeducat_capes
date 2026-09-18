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
from odoo.exceptions import ValidationError, UserError
from dateutil.relativedelta import relativedelta


class CapesScholarshipAssignment(models.Model):
    """Concessão e Ciclo de Vida de Bolsa de Pós-Graduação para o Discente.
    Nota: Controla prazos regulamentares, fidelidade de frequência e relatórios.
    O desembolso financeiro é efetuado diretamente pela agência de fomento.
    """
    _name = 'capes.scholarship.assignment'
    _description = 'Concessão de Bolsa de Estudo'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_start desc, id desc'

    name = fields.Char(string='Código da Concessão', readonly=True, default='Novo')
    quota_id = fields.Many2one(
        'capes.scholarship.quota',
        string='Cota de Origem',
        required=True,
        ondelete='restrict',
        tracking=True
    )
    program_id = fields.Many2one(
        'op.program.capes',
        string='Programa CAPES',
        related='quota_id.program_id',
        store=True,
        index=True
    )
    application_id = fields.Many2one(
        'capes.scholarship.application',
        string='Candidatura Vinculada',
        ondelete='set null'
    )
    student_id = fields.Many2one(
        'op.student',
        string='Discente Bolsista',
        required=True,
        ondelete='restrict',
        tracking=True
    )
    course_id = fields.Many2one(
        'op.course',
        string='Programa de Pós-Graduação',
        required=True,
        ondelete='restrict'
    )
    sponsor_id = fields.Many2one(
        'capes.scholarship.sponsor',
        related='quota_id.sponsor_id',
        string='Agência de Fomento',
        store=True,
        readonly=True
    )
    monthly_reference_amount = fields.Monetary(
        related='quota_id.monthly_reference_amount',
        string='Valor Mensal Referencial (Agência)',
        readonly=True
    )
    currency_id = fields.Many2one(
        'res.currency',
        related='quota_id.currency_id',
        readonly=True
    )

    # Vigências e Limites
    date_start = fields.Date(string='Início da Vigência', required=True, tracking=True)
    date_end_expected = fields.Date(string='Término Regulamentar Previsto', compute='_compute_date_end', store=True)
    date_termination = fields.Date(string='Data Efetiva de Término / Cancelamento', tracking=True)

    max_allowed_months = fields.Integer(
        string='Limite Máximo de Meses (Regulamentar)',
        default=24,
        help='Teto regulamentar da agência (24 meses no mestrado; 48 meses no doutorado).'
    )
    prior_months_used = fields.Integer(
        string='Meses Usufruídos Anteriormente (no mesmo nível)',
        default=0,
        help='Meses de bolsa usufruídos pelo aluno anteriormente no mesmo nível.'
    )
    current_months_active = fields.Integer(
        string='Meses Decorridos nesta Bolsa',
        compute='_compute_active_months'
    )
    remaining_months = fields.Integer(
        string='Saldo de Meses Disponíveis',
        compute='_compute_active_months'
    )

    # Termo de Compromisso e Conformidade
    commitment_term_signed = fields.Boolean(
        string='Termo de Compromisso Assinado',
        default=False,
        tracking=True
    )
    commitment_term_file = fields.Binary(string='Termo Digitalizado / Assinado GOV.BR')
    commitment_term_filename = fields.Char(string='Nome do Arquivo do Termo')

    attendance_rate = fields.Float(
        string='Frequência Atestada (%)',
        default=100.0,
        tracking=True,
        help='Mínimo exigido pelos editais é de 80% de assiduidade.'
    )
    last_annual_report_date = fields.Date(string='Data do Último Relatório Anual')
    cpg_report_approval_ref = fields.Char(string='Deliberação CPG de Aprovação do Relatório')

    state = fields.Selection([
        ('active', 'Bolsa Ativa'),
        ('suspended', 'Suspensa (Licença Saúde / Maternidade)'),
        ('completed', 'Concluída (Titulação / Prazo Esgotado)'),
        ('canceled', 'Cancelada (Desistência / Irregularidade)'),
    ], string='Situação da Bolsa', default='active', tracking=True)

    notes = fields.Text(string='Observações e Justificativas')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name') or vals.get('name') == 'Novo':
                seq = self.env['ir.sequence'].next_by_code('capes.scholarship.assignment') or 'OUTORGA'
                vals['name'] = seq
        return super().create(vals_list)

    @api.depends('date_start', 'max_allowed_months', 'prior_months_used')
    def _compute_date_end(self):
        for rec in self:
            effective_months = max(1, rec.max_allowed_months - rec.prior_months_used)
            if rec.date_start:
                rec.date_end_expected = rec.date_start + relativedelta(months=effective_months)
            else:
                rec.date_end_expected = False

    @api.depends('date_start', 'date_termination', 'max_allowed_months', 'prior_months_used')
    def _compute_active_months(self):
        today = fields.Date.today()
        for rec in self:
            if not rec.date_start:
                rec.current_months_active = 0
                rec.remaining_months = rec.max_allowed_months - rec.prior_months_used
                continue

            end_date = rec.date_termination or min(today, rec.date_end_expected or today)
            if end_date < rec.date_start:
                rec.current_months_active = 0
            else:
                diff = relativedelta(end_date, rec.date_start)
                rec.current_months_active = diff.years * 12 + diff.months

            effective_max = rec.max_allowed_months - rec.prior_months_used
            rec.remaining_months = max(0, effective_max - rec.current_months_active)

    @api.constrains('attendance_rate')
    def _check_attendance(self):
        for rec in self:
            if rec.attendance_rate < 0 or rec.attendance_rate > 100:
                raise ValidationError("A frequência deve ser um percentual entre 0% e 100%.")

    @api.constrains('prior_months_used', 'max_allowed_months')
    def _check_prior_months(self):
        for rec in self:
            if rec.prior_months_used >= rec.max_allowed_months:
                raise ValidationError(
                    f"O discente já utilizou {rec.prior_months_used} meses no mesmo nível, "
                    f"atingindo ou superando o limite regulamentar de {rec.max_allowed_months} meses."
                )

    def action_suspend(self):
        self.write({'state': 'suspended'})

    def action_reactivate(self):
        self.write({'state': 'active'})

    def action_complete(self):
        self.write({
            'state': 'completed',
            'date_termination': fields.Date.today(),
        })

    def action_cancel(self):
        self.write({
            'state': 'canceled',
            'date_termination': fields.Date.today(),
        })

    def unlink(self):
        for rec in self:
            if rec.state in ('active', 'suspended', 'completed'):
                raise UserError(
                    "Operação de exclusão bloqueada. As concessões de bolsas ativas ou concluídas "
                    "possuem valor legal probatório e não podem ser deletadas. Cancele o registro se necessário."
                )
        return super().unlink()
