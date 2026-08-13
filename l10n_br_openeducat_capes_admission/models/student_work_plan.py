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


class OpStudentWorkPlan(models.Model):
    _name = 'op.student.work_plan'
    _description = 'Plano de Trabalho Discente (Workflow de Submissão e Ética CEP)'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(
        string='Título do Plano de Trabalho',
        required=True,
        tracking=True,
        help='Título preliminar do projeto de tese / dissertação'
    )
    student_id = fields.Many2one(
        'op.student',
        string='Discente Solicitante',
        required=True,
        tracking=True
    )
    advisor_id = fields.Many2one(
        'op.faculty',
        string='Orientador Principal',
        related='student_id.advisor_id',
        store=True,
        readonly=True
    )
    research_line = fields.Char(
        string='Linha de Pesquisa',
        required=True,
        help='Linha de pesquisa oficial do programa na qual o plano se insere'
    )
    summary = fields.Text(
        string='Resumo e Objetivos',
        required=True
    )
    methodology = fields.Text(
        string='Metodologia de Pesquisa',
        required=True
    )
    ptt_prediction = fields.Text(
        string='Previsão do Produto Técnico-Tecnológico (PTT)',
        help='Previsão de patentes, registros de software, protótipos ou guias técnicos'
    )
    attachment_pdf = fields.Binary(
        string='PDF Completo do Plano de Trabalho',
        attachment=True,
        required=True,
        help='Arquivo PDF estruturado contendo o plano de trabalho'
    )

    # Workflow e Anuência do Orientador
    advisor_ok = fields.Boolean(
        string='Anuência Eletrônica do Orientador (OK)',
        default=False,
        tracking=True,
        help='Aceite formal do orientador autorizando a tramitação para a CPG'
    )

    # Fila de Avaliação CPG
    evaluator_id = fields.Many2one(
        'res.partner',
        string='Parecerista / Avaliador Designado CPG',
        tracking=True
    )
    cpg_meeting_id = fields.Many2one(
        'op.cpg.meeting',
        string='Homologação em Reunião CPG',
        tracking=True
    )

    # As 4 Categorias de Parecer do Avaliador
    opinion_category = fields.Selection([
        ('approved', 'a) Aprovado Satisfatório sem Ressalvas'),
        ('revisions', 'b) Aprovado com Revisões Exigidas'),
        ('cep_pending', 'c) Aprovado com Pendência de CEP/CEUA (Bloqueia Bancas)'),
        ('rejected', 'd) Reprovado sem Direito a Revisão')
    ], string='Categoria de Parecer do Avaliador', tracking=True)

    evaluator_opinion = fields.Text(
        string='Parecer Técnico do Avaliador',
        tracking=True
    )

    # Trava Ética CEP / CEUA
    cep_document = fields.Binary(
        string='Parecer Consubstanciado CEP/CEUA (Upload)',
        attachment=True,
        help='Comprovante de aprovação da Plataforma Brasil / CEP / CEUA'
    )
    cep_approved = fields.Boolean(
        string='Aprovação CEP/CEUA Validada',
        default=False,
        tracking=True,
        help='Validação do parecer ético liberando o discente para bancas'
    )

    state = fields.Selection([
        ('draft', 'Rascunho'),
        ('submitted', 'Submetido (Aguardando OK Orientador)'),
        ('advisor_approved', 'Aprovado pelo Orientador (Fila Triagem Secretaria)'),
        ('under_evaluation', 'Em Avaliação pelo Parecerista'),
        ('revisions_requested', 'Em Revisão pelo Discente'),
        ('cep_pending', 'Aprovado Condicional (Pendente CEP/CEUA)'),
        ('homologated', 'Homologado CPG'),
        ('rejected', 'Reprovado')
    ], string='Situação do Plano', default='draft', tracking=True)

    def action_submit_by_student(self):
        """Submissão inicial do aluno para aceite do orientador."""
        for record in self:
            if record.state != 'draft':
                raise ValidationError("Apenas planos em rascunho podem ser submetidos.")
            record.state = 'submitted'

    def action_advisor_approve(self):
        """Aceite do orientador liberando para a secretaria/CPG."""
        for record in self:
            record.advisor_ok = True
            record.state = 'advisor_approved'

    def action_assign_evaluator(self):
        """Designação de parecerista pela CPG."""
        for record in self:
            if not record.evaluator_id:
                raise ValidationError("Indique o parecerista designado antes de alterar a situação.")
            record.state = 'under_evaluation'

    def action_register_opinion(self):
        """Registro do parecer do avaliador."""
        for record in self:
            if not record.opinion_category:
                raise ValidationError("Selecione a categoria de parecer do avaliador.")
            
            if record.opinion_category == 'approved':
                record.state = 'homologated'
            elif record.opinion_category == 'revisions':
                record.state = 'revisions_requested'
            elif record.opinion_category == 'cep_pending':
                record.state = 'cep_pending'
            elif record.opinion_category == 'rejected':
                record.state = 'rejected'

    def action_validate_cep(self):
        """Validação do parecer CEP/CEUA pelo setor de pesquisa/CPG."""
        for record in self:
            if not record.cep_document:
                raise ValidationError("É necessário realizar o upload do comprovante de aprovação CEP/CEUA antes de validar.")
            record.cep_approved = True
            record.state = 'homologated'
