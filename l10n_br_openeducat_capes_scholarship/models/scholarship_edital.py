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


class CapesScholarshipEdital(models.Model):
    """Edital de Seleção e Distribuição de Bolsas de Estudo de Pós-Graduação."""
    _name = 'capes.scholarship.edital'
    _description = 'Edital de Concessão de Bolsas'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_start desc, name'

    name = fields.Char(string='Número/Ano do Edital', required=True, tracking=True)
    course_id = fields.Many2one(
        'op.course',
        string='Programa de Pós-Graduação',
        required=True,
        ondelete='restrict',
        tracking=True
    )
    academic_year_id = fields.Many2one(
        'op.academic.year',
        string='Ano Acadêmico',
        required=True,
        ondelete='restrict'
    )
    quota_id = fields.Many2one(
        'capes.scholarship.quota',
        string='Cota Institucional Vinculada',
        required=True,
        ondelete='restrict',
        tracking=True
    )
    program_id = fields.Many2one(
        'op.program.capes',
        string='Programa CAPES',
        related='quota_id.program_id',
        store=True,
        readonly=False,
        index=True
    )
    rubric_id = fields.Many2one(
        'capes.scholarship.rubric',
        string='Barema de Avaliação',
        required=True,
        ondelete='restrict'
    )
    level = fields.Selection(
        related='quota_id.level',
        string='Nível da Bolsa',
        readonly=True,
        store=True
    )

    # Cronograma Oficial
    date_start = fields.Date(string='Início das Inscrições', required=True, tracking=True)
    date_end = fields.Date(string='Término das Inscrições', required=True, tracking=True)
    date_preliminary_result = fields.Datetime(string='Divulgação do Resultado Preliminar')
    date_appeals_end = fields.Datetime(string='Prazo Limite para Recursos')
    date_final_result = fields.Datetime(string='Divulgação do Resultado Final')

    # Quadro de Vagas e Ações Afirmativas
    slots_total = fields.Integer(string='Total de Bolsas Ofertadas', required=True, default=1)
    slots_open_competition = fields.Integer(string='Vagas Ampla Concorrência', required=True, default=1)
    slots_affirmative_action = fields.Integer(string='Vagas Reservadas (PPI/Afirmativas)', default=0)
    revert_unused_affirmative_slots = fields.Boolean(
        string='Reverter Vagas PPI Remanescentes',
        default=True,
        help='Se marcado, vagas reservadas de PPI não preenchidas são automaticamente convertidas para ampla concorrência.'
    )

    state = fields.Selection([
        ('draft', 'Rascunho'),
        ('open', 'Inscrições Abertas'),
        ('under_review', 'Em Julgamento (Revisores em Paralelo)'),
        ('preliminary', 'Resultado Preliminar'),
        ('appeals', 'Fase Recursal'),
        ('homologated', 'Homologado (CPG)'),
        ('closed', 'Encerrado'),
    ], string='Situação do Edital', default='draft', tracking=True)

    application_ids = fields.One2many(
        'capes.scholarship.application',
        'edital_id',
        string='Inscrições Recebidas'
    )
    total_applications = fields.Integer(
        string='Total de Candidatos',
        compute='_compute_application_counts'
    )

    notes = fields.Text(string='Disposições Gerais e Observações')

    @api.depends('application_ids')
    def _compute_application_counts(self):
        for rec in self:
            rec.total_applications = len(rec.application_ids)

    @api.constrains('slots_open_competition', 'slots_affirmative_action', 'slots_total')
    def _check_slots_distribution(self):
        for rec in self:
            if rec.slots_open_competition + rec.slots_affirmative_action != rec.slots_total:
                raise ValidationError(
                    f"A soma de vagas de ampla concorrência ({rec.slots_open_competition}) "
                    f"e afirmativas ({rec.slots_affirmative_action}) deve ser igual ao total de vagas ({rec.slots_total})."
                )

    def action_open_edital(self):
        for rec in self:
            if not rec.quota_id or rec.quota_id.available_slots < rec.slots_total:
                raise UserError(
                    f"A cota '{rec.quota_id.name}' possui apenas {rec.quota_id.available_slots} vaga(s) "
                    f"disponível(is), insuficiente para as {rec.slots_total} bolsa(s) ofertadas neste edital."
                )
            rec.state = 'open'

    def action_start_evaluation(self):
        """Inicia a fase de julgamento pelos revisores (em paralelo)."""
        for rec in self:
            submitted = rec.application_ids.filtered(lambda a: a.state in ('submitted', 'homologated'))
            if not submitted:
                raise UserError("Não há inscrições válidas para iniciar o julgamento.")
            for app in submitted:
                app.action_distribute_to_reviewers()
            rec.state = 'under_review'

    def action_publish_preliminary(self):
        """Consolida as notas e gera a classificação preliminar."""
        for rec in self:
            for app in rec.application_ids:
                app.consolidate_scores()
            rec._rank_candidates()
            rec.state = 'preliminary'

    def action_open_appeals(self):
        self.write({'state': 'appeals'})

    def action_homologate_results(self):
        """Homologação final pela CPG e seleção de contemplados com bolsas."""
        for rec in self:
            rec._rank_candidates()
            # Distribuir as bolsas entre os classificados
            available_slots = rec.slots_total
            ppi_slots = rec.slots_affirmative_action
            ampla_slots = rec.slots_open_competition

            # Candidatos ordenados por pontuação
            sorted_apps = rec.application_ids.filtered(lambda a: a.state in ('under_review', 'ranked')).sorted(
                key=lambda a: a.final_score, reverse=True
            )

            # 1. Atendimento de cotas PPI
            ppi_awarded = 0
            for app in sorted_apps.filtered(lambda a: a.quota_type == 'ppi'):
                if ppi_awarded < ppi_slots:
                    app.state = 'awarded'
                    ppi_awarded += 1
                else:
                    break

            # 2. Se houver vagas PPI ociosas e reversão habilitada
            unused_ppi = ppi_slots - ppi_awarded
            if unused_ppi > 0 and rec.revert_unused_affirmative_slots:
                ampla_slots += unused_ppi

            # 3. Ampla Concorrência (inclusive PPIs remanescentes)
            ampla_awarded = 0
            for app in sorted_apps.filtered(lambda a: a.state != 'awarded'):
                if ampla_awarded < ampla_slots:
                    app.state = 'awarded'
                    ampla_awarded += 1
                else:
                    app.state = 'rejected'

            rec.state = 'homologated'

    def _rank_candidates(self):
        """Classifica os candidatos em ordem decrescente de nota."""
        for rec in self:
            sorted_apps = rec.application_ids.sorted(key=lambda a: a.final_score, reverse=True)
            pos = 1
            for app in sorted_apps:
                app.ranking_position = pos
                if app.state in ('submitted', 'under_review'):
                    app.state = 'ranked'
                pos += 1

    def action_close_edital(self):
        self.write({'state': 'closed'})
