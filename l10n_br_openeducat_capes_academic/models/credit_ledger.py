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
from odoo.exceptions import UserError, ValidationError


class OpStudentCreditLedger(models.Model):
    _name = 'op.student.credit.ledger'
    _description = 'Livro-Razão Acadêmico de Créditos (Append-Only)'
    _order = 'date_earned desc, id desc'

    student_id = fields.Many2one(
        'op.student',
        string='Discente',
        required=True,
        ondelete='restrict',
        index=True
    )
    curriculum_version_id = fields.Many2one(
        'op.curriculum.version',
        string='Versão Regimental Ativa (Ato Perfeito)',
        required=True,
        help='Regimento sob o qual o crédito foi efetivamente conquistado'
    )
    program_id = fields.Many2one(
        'op.program.capes',
        string='Programa CAPES',
        related='curriculum_version_id.program_id',
        store=True,
        index=True
    )
    credit_type = fields.Selection([
        ('subject', 'Disciplinas Regulares'),
        ('subject_internal', 'Disciplinas do Próprio Programa'),
        ('subject_intra_ies', 'Disciplinas de outros PPGs da mesma IES (100% Equivalência)'),
        ('subject_special_quarantine', 'Créditos em Quarentena (Aluno Especial)'),
        ('subject_special_incorporated', 'Créditos de Aluno Especial Incorporados (Homologados CPG)'),
        ('subject_extra_ies', 'Disciplinas Externas de Outras IES (Com Equivalência)'),
        ('apo', 'Atividades Programadas Obrigatórias (APO) / PTT'),
        ('milestone', 'Créditos por Qualificação e Defesa'),
        ('external', 'Aproveitamento de Créditos Externos')
    ], string='Natureza do Crédito', required=True, index=True)

    incorporation_request_id = fields.Many2one(
        'op.special.credit.incorporation.request',
        string='Requerimento de Incorporação CPG',
        index=True,
        help='Vínculo formal com o processo de aproveitamento homologado pela CPG'
    )
    original_program_id = fields.Many2one(
        'op.program.capes',
        string='Programa Ofertante de Origem',
        help='Programa acadêmico que ofertou a disciplina originalmente'
    )

    subject_id = fields.Many2one(
        'op.subject',
        string='Disciplina'
    )
    course_name = fields.Char(
        string='Denominação da Atividade / Disciplina',
        required=True,
        help='Nome oficial da disciplina ou atividade no momento do encerramento'
    )
    credits = fields.Float(
        string='Unidades de Crédito',
        required=True,
        help='Quantidade de créditos concedidos no lançamento'
    )
    hours = fields.Float(
        string='Carga Horária Computada (horas)',
        compute='_compute_hours',
        store=True,
        help='Carga horária calculada dinamicamente via razão de crédito do regimento'
    )
    grade_concept = fields.Char(
        string='Conceito / Nota Obtida',
        help='Ex: A, B, C, D ou nota numérica'
    )
    is_approved = fields.Boolean(
        string='Aprovado / Homologado',
        default=True
    )
    date_earned = fields.Date(
        string='Data da Conquista / Homologação',
        required=True,
        default=fields.Date.context_today
    )
    origin_ref = fields.Char(
        string='Documento de Origem / Ata / Código de Turma',
        help='Referência formal da turma, ata CPG ou processo de aproveitamento'
    )
    notes = fields.Text(
        string='Observações e Histórico Auditável'
    )

    @api.depends('credits', 'curriculum_version_id.credit_hour_ratio')
    def _compute_hours(self):
        for record in self:
            ratio = record.curriculum_version_id.credit_hour_ratio or 15
            record.hours = record.credits * ratio

    def unlink(self):
        """Garante a imutabilidade absoluta do Livro-Razão de Créditos (Append-Only)."""
        raise UserError("O Livro-Razão de créditos acadêmicos opera estritamente em modo append-only. "
                        "Operações de exclusão são terminantemente proibidas para preservação do Ato Jurídico Perfeito.")
