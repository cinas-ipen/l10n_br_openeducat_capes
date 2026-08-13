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


class OpAcademicRequest(models.Model):
    _name = 'op.academic.request'
    _description = 'Requerimentos Acadêmicos do Portal Discente'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(
        string='Número do Requerimento',
        required=True,
        default='Novo',
        readonly=True,
        copy=False
    )
    student_id = fields.Many2one(
        'op.student',
        string='Discente Solicitante',
        required=True,
        tracking=True
    )
    current_curriculum_version_id = fields.Many2one(
        'op.curriculum.version',
        string='Regimento Curricular Atual',
        related='student_id.curriculum_version_id',
        store=True,
        readonly=True
    )
    request_type = fields.Selection([
        ('trancamento', 'Trancamento de Matrícula / Trancamento Contínuo'),
        ('prorrogacao', 'Prorrogação de Prazo para Defesa / Qualificação'),
        ('regime_migration', 'Opção de Migração de Regimento Curricular'),
        ('credit_transfer', 'Aproveitamento de Créditos Externos'),
        ('coadvisor_add', 'Indicação / Troca de Coorientador'),
        ('proficiencia', 'Homologação de Exame de Proficiência'),
        ('ptt_homologation', 'Homologação de Produto Técnico-Tecnológico (PTT)')
    ], string='Tipo de Requerimento', required=True, tracking=True)

    state = fields.Selection([
        ('draft', 'Rascunho'),
        ('submitted', 'Submetido'),
        ('under_review', 'Em Análise (Gabinete / CPG)'),
        ('approved', 'Aprovado / Deferido'),
        ('rejected', 'Indeferido'),
        ('cancelled', 'Cancelado')
    ], string='Situação do Requerimento', default='draft', tracking=True)

    target_curriculum_version_id = fields.Many2one(
        'op.curriculum.version',
        string='Novo Regimento Solicitado (Direito de Opção)',
        help='Utilizado exclusivamente no requerimento de migração de regimento'
    )
    requested_days = fields.Integer(
        string='Dias Solicitados (Prorrogação / Trancamento)',
        help='Prazo adicional em dias requerido pelo discente'
    )
    justification = fields.Text(
        string='Justificativa Fundamentada do Discente',
        required=True
    )
    advisor_approval = fields.Selection([
        ('pending', 'Pendente de Anuência'),
        ('approved', 'Aprovado pelo Orientador'),
        ('rejected', 'Rejeitado pelo Orientador')
    ], string='Anuência do Orientador', default='pending', tracking=True)

    cpg_meeting_id = fields.Many2one(
        'op.cpg.meeting',
        string='Pauta na Reunião CPG',
        tracking=True
    )
    resolution_notes = fields.Text(
        string='Parecer / Deliberação Final CPG',
        tracking=True
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'Novo') == 'Novo':
                vals['name'] = self.env['ir.sequence'].next_by_code('op.academic.request') or 'REQ-ACAD'
        return super().create(vals_list)

    def action_submit(self):
        for record in self:
            if record.state != 'draft':
                raise ValidationError("Apenas requerimentos em rascunho podem ser submetidos.")
            record.state = 'submitted'

    def action_approve(self):
        for record in self:
            record.state = 'approved'
            # Se for migração de regimento, atualiza o Ato Jurídico Perfeito do discente
            if record.request_type == 'regime_migration' and record.target_curriculum_version_id:
                record.student_id.curriculum_version_id = record.target_curriculum_version_id

    def action_reject(self):
        for record in self:
            record.state = 'rejected'
