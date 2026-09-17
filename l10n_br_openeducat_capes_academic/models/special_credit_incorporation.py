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
from odoo.exceptions import ValidationError, UserError


class OpSpecialCreditIncorporationRequest(models.Model):
    _name = 'op.special.credit.incorporation.request'
    _description = 'Requerimento de Aproveitamento de Créditos de Aluno Especial'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(
        string='Número do Requerimento',
        required=True,
        copy=False,
        readonly=True,
        default='Novo'
    )
    student_id = fields.Many2one(
        'op.student',
        string='Discente Requerente (Regular)',
        required=True,
        tracking=True,
        help='Discente com matrícula regular ativa na IES'
    )
    target_program_id = fields.Many2one(
        'op.program.capes',
        string='Programa de Pós-Graduação',
        required=True,
        tracking=True
    )
    target_curriculum_version_id = fields.Many2one(
        'op.curriculum.version',
        string='Versão Regimental Ativa',
        required=True,
        tracking=True,
        help='Regimento que dita os limites de aproveitamento e prazo de validade'
    )
    admission_date = fields.Date(
        string='Data de Ingresso Regular',
        related='student_id.admission_date',
        store=True,
        readonly=True
    )

    quarantine_ledger_ids = fields.Many2many(
        'op.student.credit.ledger',
        'rel_special_incorporation_quarantine_ledger',
        'request_id',
        'ledger_id',
        string='Disciplinas Cursadas como Especial (Em Quarentena)',
        domain="[('student_id', '=', student_id), ('credit_type', '=', 'subject_special_quarantine'), ('is_approved', '=', True)]",
        help='Disciplinas concluídas anteriormente sob regime de Aluno Especial'
    )

    state = fields.Selection([
        ('draft', 'Rascunho'),
        ('submitted', 'Submetido para Parecer'),
        ('advisor_approved', 'Aprovado pelo Orientador'),
        ('cpg_approved', 'Homologado pela CPG'),
        ('rejected', 'Indeferido')
    ], string='Situação do Requerimento', default='draft', tracking=True)

    # Parecer e Homologação
    advisor_opinion = fields.Text(
        string='Parecer Circunstanciado do Orientador',
        tracking=True,
        help='Justificativa da pertinência das disciplinas em relação à pesquisa da dissertação'
    )
    cpg_resolution_number = fields.Char(
        string='Número da Resolução / Ata da CPG',
        tracking=True,
        help='Identificador formal do ato colegiado de deferimento'
    )
    cpg_resolution_date = fields.Date(
        string='Data da Reunião / Deliberação CPG',
        tracking=True
    )
    cpg_notes = fields.Text(
        string='Despacho / Observações da CPG',
        tracking=True
    )

    total_requested_credits = fields.Float(
        string='Total de Créditos Solicitados',
        compute='_compute_totals',
        store=True
    )
    total_requested_subjects = fields.Integer(
        string='Total de Disciplinas Solicitadas',
        compute='_compute_totals',
        store=True
    )

    @api.depends('quarantine_ledger_ids', 'quarantine_ledger_ids.credits')
    def _compute_totals(self):
        for record in self:
            record.total_requested_credits = sum(record.quarantine_ledger_ids.mapped('credits'))
            record.total_requested_subjects = len(record.quarantine_ledger_ids)

    @api.onchange('student_id')
    def _onchange_student_id(self):
        if self.student_id:
            if hasattr(self.student_id, 'curriculum_version_id') and self.student_id.curriculum_version_id:
                self.target_curriculum_version_id = self.student_id.curriculum_version_id
                self.target_program_id = self.student_id.curriculum_version_id.program_id
            elif hasattr(self.student_id, 'program_id') and self.student_id.program_id:
                self.target_program_id = self.student_id.program_id

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'Novo') == 'Novo':
                year = fields.Date.context_today(self).year
                count = self.search_count([]) + 1
                vals['name'] = f"REQ-ESP/{year}/{count:04d}"
        return super().create(vals_list)

    def action_submit(self):
        """Valida prazos decadenciais e limites antes de submeter o requerimento."""
        for record in self:
            if not record.quarantine_ledger_ids:
                raise ValidationError("Selecione ao menos uma disciplina cursada em regime especial para requerer o aproveitamento.")

            regimento = record.target_curriculum_version_id
            if not regimento:
                raise ValidationError("O discente precisa estar associado a uma versão regimental ativa.")

            # Validação 1: Limite quantitativo de disciplinas
            max_limit = regimento.max_special_subjects_limit or 2
            if len(record.quarantine_ledger_ids) > max_limit:
                raise ValidationError(
                    f"O regimento '{regimento.name}' permite no máximo {max_limit} disciplina(s) cursada(s) como Aluno Especial. "
                    f"Foram selecionadas {len(record.quarantine_ledger_ids)} disciplinas."
                )

            # Validação 2: Prazo decadencial (default 36 meses / 3 anos)
            validity_months = regimento.special_credit_validity_months or 36
            adm_date = record.admission_date or fields.Date.context_today(self)

            for line in record.quarantine_ledger_ids:
                if line.date_earned:
                    delta_months = (adm_date.year - line.date_earned.year) * 12 + (adm_date.month - line.date_earned.month)
                    if delta_months > validity_months:
                        raise ValidationError(
                            f"A disciplina '{line.course_name}' foi concluída em {line.date_earned.strftime('%d/%m/%Y')}, "
                            f"totalizando aproximadamente {delta_months} meses até a data de admissão regular ({adm_date.strftime('%d/%m/%Y')}).\n"
                            f"O regimento estabelece prazo decadencial máximo de {validity_months} meses (3 anos) para aproveitamento de estudos de Aluno Especial."
                        )

            record.state = 'submitted'

    def action_advisor_approve(self):
        """Registra a aprovação/anuência do orientador."""
        for record in self:
            if not record.advisor_opinion or not record.advisor_opinion.strip():
                raise ValidationError("É obrigatório preencher o parecer circunstanciado do orientador antes de encaminhar à CPG.")
            record.state = 'advisor_approved'

    def action_cpg_approve(self):
        """Homologa o aproveitamento e gera lançamentos imutáveis append-only no Livro-Razão."""
        Ledger = self.env['op.student.credit.ledger']
        for record in self:
            if not record.cpg_resolution_number or not record.cpg_resolution_date:
                raise ValidationError("Informe o número da resolução/ata da CPG e a respectiva data para homologar o aproveitamento.")

            # Geração das linhas de crédito incorporadas no Livro-Razão (Append-Only)
            for line in record.quarantine_ledger_ids:
                Ledger.create({
                    'student_id': record.student_id.id,
                    'curriculum_version_id': record.target_curriculum_version_id.id,
                    'credit_type': 'subject_special_incorporated',
                    'subject_id': line.subject_id.id if line.subject_id else False,
                    'course_name': line.course_name,
                    'credits': line.credits,
                    'grade_concept': line.grade_concept,
                    'is_approved': True,
                    'date_earned': line.date_earned,
                    'origin_ref': f"Aproveitamento Resolução CPG {record.cpg_resolution_number} de {record.cpg_resolution_date.strftime('%d/%m/%Y')} (Origem Quarentena #{line.id})",
                    'incorporation_request_id': record.id,
                    'original_program_id': line.original_program_id.id if line.original_program_id else False,
                    'notes': f"Crédito de aluno especial homologado em ata da CPG ({record.cpg_resolution_number})."
                })

            record.state = 'cpg_approved'

    def action_reject(self):
        """Registra o indeferimento do requerimento."""
        for record in self:
            record.state = 'rejected'
