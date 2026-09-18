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


class CapesScholarshipApplication(models.Model):
    """Ficha de Inscrição e Candidatura a Edital de Bolsas de Pós-Graduação."""
    _name = 'capes.scholarship.application'
    _description = 'Inscrição em Edital de Bolsas'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'final_score desc, id desc'

    name = fields.Char(string='Protocolo de Inscrição', readonly=True, default='Novo')
    edital_id = fields.Many2one(
        'capes.scholarship.edital',
        string='Edital de Bolsas',
        required=True,
        ondelete='restrict',
        tracking=True
    )
    program_id = fields.Many2one(
        'op.program.capes',
        string='Programa CAPES',
        related='edital_id.program_id',
        store=True,
        index=True
    )
    student_id = fields.Many2one(
        'op.student',
        string='Discente Candidato',
        required=True,
        ondelete='restrict',
        tracking=True
    )
    admission_candidate_id = fields.Many2one(
        'op.admission.candidate',
        string='Candidatura no Processo Seletivo (se ingressante)',
        ondelete='set null'
    )
    faculty_id = fields.Many2one(
        'op.faculty',
        string='Orientador Responsável',
        required=True,
        ondelete='restrict',
        tracking=True
    )
    course_id = fields.Many2one(
        'op.course',
        related='edital_id.course_id',
        string='Programa de Pós-Graduação',
        store=True,
        readonly=True
    )

    # Reserva de Vagas / Modalidade de Concorrência
    quota_type = fields.Selection([
        ('ampla', 'Ampla Concorrência'),
        ('ppi', 'Ações Afirmativas (Pretos, Pardos e Indígenas - PPI)'),
    ], string='Modalidade de Concorrência', required=True, default='ampla', tracking=True)

    affirmative_declaration_file = fields.Binary(string='Autodeclaração Étnico-Racial (Anexo III)')
    affirmative_declaration_filename = fields.Char(string='Nome do Arquivo Autodeclaração')

    # Dossiê Documental e Qualificações
    lattes_url = fields.Char(string='Link do Currículo Lattes', required=True)
    work_plan_file = fields.Binary(string='Plano de Trabalho Preliminar (PDF)')
    work_plan_filename = fields.Char(string='Nome do Arquivo Plano')
    work_plan_approved_cpg = fields.Boolean(
        string='Plano de Trabalho Aprovado pela CPG?',
        default=False
    )
    work_plan_deliberation_ref = fields.Char(string='Nº da Deliberação de Aprovação do Plano')
    english_proficiency_ref = fields.Char(string='Proficiência em Inglês (Data ou Nº Deliberação)')
    capacity_exam_ref = fields.Char(string='Exame de Capacidade (Data ou Nº Deliberação/Ata)')
    residence_proof_file = fields.Binary(string='Comprovante de Residência')
    auto_presentation_letter = fields.Binary(string='Carta de Autoapresentação / Motivação')

    # Declaração de Dedicação e Acúmulo (Portaria CAPES nº 133/2023 e IN CNEN 07/2024)
    dedication_mode = fields.Selection([
        ('exclusive', 'Dedicação Exclusiva (sem renda nem aposentadoria)'),
        ('partial_teaching', 'Dedicação Parcial - Docência Autorizada pela CPG'),
        ('partial_other', 'Dedicação Parcial - Outra Atividade Remunerada'),
        ('retired', 'Aposentado(a)'),
    ], string='Regime de Dedicação', required=True, default='exclusive', tracking=True)

    weekly_work_hours = fields.Integer(string='Carga Horária Semanal Externa (horas)')
    employer_name = fields.Char(string='Empregador / Instituição Externa')
    cpg_approval_date = fields.Date(string='Data da Deliberação CPG (Acúmulo de Bolsa)')
    cpg_approval_ref = fields.Char(string='Nº da Ata/Deliberação CPG de Autorização')

    # Avaliadores Designados (Atuam em Paralelo)
    reviewer1_id = fields.Many2one(
        'op.faculty',
        string='Revisor 01 Designado',
        ondelete='restrict',
        tracking=True
    )
    reviewer2_id = fields.Many2one(
        'op.faculty',
        string='Revisor 02 Designado',
        ondelete='restrict',
        tracking=True
    )

    evaluation_ids = fields.One2many(
        'capes.scholarship.evaluation',
        'application_id',
        string='Avaliações Realizadas'
    )

    # Notas em 4 Colunas (Padrão IPEN)
    self_score = fields.Float(
        string='Coluna 1: Autoavaliação do Candidato',
        compute='_compute_scores',
        store=True
    )
    reviewer1_score = fields.Float(
        string='Coluna 2: Revisor 01',
        compute='_compute_scores',
        store=True
    )
    reviewer2_score = fields.Float(
        string='Coluna 3: Revisor 02',
        compute='_compute_scores',
        store=True
    )
    final_score = fields.Float(
        string='Coluna 4: Nota Consolidada Final',
        compute='_compute_scores',
        store=True,
        tracking=True
    )
    ranking_position = fields.Integer(string='Posição no Ranqueamento', readonly=True)

    state = fields.Selection([
        ('draft', 'Rascunho'),
        ('submitted', 'Inscrição Submetida'),
        ('homologated', 'Inscrição Homologada'),
        ('under_review', 'Em Avaliação pelos Revisores'),
        ('ranked', 'Classificado'),
        ('awarded', 'Contemplado com Bolsa'),
        ('rejected', 'Não Contemplado / Excedente'),
    ], string='Situação', default='draft', tracking=True)

    assignment_id = fields.Many2one(
        'capes.scholarship.assignment',
        string='Concessão de Bolsa Gerada',
        readonly=True
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name') or vals.get('name') == 'Novo':
                seq = self.env['ir.sequence'].next_by_code('capes.scholarship.application') or 'BOLSA'
                vals['name'] = seq
        return super().create(vals_list)

    @api.depends('evaluation_ids.total_score', 'evaluation_ids.evaluator_role', 'evaluation_ids.state')
    def _compute_scores(self):
        for rec in self:
            self_eval = rec.evaluation_ids.filtered(lambda e: e.evaluator_role == 'candidate_self')
            rev1_eval = rec.evaluation_ids.filtered(lambda e: e.evaluator_role == 'reviewer_1')
            rev2_eval = rec.evaluation_ids.filtered(lambda e: e.evaluator_role == 'reviewer_2')
            comm_eval = rec.evaluation_ids.filtered(lambda e: e.evaluator_role == 'committee')

            rec.self_score = self_eval[0].total_score if self_eval else 0.0
            rec.reviewer1_score = rev1_eval[0].total_score if rev1_eval else 0.0
            rec.reviewer2_score = rev2_eval[0].total_score if rev2_eval else 0.0

            if comm_eval:
                rec.final_score = comm_eval[0].total_score
            elif rev1_eval and rev2_eval and rev1_eval[0].state == 'completed' and rev2_eval[0].state == 'completed':
                rec.final_score = (rev1_eval[0].total_score + rev2_eval[0].total_score) / 2.0
            elif rev1_eval and rev1_eval[0].state == 'completed':
                rec.final_score = rev1_eval[0].total_score
            else:
                rec.final_score = rec.self_score

    def action_submit(self):
        for rec in self:
            if not rec.lattes_url:
                raise ValidationError("O link do Currículo Lattes é obrigatório.")
            if rec.quota_type == 'ppi' and not rec.affirmative_declaration_file:
                raise ValidationError("Para concorrer à vaga reservada (PPI), é obrigatório anexar a autodeclaração voluntária.")
            rec.state = 'submitted'

    def action_homologate(self):
        for rec in self:
            rec.state = 'homologated'

    def action_distribute_to_reviewers(self):
        """Distribui a avaliação para Revisor 1 e Revisor 2 em paralelo."""
        self.ensure_one()
        rubric = self.edital_id.rubric_id
        if not rubric:
            raise UserError("O edital não possui barema configurado.")

        # Cria avaliação para Revisor 1 se não existir
        if self.reviewer1_id and not self.evaluation_ids.filtered(lambda e: e.evaluator_role == 'reviewer_1'):
            self.env['capes.scholarship.evaluation'].create({
                'application_id': self.id,
                'evaluator_role': 'reviewer_1',
                'evaluator_id': self.reviewer1_id.id,
            })._init_lines_from_rubric(rubric)

        # Cria avaliação para Revisor 2 se não existir
        if self.reviewer2_id and not self.evaluation_ids.filtered(lambda e: e.evaluator_role == 'reviewer_2'):
            self.env['capes.scholarship.evaluation'].create({
                'application_id': self.id,
                'evaluator_role': 'reviewer_2',
                'evaluator_id': self.reviewer2_id.id,
            })._init_lines_from_rubric(rubric)

        self.state = 'under_review'

    def consolidate_scores(self):
        """Calcula a nota final e registra a avaliação consolidada pela comissão."""
        for rec in self:
            rev1 = rec.evaluation_ids.filtered(lambda e: e.evaluator_role == 'reviewer_1' and e.state == 'completed')
            rev2 = rec.evaluation_ids.filtered(lambda e: e.evaluator_role == 'reviewer_2' and e.state == 'completed')
            if rev1 and rev2:
                final_val = (rev1[0].total_score + rev2[0].total_score) / 2.0
            elif rev1:
                final_val = rev1[0].total_score
            elif rev2:
                final_val = rev2[0].total_score
            else:
                final_val = rec.self_score

            comm_eval = rec.evaluation_ids.filtered(lambda e: e.evaluator_role == 'committee')
            if not comm_eval:
                comm_eval = self.env['capes.scholarship.evaluation'].create({
                    'application_id': rec.id,
                    'evaluator_role': 'committee',
                    'total_score': final_val,
                    'state': 'completed',
                })
            else:
                comm_eval.write({'total_score': final_val, 'state': 'completed'})
            rec._compute_scores()

    def action_create_assignment(self):
        """Implementa a bolsa para o candidato aprovado, gerando a concessão."""
        self.ensure_one()
        if self.state != 'awarded':
            raise UserError("Apenas candidaturas contempladas ('awarded') podem ser implementadas.")
        if self.assignment_id:
            raise UserError("Já existe concessão de bolsa gerada para este candidato.")

        edital = self.edital_id
        quota = edital.quota_id

        # Duração regulamentar máxima: 24 meses mestrado, 48 meses doutorado
        max_months = 48 if quota.level in ('phd', 'direct_phd') else 24

        assignment = self.env['capes.scholarship.assignment'].create({
            'quota_id': quota.id,
            'application_id': self.id,
            'student_id': self.student_id.id,
            'course_id': edital.course_id.id,
            'date_start': fields.Date.today(),
            'max_allowed_months': max_months,
            'state': 'active',
        })
        self.assignment_id = assignment.id
        return {
            'type': 'ir.actions.act_window',
            'name': 'Concessão de Bolsa Implementada',
            'res_model': 'capes.scholarship.assignment',
            'res_id': assignment.id,
            'view_mode': 'form',
        }
