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
from odoo.exceptions import ValidationError


class OpCurriculumVersion(models.Model):
    _name = 'op.curriculum.version'
    _description = 'Versão Regimental e Motor de Versionamento Curricular'
    _order = 'create_date desc, name'

    name = fields.Char(
        string='Nome da Versão Regimental',
        required=True,
        help='Ex: Regimento IPEN 2024, Regimento CDTN 2026, Regimento Mackenzie 2024'
    )
    program_id = fields.Many2one(
        'op.program.capes',
        string='Programa de Pós-Graduação',
        required=True,
        ondelete='cascade'
    )

    # Prazos Temporais e Cronometria
    max_months_defense = fields.Integer(
        string='Prazo Máximo Titulação (meses)',
        default=24,
        required=True,
        help='Ex: 24 para Mestrado, 48 para Doutorado'
    )
    max_extension_days = fields.Integer(
        string='Teto Máximo Prorrogação (dias)',
        default=90
    )
    max_days_post_defense_deposit = fields.Integer(
        string='Prazo Depósito Final Pós-Defesa (dias)',
        default=30,
        help='30 dias (IPEN/Mackenzie) a 90 dias (CDTN)'
    )
    presentation_max_minutes = fields.Integer(
        string='Tempo Máximo Exposição (min)',
        default=50
    )
    arguing_max_minutes_per_member = fields.Integer(
        string='Tempo Máximo Arguição p/ Membro (min)',
        default=40
    )

    # Regras de Trancamento e Flexibilidade
    max_trancamento_days = fields.Integer(
        string='Prazo Máximo de Trancamento Contínuo (dias)',
        default=365
    )
    block_first_semester_trancamento = fields.Boolean(
        string='Bloqueio Trancamento 1º Semestre',
        default=False
    )
    retorno_rule = fields.Selection([
        ('current_matrix', 'Vinculação à Matriz Vigente no Retorno')
    ], string='Regra de Retorno e Estrutura', default='current_matrix', required=True)

    # Matriz de Carga Horária, Créditos e Aproveitamento (Sucupira / CAPES)
    min_credits = fields.Integer(
        string='Créditos Totais Exigidos',
        default=100,
        required=True,
        help='Total de créditos exigidos para titulação (ex: 100 créditos MP-TRCS)'
    )
    min_subject_credits = fields.Integer(
        string='Créditos Mínimos em Disciplinas',
        default=40,
        required=True,
        help='Créditos exigidos especificamente em disciplinas presenciais do programa'
    )
    thesis_credits = fields.Integer(
        string='Créditos da Dissertação / Tese',
        default=52,
        required=True,
        help='Créditos atribuídos ao Trabalho Final de Curso (Dissertação / Tese)'
    )
    other_mandatory_credits = fields.Integer(
        string='Créditos em Outras Atividades Obrigatórias',
        default=8,
        required=True,
        help='Créditos em Seminários Gerais de Área, Estágios Docência ou Atividades Fixas'
    )
    credit_hour_ratio = fields.Integer(
        string='Horas por Unidade de Crédito',
        default=15,
        required=True,
        help='15h (IPEN/CDTN) ou 12h (Mackenzie Computação) / 10h (Mackenzie ADN)'
    )
    max_external_credits_percent = fields.Integer(
        string='Teto Aproveitamento Créditos Externos (%)',
        default=50,
        help='Teto regulamentar para aproveitamento de disciplinas externas (ex: 50% IPEN, 40% Mackenzie)'
    )
    max_external_subject_credits = fields.Float(
        string='Teto Efetivo Disciplinas Externas (Créditos)',
        compute='_compute_max_external_subject_credits',
        store=True,
        help='Quantidade máxima absoluta de créditos em disciplinas externas que podem ser aproveitados'
    )
    grading_scale_type = fields.Selection([
        ('scale_abc_r', 'Conceitos A, B, C (Aprovados) e R (Reprovado)'),
        ('scale_abcd_rf', 'Conceitos A, B, C, D (Aprovados) e R, F (Reprovados)')
    ], string='Escala de Conceitos e Corte', default='scale_abc_r', required=True)

    @api.depends('min_subject_credits', 'max_external_credits_percent')
    def _compute_max_external_subject_credits(self):
        for record in self:
            record.max_external_subject_credits = (record.min_subject_credits * record.max_external_credits_percent) / 100.0

    # Governança de Alunos Especiais (Disciplinas Isoladas)
    allow_special_students = fields.Boolean(
        string='Permite Alunos Especiais no Programa',
        default=False,
        help='Indica se o programa admite alunos especiais para cursar disciplinas isoladas. Padrão False no MPTRCS.'
    )
    max_special_subjects_limit = fields.Integer(
        string='Limite Máximo de Disciplinas Isoladas',
        default=2,
        help='Quantidade máxima de disciplinas isoladas que um aluno especial pode cursar no programa.'
    )
    special_credit_validity_months = fields.Integer(
        string='Prazo Decadencial de Aproveitamento Especial (meses)',
        default=36,
        help='Prazo máximo em meses (padrão 36 meses / 3 anos) para requerer aproveitamento de disciplinas de aluno especial após ingresso regular.'
    )
    special_incorporation_workflow = fields.Selection([
        ('cpg_approval', 'Exige Parecer e Deliberação da CPG'),
        ('direct_request', 'Incorporação Direta via Requerimento')
    ], string='Workflow de Incorporação Especial', default='cpg_approval', required=True)
    special_transcript_fail_policy = fields.Selection([
        ('omit_on_regular', 'Omitir Reprovações e Não-Aproveitadas no Histórico Regular (Padrão MPTRCS)'),
        ('display_all', 'Exibir Todas as Ocorrências de Regime Especial')
    ], string='Política de Reprovações de Aluno Especial no Histórico', default='omit_on_regular', required=True)

    # Governança de Disciplinas Intra-IES vs. Extra-IES
    allow_intra_ies_credits = fields.Boolean(
        string='Permite Cursar Disciplinas Intra-IES',
        default=True,
        help='Permite que discentes regulares deste programa cursem disciplinas em outros PPGs da mesma instituição.'
    )
    max_intra_ies_credits_percent = fields.Float(
        string='Teto de Disciplinas Intra-IES (%)',
        default=0.0,
        help='Percentual máximo de créditos que podem vir de outros PPGs da mesma IES. 0.0 indica sem teto específico.'
    )
    intra_ies_advisor_approval_required = fields.Boolean(
        string='Exige Anuência do Orientador para Intra-IES',
        default=True
    )

    # Parametrizações de Domínio Específico
    proficiency_stage = fields.Selection([
        ('admission', 'Na Admissão (Entrada - IPEN)'),
        ('qualification', 'No Exame de Qualificação'),
        ('defense', 'No Momento da Defesa')
    ], string='Momento Exigência Proficiência', default='admission', required=True)

    teaching_internship_mode = fields.Selection([
        ('not_applicable', 'Inaplicável (Cursos Profissionais/Isentos)'),
        ('scholarship_only', 'Apenas Bolsistas'),
        ('mandatory_all', 'Obrigatório para Todos'),
        ('flexible_equivalence', 'Permite Equivalência / Estágio Supervisionado')
    ], string='Regra de Estágio de Docência (Portaria 221/2025)', default='not_applicable', required=True)

    ptt_validation_mode = fields.Selection([
        ('cpg_checklist', 'Checklist + Dupla Anuência + Pauta CPG (MPTRCS)'),
        ('qualis_prior', 'Avaliação Qualis Prévia (T1-T5)'),
        ('none', 'Sem Exigência de PTT (Acadêmico)')
    ], string='Modo de Validação do PTT', default='cpg_checklist', required=True)

    defense_location_policy = fields.Selection([
        ('onsite_mandatory', 'Presencial Obrigatório'),
        ('hybrid_allowed', 'Híbrido (Presença física aluno/presidente)'),
        ('fully_remote_allowed', '100% Remota Autorizada')
    ], string='Política de Modalidade da Defesa', default='hybrid_allowed', required=True)

    # Relacionamentos Dinâmicos (One2many)
    subject_rule_ids = fields.One2many(
        'op.curriculum.subject.rule',
        'curriculum_version_id',
        string='Regras de Disciplinas Obrigatórias'
    )
    committee_rule_ids = fields.One2many(
        'op.curriculum.committee.rule',
        'curriculum_version_id',
        string='Regras de Composição de Bancas'
    )

    is_active = fields.Boolean(
        string='Versão Vigente para Novos Editais',
        default=True
    )

    @api.constrains('max_months_defense', 'min_credits', 'min_subject_credits', 'thesis_credits', 'other_mandatory_credits', 'max_external_credits_percent')
    def _check_regimen_parameters(self):
        for record in self:
            if record.max_months_defense <= 0:
                raise ValidationError("O prazo máximo de titulação em meses deve ser superior a zero.")
            if record.min_credits <= 0:
                raise ValidationError("A exigência total de créditos deve ser um valor positivo.")
            if record.min_subject_credits < 0 or record.thesis_credits < 0 or record.other_mandatory_credits < 0:
                raise ValidationError("Os valores de créditos específicos não podem ser negativos.")
            if (record.min_subject_credits + record.thesis_credits + record.other_mandatory_credits) > record.min_credits:
                raise ValidationError(
                    f"A soma dos créditos em disciplinas ({record.min_subject_credits}), dissertação ({record.thesis_credits}) "
                    f"e outras atividades ({record.other_mandatory_credits}) supera os créditos totais exigidos ({record.min_credits})."
                )
            if record.max_external_credits_percent < 0 or record.max_external_credits_percent > 100:
                raise ValidationError("O percentual máximo de créditos externos deve estar entre 0% e 100%.")


