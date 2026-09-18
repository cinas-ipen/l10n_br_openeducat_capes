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


class OpFacultyProgramLink(models.Model):
    _name = 'op.faculty.program.link'
    _description = 'Vínculo e Credenciamento Docente no Programa (PPG)'
    _order = 'faculty_id, program_id'

    faculty_id = fields.Many2one(
        'op.faculty',
        string='Docente',
        required=True,
        ondelete='cascade'
    )
    link_type = fields.Selection([
        ('internal', 'Programa Local (Mesma IES)'),
        ('external', 'Programa Externo (Outra IES)')
    ], string='Tipo de Vínculo', default='internal', required=True)

    program_id = fields.Many2one(
        'op.program.capes',
        string='Programa Local (PPG)',
        required=False,
        ondelete='cascade'
    )
    external_ies_name = fields.Char(
        string='IES do Programa Externo',
        help='Nome da Instituição de Ensino Superior externa (ex: USP, UNICAMP)'
    )
    external_program_name = fields.Char(
        string='Nome do Programa Externo',
        help='Nome do Programa de Pós-Graduação na IES externa'
    )
    external_snpg_code = fields.Char(
        string='Código SNPG / CAPES',
        help='Código do programa externo no Sistema Nacional de Pós-Graduação'
    )
    faculty_category = fields.Selection([
        ('permanent', 'Permanente (DP)'),
        ('collaborator', 'Colaborador (DC)'),
        ('visiting', 'Visitante (DV)'),
        ('assistant', 'Assistente')
    ], string='Categoria de Atuação', default='permanent', required=True)

    weekly_hours = fields.Integer(
        string='Carga Horária Semanal (h)',
        default=10,
        help='Carga horária semanal dedicada a este programa de pós-graduação'
    )

    active_advisees_count = fields.Integer(
        string='Número de Orientandos Ativos',
        compute='_compute_active_advisees_count',
        store=True,
        help='Número de discentes matriculados com este orientador no programa'
    )
    category_ledger_ids = fields.One2many(
        'op.faculty.category.ledger',
        'program_link_id',
        string='Histórico de Categorias de Credenciamento (Ledger)'
    )

    @api.depends('link_type', 'program_id', 'external_program_name', 'external_ies_name', 'faculty_category')
    def _compute_display_name(self):
        cat_labels = {
            'permanent': 'Permanente',
            'collaborator': 'Colaborador',
            'visiting': 'Visitante',
            'assistant': 'Assistente',
        }
        for record in self:
            cat = cat_labels.get(record.faculty_category, record.faculty_category or '')
            if record.link_type == 'internal':
                p_name = record.program_id.short_name or record.program_id.name or 'Programa Local'
                record.display_name = f"{p_name} ({cat})"
            else:
                p_name = record.external_program_name or 'Programa Externo'
                ies = f" - {record.external_ies_name}" if record.external_ies_name else ""
                record.display_name = f"{p_name}{ies} [Externo - {cat}]"

    @api.constrains('faculty_id', 'program_id', 'link_type', 'external_program_name', 'external_ies_name')
    def _check_link_consistency(self):
        for record in self:
            if record.link_type == 'internal':
                if not record.program_id:
                    raise ValidationError("Para vínculos locais (mesma IES), selecione obrigatoriamente o Programa de Pós-Graduação (PPG).")
                duplicates = self.search([
                    ('id', '!=', record.id),
                    ('faculty_id', '=', record.faculty_id.id),
                    ('link_type', '=', 'internal'),
                    ('program_id', '=', record.program_id.id)
                ])
                if duplicates:
                    raise ValidationError(f"O docente já possui vínculo cadastrado com o programa {record.program_id.name}.")
            elif record.link_type == 'external':
                if not record.external_program_name:
                    raise ValidationError("Para vínculos externos, informe o nome do Programa de Pós-Graduação externo.")
                if not record.external_ies_name:
                    raise ValidationError("Para vínculos externos, informe a Instituição de Ensino Superior (IES) externa.")

    @api.depends('faculty_id', 'program_id')
    def _compute_active_advisees_count(self):
        Student = self.env['op.student']
        for record in self:
            if record.faculty_id and record.program_id:
                count = Student.search_count([
                    ('advisor_id', '=', record.faculty_id.id),
                    ('curriculum_version_id.program_id', '=', record.program_id.id),
                    ('capes_status', '=', 'enrolled')
                ])
                record.active_advisees_count = count
            else:
                record.active_advisees_count = 0


class OpFacultyCategoryLedger(models.Model):
    _name = 'op.faculty.category.ledger'
    _description = 'Livro-Razão de Categorias Docentes (Append-Only)'
    _order = 'start_date desc, id desc'

    program_link_id = fields.Many2one(
        'op.faculty.program.link',
        string='Vínculo Docente-Programa',
        required=True,
        ondelete='restrict'
    )
    program_id = fields.Many2one(
        'op.program.capes',
        string='Programa de Pós-Graduação',
        related='program_link_id.program_id',
        store=True,
        readonly=True,
        index=True
    )
    category = fields.Selection([
        ('permanent', 'Permanente'),
        ('collaborator', 'Colaborador'),
        ('visiting', 'Visitante'),
        ('assistant', 'Assistente')
    ], string='Categoria de Atuação', required=True)

    start_date = fields.Date(
        string='Início do Credenciamento',
        required=True,
        default=fields.Date.context_today
    )
    end_date = fields.Date(
        string='Fim do Credenciamento',
        help='Data limite da validade da portaria/credenciamento (ex: teto 2 anos no IPEN)'
    )
    document_ref = fields.Char(
        string='Portaria / Ata CPG de Credenciamento',
        help='Referência do ato administrativo formal de credenciamento'
    )
    notes = fields.Text(
        string='Observações e Deliberação'
    )

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for rec in records:
            if rec.program_link_id and rec.category:
                rec.program_link_id.faculty_category = rec.category
        return records

    @api.constrains('start_date', 'end_date')
    def _check_accreditation_dates(self):
        for record in self:
            if record.start_date and record.end_date:
                if record.end_date < record.start_date:
                    raise ValidationError("A data de término do credenciamento docente deve ser posterior à data de início.")

    def unlink(self):
        """Garante a imutabilidade do Livro-Razão de Categorias Docentes (Append-Only)."""
        raise UserError("O Livro-Razão de credenciamento docente opera estritamente em modo append-only. "
                        "Operações de exclusão são terminantemente proibidas para preservação do histórico CAPES.")
