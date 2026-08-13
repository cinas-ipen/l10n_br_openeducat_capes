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


class CapesThesis(models.Model):
    _name = 'capes.thesis'
    _description = 'Trabalho de Conclusão e Ritos Acadêmicos (Qualificação / Defesa)'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'defense_date desc, id desc'

    capes_id = fields.Integer(
        string='Identificador CAPES',
        help='ID numérico do registro na CAPES / Sucupira'
    )
    student_id = fields.Many2one(
        'op.student',
        string='Discente Solicitante',
        required=True,
        tracking=True
    )
    curriculum_version_id = fields.Many2one(
        'op.curriculum.version',
        string='Versão Regimental Ativa (Ato Perfeito)',
        related='student_id.curriculum_version_id',
        store=True,
        readonly=True
    )
    work_plan_id = fields.Many2one(
        'op.student.work_plan',
        string='Plano de Trabalho Homologado',
        required=True,
        tracking=True,
        help='Plano de trabalho discente homologado pela CPG'
    )
    project_id = fields.Many2one(
        'capes.research.project',
        string='Projeto de Pesquisa Vinculado'
    )
    stage = fields.Selection([
        ('seminar_area', 'Seminário de Área'),
        ('qualification', 'Exame de Qualificação Clássico'),
        ('defense', 'Defesa Pública Final')
    ], string='Rito Acadêmico Registrado', required=True, default='defense', tracking=True)

    doc_type = fields.Selection([
        ('dissertation', 'Dissertação de Mestrado'),
        ('thesis', 'Tese de Doutorado'),
        ('tech_product', 'Produto Tecnológico / Relatório Técnico')
    ], string='Tipo de Documento Final', required=True, default='dissertation', tracking=True)

    defense_date = fields.Datetime(
        string='Data e Horário da Sessão',
        required=True,
        tracking=True
    )
    title = fields.Char(
        string='Título Final Aprovado em Ata',
        required=True,
        tracking=True
    )
    title_alt = fields.Char(
        string='Título Traduzido (Inglês)',
        tracking=True
    )
    abstract_main = fields.Text(
        string='Resumo no Idioma Principal'
    )
    abstract_alt = fields.Text(
        string='Resumo em Inglês (Abstract)'
    )
    keywords_main = fields.Char(
        string='Palavras-chave no Idioma Principal',
        help='Vocabulário controlado separado por ponto e vírgula'
    )
    keywords_alt = fields.Char(
        string='Palavras-chave em Inglês'
    )

    presentation_time_minutes = fields.Integer(
        string='Tempo de Exposição do Candidato (min)',
        default=50,
        help='Teto regimental de exposição (ex: 50 min no IPEN)'
    )
    arguing_time_minutes = fields.Integer(
        string='Tempo de Arguição por Examinador (min)',
        default=40,
        help='Teto regimental de arguição por examinador (ex: 40 min)'
    )

    # Integração Repositório Institucional (Fonte Ouro / DSpace)
    repository_url = fields.Char(
        string='Handle / URI no Repositório (DSpace)',
        tracking=True,
        help='Handle permanente gerado pela biblioteca (ex: http://repositorio.ipen.br/handle/12345/6789)'
    )
    deposit_date = fields.Date(
        string='Data do Depósito Definitivo no DSpace'
    )

    status = fields.Selection([
        ('draft', 'Rascunho'),
        ('scheduled', 'Agendado'),
        ('approved', 'Aprovado na Banca'),
        ('disapproved', 'Reprovado na Banca'),
        ('deposit_pending', 'Pendente de Depósito DSpace'),
        ('homologated', 'Homologado / Titulado')
    ], string='Situação do Rito', default='draft', tracking=True)

    committee_ids = fields.One2many(
        'capes.thesis.committee',
        'thesis_id',
        string='Membros da Comissão Examinadora'
    )

    def action_schedule_rite(self):
        """Executa as travas prévias de elegibilidade antes de agendar o rito acadêmico."""
        Ledger = self.env['op.student.credit.ledger']
        for record in self:
            curriculum = record.curriculum_version_id
            if not curriculum:
                raise ValidationError("O discente deve possuir uma Versão Regimental ativa vinculada.")

            # 1. Trava do Plano de Trabalho Homologado
            if record.work_plan_id.state != 'homologated':
                raise ValidationError("O agendamento do rito exige que o Plano de Trabalho do discente esteja com o status 'Homologado CPG'.")

            # 2. Trava Ética CEP/CEUA
            if record.work_plan_id.opinion_category == 'cep_pending' and not record.work_plan_id.cep_approved:
                raise ValidationError("O Plano de Trabalho possui pendência ética de CEP/CEUA não liberada. Faça o upload do parecer consubstanciado de aprovação.")

            # 3. Trava de Proficiência Linguística (se exigida no rito ou na admissão)
            if curriculum.proficiency_stage == 'qualification' and record.stage == 'qualification':
                if record.student_id.english_proficiency_status != 'approved':
                    raise ValidationError("O regimento do curso exige a comprovação de proficiência em inglês aprovada no Exame de Qualificação.")
            elif curriculum.proficiency_stage == 'defense' and record.stage == 'defense':
                if record.student_id.english_proficiency_status != 'approved':
                    raise ValidationError("O regimento do curso exige a comprovação de proficiência em inglês aprovada para a Defesa Final.")

            # 4. Trava de Créditos Cumpridos (apenas para Defesa Final)
            if record.stage == 'defense':
                total_credits = sum(Ledger.search([
                    ('student_id', '=', record.student_id.id),
                    ('is_approved', '=', True)
                ]).mapped('credits'))
                if total_credits < curriculum.min_credits:
                    raise ValidationError(f"Integralização de créditos insuficiente. O aluno possui {total_credits} créditos conquistados, mas o regimento exige o mínimo de {curriculum.min_credits} créditos.")

            record.status = 'scheduled'

    def action_approve_in_board(self):
        """Registra a aprovação na banca e encaminha para depósito no DSpace em caso de defesa final."""
        for record in self:
            if record.stage == 'defense':
                record.status = 'deposit_pending'
            else:
                record.status = 'approved'

    def action_disapprove_in_board(self):
        """Registra a reprovação na banca."""
        for record in self:
            record.status = 'disapproved'

    def action_homologate_deposit(self):
        """Verifica a averbação do Handle do DSpace e titula o discente."""
        for record in self:
            if not record.repository_url or not record.repository_url.strip():
                raise ValidationError("É obrigatório informar a URL/Handle permanente do repositório DSpace para homologar o depósito e a titulação.")

            record.status = 'homologated'
            record.student_id.capes_status = 'graduated'
            record.student_id.status_date = fields.Date.context_today(self)
