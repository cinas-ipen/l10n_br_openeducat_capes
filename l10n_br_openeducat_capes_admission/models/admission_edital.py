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

import math
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class OpAdmissionEdital(models.Model):
    _name = 'op.admission.edital'
    _description = 'Edital de Seleção Pública de Pós-Graduação'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, code'

    name = fields.Char(
        string='Título do Edital',
        required=True,
        tracking=True,
        help='Ex: Edital de Seleção PPGTN 2026/1 - Mestrado e Doutorado'
    )
    code = fields.Char(
        string='Código / Número do Edital',
        required=True,
        tracking=True,
        help='Ex: EDITAL-PPGTN-2026-01'
    )
    curriculum_version_id = fields.Many2one(
        'op.curriculum.version',
        string='Versão Regimental Vinculada (Ato Perfeito)',
        required=True,
        tracking=True,
        help='Regimento regente das regras do certame e da vida acadêmica da turma'
    )
    program_id = fields.Many2one(
        'op.program.capes',
        string='Programa de Pós-Graduação',
        related='curriculum_version_id.program_id',
        store=True,
        readonly=True
    )
    academic_year = fields.Integer(
        string='Ano Letivo da Turma (Cohort)',
        required=True,
        default=lambda self: fields.Date.context_today(self).year
    )
    academic_term = fields.Selection([
        ('1', '1º Semestre'),
        ('2', '2º Semestre')
    ], string='Período Letivo', required=True, default='1')

    cohort_name = fields.Char(
        string='Denominação da Turma (Cohort)',
        help='Denominação do agrupamento cronológico (ex: Turma IPEN 2026/1)'
    )
    is_remanescent_vagas = fields.Boolean(
        string='Edital de Vagas Remanescentes',
        default=False,
        help='Indica se o certame destina-se a preencher vagas ociosas da mesma turma'
    )
    parent_edital_id = fields.Many2one(
        'op.admission.edital',
        string='Edital Original Sede',
        help='Edital de origem quando se tratar de certame para vagas remanescentes'
    )
    total_slots = fields.Integer(
        string='Total de Vagas Globais',
        required=True,
        default=10
    )
    affirmative_action_percent = fields.Float(
        string='Reserva de Cotas / Ações Afirmativas (%)',
        default=20.0,
        required=True,
        help='Percentual de vagas reservadas para candidatos pretos, pardos, indígenas ou PcD'
    )
    affirmative_action_slots = fields.Integer(
        string='Vagas Reservadas (Cotas)',
        compute='_compute_affirmative_slots',
        store=True
    )
    start_date = fields.Date(
        string='Início das Inscrições',
        required=True
    )
    end_date = fields.Date(
        string='Término das Inscrições',
        required=True
    )
    result_date = fields.Date(
        string='Data Prevista Resultado Final'
    )
    state = fields.Selection([
        ('draft', 'Rascunho'),
        ('published', 'Publicado / Inscrições Abertas'),
        ('in_selection', 'Em Processo Seletivo'),
        ('homologated', 'Homologado / Concluído'),
        ('cancelled', 'Cancelado')
    ], string='Situação do Edital', default='draft', tracking=True)

    phase_ids = fields.One2many(
        'op.edital.phase',
        'edital_id',
        string='Fases de Seleção'
    )
    slot_distribution_ids = fields.One2many(
        'op.edital.slot.distribution',
        'edital_id',
        string='Quadro de Vagas por Linha / Orientador'
    )
    candidate_ids = fields.One2many(
        'op.admission.candidate',
        'edital_id',
        string='Candidatos Inscritos'
    )

    @api.depends('total_slots', 'affirmative_action_percent')
    def _compute_affirmative_slots(self):
        for record in self:
            if record.total_slots and record.affirmative_action_percent:
                record.affirmative_action_slots = math.ceil(record.total_slots * (record.affirmative_action_percent / 100.0))
            else:
                record.affirmative_action_slots = 0

    @api.constrains('start_date', 'end_date')
    def _check_edital_dates(self):
        for record in self:
            if record.start_date and record.end_date and record.end_date < record.start_date:
                raise ValidationError("A data final de inscrições deve ser posterior à data inicial.")


class OpEditalPhase(models.Model):
    _name = 'op.edital.phase'
    _description = 'Fase de Seleção do Edital'
    _order = 'sequence, id'

    edital_id = fields.Many2one(
        'op.admission.edital',
        string='Edital',
        required=True,
        ondelete='cascade'
    )
    sequence = fields.Integer(
        string='Ordem da Fase',
        default=10
    )
    name = fields.Char(
        string='Nome da Fase',
        required=True,
        help='Ex: Validação Documental, Prova Escrita, Entrevista Qualitativa'
    )
    phase_type = fields.Selection([
        ('doc_val', 'Validação Documental'),
        ('lattes_exam', 'Análise Lattes e Provas'),
        ('interview', 'Entrevista Qualitativa (Rubrica 1 a 5)'),
        ('proficiency', 'Trava de Proficiência na Admissão')
    ], string='Tipo da Fase', required=True, default='doc_val')

    weight = fields.Float(
        string='Peso na Nota Final (%)',
        default=1.0
    )
    is_eliminatory = fields.Boolean(
        string='Fase Eliminatória',
        default=True
    )
    min_score = fields.Float(
        string='Nota Mínima para Aprovação',
        default=7.0
    )