class OpCurriculumSubjectRule(models.Model):
    _name = 'op.curriculum.subject.rule'
    _description = 'Regra de Disciplina Obrigatória por Currículo'

    curriculum_version_id = fields.Many2one(
        'op.curriculum.version',
        string='Versão Regimental',
        required=True,
        ondelete='cascade'
    )
    subject_id = fields.Many2one(
        'op.subject',
        string='Disciplina',
        required=True
    )
    scope = fields.Selection([
        ('program', 'Geral do Programa'),
        ('area', 'Específica de Área de Concentração')
    ], string='Escopo da Obrigatoriedade', default='program', required=True)

    area_name = fields.Char(
        string='Área de Concentração',
        help='Especificação da Área de Concentração quando o escopo for restrito por Área'
    )


class OpCurriculumCommitteeRule(models.Model):
    _name = 'op.curriculum.committee.rule'
    _description = 'Regra de Composição de Bancas e Comissões Julgadoras'

    curriculum_version_id = fields.Many2one(
        'op.curriculum.version',
        string='Versão Regimental',
        required=True,
        ondelete='cascade'
    )
    academic_level = fields.Selection([
        ('master', 'Mestrado'),
        ('phd', 'Doutorado')
    ], string='Nível de Formação', required=True, default='master')

    stage = fields.Selection([
        ('qualification', 'Exame de Qualificação'),
        ('seminar', 'Seminário de Área'),
        ('defense', 'Defesa Final')
    ], string='Rito Acadêmico', required=True, default='defense')

    min_titular_count = fields.Integer(
        string='Mínimo de Examinadores Titulares',
        default=3,
        required=True,
        help='Ex: 3 para Mestrado; 3 a 5 para Doutorado'
    )
    suplente_mode = fields.Selection([
        ('fixed_pair', 'Mínimo 2 Suplentes (1 Int / 1 Ext)'),
        ('one_per_titular', '1 Suplente por Titular'),
        ('custom', 'Quantidade Fixa')
    ], string='Regra de Suplentes', default='fixed_pair', required=True)

    advisor_vote_role = fields.Selection([
        ('voting_president', 'Preside e Vota (IPEN/Mackenzie)'),
        ('non_voting_president', 'Preside sem Voto (Não-Votante)'),
        ('examiner_only', 'Membro Votante sem Presidência')
    ], string='Papel e Voto do Orientador', default='voting_president', required=True)

    coadvisor_participation = fields.Selection([
        ('non_voting_additional', 'Membro Adicional sem Voto'),
        ('forbidden_with_advisor', 'Proibido se Orientador Presente'),
        ('full_voting_member', 'Membro Votante Integral')
    ], string='Participação do Coorientador', default='non_voting_additional', required=True)

    external_rule = fields.Selection([
        ('min_one_external', 'Mínimo 1 Externo ao PPG/IES'),
        ('min_two_external', 'Mínimo 2 Externos (Doutorado CDTN)'),
        ('majority_external', 'Maioria Externa ao PPG')
    ], string='Exigência de Membros Externos', default='min_one_external', required=True)

    allow_non_phd_member = fields.Boolean(
        string='Permite Especialista sem Doutorado',
        default=False,
        help='Permite especialistas com notório saber em Mestrados Profissionais'
    )
    non_phd_approval_level = fields.Selection([
        ('cpg_simple', 'Maioria Simples CPG'),
        ('cpg_qualified', '2/3 da CPG'),
        ('superior_council', 'CPG + Conselho Superior')
    ], string='Alçada de Aprovação de Não-Doutor', default='cpg_simple')


class OpStudent(models.Model):
    _inherit = 'op.student'

    curriculum_version_id = fields.Many2one(
        'op.curriculum.version',
        string='Versão Regimental (Ato Jurídico Perfeito)',
        help='Regimento ao qual o estudante foi vinculado no momento do ingresso'
    )

