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

    name = fields.Char(string='Nome da Versão Regimental', required=True, help='Ex: Regimento IPEN 2024, Regimento CDTN 2026')
    program_id = fields.Many2one('op.program.capes', string='Programa de Pós-Graduação', required=True, ondelete='cascade')

    # Prazos Temporais e Cronometria
    max_months_defense = fields.Integer(string='Prazo Máximo Titulação (meses)', default=24, required=True, help='Ex: 24 para Mestrado, 48 para Doutorado')
    max_extension_days = fields.Integer(string='Teto Máximo Prorrogação (dias)', default=90)
    max_days_post_defense_deposit = fields.Integer(string='Prazo Depósito Final Pós-Defesa (dias)', default=30)
    presentation_max_minutes = fields.Integer(string='Tempo Máximo Exposição (min)', default=50)
    arguing_max_minutes_per_member = fields.Integer(string='Tempo Máximo Arguição p/ Membro (min)', default=40)

    # Regras de Trancamento e Flexibilidade
    max_trancamento_days = fields.Integer(string='Prazo Máximo de Trancamento Contínuo (dias)', default=365)
    block_first_semester_trancamento = fields.Boolean(string='Bloqueio Trancamento 1º Semestre', default=False)
    retorno_rule = fields.Selection([
        ('current_matrix', 'Vinculação à Matriz Vigente no Retorno')
    ], string='Regra de Retorno e Estrutura', default='current_matrix', required=True)

    # Matriz de Carga Horária e Escala de Avaliação
    min_credits = fields.Integer(string='Créditos Totais Exigidos', default=100, required=True)
    credit_hour_ratio = fields.Integer(string='Horas por Unidade de Crédito', default=15, required=True, help='15h (IPEN/CDTN) ou 12h (Mackenzie)')
    grading_scale_type = fields.Selection([
        ('scale_abc_r', 'Conceitos A, B, C (Aprovados) e R (Reprovado)'),
        ('scale_abcd_rf', 'Conceitos A, B, C, D (Aprovados) e R, F (Reprovados)')
    ], string='Escala de Conceitos e Corte', default='scale_abc_r', required=True)

    # Parametrizações de Domínio Específico
    proficiency_stage = fields.Selection([
        ('admission', 'Na Admissão (Entrada - IPEN/USP)'),
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
    subject_rule_ids = fields.One2many('op.curriculum.subject.rule', 'curriculum_version_id', string='Regras de Disciplinas Obrigatórias')
    committee_rule_ids = fields.One2many('op.curriculum.committee.rule', 'curriculum_version_id', string='Regras de Composição de Bancas')

    is_active = fields.Boolean(string='Versão Vigente para Novos Editais', default=True)

    @api.constrains('max_months_defense', 'min_credits')
    def _check_regimen_parameters(self):
        for record in self:
            if record.max_months_defense <= 0:
                raise ValidationError("O prazo máximo de titulação em meses deve ser superior a zero.")
            if record.min_credits <= 0:
                raise ValidationError("A exigência total de créditos deve ser um valor positivo.")