class OpEditalSlotDistribution(models.Model):
    _name = 'op.edital.slot.distribution'
    _description = 'Distribuição de Vagas do Edital por Linha e Orientador'

    edital_id = fields.Many2one(
        'op.admission.edital',
        string='Edital',
        required=True,
        ondelete='cascade'
    )
    research_line = fields.Char(
        string='Linha de Pesquisa',
        required=True
    )
    faculty_id = fields.Many2one(
        'op.faculty',
        string='Orientador Responsável',
        required=True
    )
    slots = fields.Integer(
        string='Vagas Ofertadas',
        default=1,
        required=True
    )


class OpAdmissionCandidate(models.Model):
    _name = 'op.admission.candidate'
    _description = 'Inscrição de Candidato em Edital de Seleção'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'final_score desc, id'

    edital_id = fields.Many2one(
        'op.admission.edital',
        string='Edital de Seleção',
        required=True,
        ondelete='cascade',
        tracking=True
    )
    partner_id = fields.Many2one(
        'res.partner',
        string='Candidato (Pessoa)',
        required=True,
        tracking=True
    )
    advisor_id = fields.Many2one(
        'op.faculty',
        string='Orientador Pretendido / Indicado',
        tracking=True
    )
    is_affirmative_action = fields.Boolean(
        string='Optante por Cotas / Ações Afirmativas',
        default=False,
        tracking=True
    )
    english_proficient = fields.Boolean(
        string='Comprovante Proficiência Inglês Deferido',
        default=False,
        tracking=True
    )
    final_score = fields.Float(
        string='Pontuação Final Computada',
        default=0.0,
        tracking=True
    )
    state = fields.Selection([
        ('draft', 'Inscrito'),
        ('doc_ok', 'Documentação Homologada'),
        ('in_evaluation', 'Em Avaliação'),
        ('approved', 'Aprovado'),
        ('approved_override', 'Aprovado (Exceção CPG / Override)'),
        ('rejected', 'Reprovado'),
        ('converted', 'Convertido em Aluno Regular')
    ], string='Situação da Inscrição', default='draft', tracking=True)

    # Soberania do Coordenador (Override)
    is_override = fields.Boolean(
        string='Aprovação em Caráter Excepcional (Override)',
        default=False,
        tracking=True,
        help='Ativado pelo Coordenador para aprovação de candidato estratégico reprovado em etapas teóricas'
    )
    override_justification = fields.Text(
        string='Justificativa Técnica do Override (Obrigatória)',
        tracking=True
    )
    converted_student_id = fields.Many2one(
        'op.student',
        string='Aluno Regular Criado',
        readonly=True
    )

    def action_apply_override(self):
        """Aplica a Soberania do Coordenador (Override) mediante justificativa técnica."""
        for record in self:
            if not record.override_justification or not record.override_justification.strip():
                raise ValidationError("A justificativa técnica para a aprovação em caráter excepcional (soberania do coordenador) é obrigatória.")
            record.is_override = True
            record.state = 'approved_override'

    def action_convert_to_student(self):
        """Converte candidato aprovado em Aluno Regular (op.student) com verificação de proficiência."""
        Student = self.env['op.student']
        for record in self:
            if record.state not in ('approved', 'approved_override'):
                raise ValidationError("Apenas candidatos com situação Aprovado ou Aprovado (Override) podem ser convertidos em Aluno Regular.")
            
            curriculum = record.edital_id.curriculum_version_id
            # Trava de Proficiência na Admissão (Regra IPEN/USP)
            if curriculum.proficiency_stage == 'admission' and not record.english_proficient:
                raise ValidationError("O regimento do curso exige a comprovação de proficiência linguística na admissão (Regra IPEN/USP) antes da conversão em Aluno Regular.")

            # Criação do Aluno Regular
            student = Student.create({
                'partner_id': record.partner_id.id,
                'curriculum_version_id': curriculum.id,
                'advisor_id': record.advisor_id.id if record.advisor_id else False,
                'student_category': 'regular',
                'capes_status': 'enrolled',
                'admission_date': fields.Date.context_today(self),
                'english_proficiency_status': 'approved' if record.english_proficient else 'pending',
            })
            record.converted_student_id = student
            record.state = 'converted'
