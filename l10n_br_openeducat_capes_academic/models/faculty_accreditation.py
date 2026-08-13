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
    _order = 'program_id, faculty_id'

    faculty_id = fields.Many2one(
        'op.faculty',
        string='Docente',
        required=True,
        ondelete='cascade'
    )
    program_id = fields.Many2one(
        'op.program.capes',
        string='Programa de Pós-Graduação',
        required=True,
        ondelete='cascade'
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

    _sql_constraints = [
        ('faculty_program_unique', 'unique(faculty_id, program_id)', 'O docente já possui vínculo cadastrado com este Programa de Pós-Graduação.')
    ]

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
