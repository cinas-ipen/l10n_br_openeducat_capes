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


def _parse_brazilian_name(name):
    """Decompõe nomes completos em first_name, middle_name e last_name.
    Remove honoríficos acadêmicos e preserva preposições e nomes do meio."""
    if not name:
        return "", "", ""
    clean = name.strip()
    for prefix in ['Prof. Dr.', 'Profa. Dra.', 'Profª. Drª.', 'Prof.', 'Profa.', 'Profª.', 'Dr.', 'Dra.', 'Drª.']:
        if clean.startswith(prefix + ' '):
            clean = clean[len(prefix):].strip()
            break
    parts = clean.split()
    if len(parts) == 0:
        return "", "", ""
    elif len(parts) == 1:
        return parts[0], "", ""
    elif len(parts) == 2:
        return parts[0], "", parts[1]
    else:
        return parts[0], " ".join(parts[1:-1]), parts[-1]


class OpFaculty(models.Model):
    _inherit = 'op.faculty'

    work_regime = fields.Selection([
        ('exclusive', 'Dedicação Exclusiva (DE)'),
        ('fulltime', 'Tempo Integral (40h)'),
        ('parttime', 'Tempo Parcial (<40h)')
    ], string='Regime de Dedicação', default='fulltime')

    workload = fields.Integer(
        string='Carga Horária Semanal (horas)',
        default=40,
        help='Carga horária semanal dedicada à instituição'
    )
    faculty_status = fields.Selection([
        ('active', 'Ativo'),
        ('inactive', 'Inativo'),
        ('deceased', 'Falecido')
    ], string='Situação Docente', default='active')

    is_retired = fields.Boolean(
        string='Indicação de Aposentadoria',
        default=False
    )
    degree_area = fields.Char(
        string='Área de Conhecimento da Titulação',
        help='Área do conhecimento da maior titulação'
    )
    degree_level = fields.Selection([
        ('master', 'Mestrado'),
        ('phd', 'Doutorado')
    ], string='Nível Acadêmico da Titulação Máxima', default='phd')

    degree_ies = fields.Char(
        string='IES da Titulação',
        help='Instituição onde obteve o título máximo'
    )

    # Relacionamentos com Áreas de Concentração e Linhas de Pesquisa
    concentration_area_ids = fields.Many2many(
        'op.program.concentration.area',
        'op_area_faculty_rel',
        'faculty_id',
        'area_id',
        string='Áreas de Concentração do PPG'
    )
    research_line_ids = fields.Many2many(
        'op.program.research.line',
        'op_line_faculty_rel',
        'faculty_id',
        'line_id',
        string='Linhas de Pesquisa do PPG'
    )

    # Vínculos com Orientandos
    advisee_ids = fields.One2many(
        'op.student',
        'advisor_id',
        string='Orientandos Principais'
    )
    coadvisee_ids = fields.One2many(
        'op.student',
        'coadvisor_id',
        string='Coorientandos'
    )

    # Contadores KPI para os Smart Buttons (Core)
    active_advisees_count = fields.Integer(
        string='Orientandos Ativos',
        compute='_compute_advisees_count'
    )
    alumni_advisees_count = fields.Integer(
        string='Egressos Titulados',
        compute='_compute_advisees_count'
    )
    subject_count = fields.Integer(
        string='Disciplinas Ministradas',
        compute='_compute_subject_count'
    )

    @api.depends('advisee_ids.capes_status', 'coadvisee_ids.capes_status')
    def _compute_advisees_count(self):
        for record in self:
            all_students = record.advisee_ids | record.coadvisee_ids
            record.active_advisees_count = len(all_students.filtered(lambda s: s.capes_status == 'enrolled'))
            record.alumni_advisees_count = len(all_students.filtered(lambda s: s.capes_status == 'graduated' or s.student_category == 'alumni'))

    @api.depends('faculty_subject_ids')
    def _compute_subject_count(self):
        for record in self:
            record.subject_count = len(record.faculty_subject_ids)

    def action_view_active_advisees(self):
        self.ensure_one()
        return {
            'name': f'Orientandos Ativos - {self.name}',
            'type': 'ir.actions.act_window',
            'res_model': 'op.student',
            'view_mode': 'list,form',
            'domain': ['|', ('advisor_id', '=', self.id), ('coadvisor_id', '=', self.id), ('capes_status', '=', 'enrolled')],
            'context': {'default_advisor_id': self.id},
        }

    def action_view_alumni_advisees(self):
        self.ensure_one()
        return {
            'name': f'Egressos e Titulados Orientados - {self.name}',
            'type': 'ir.actions.act_window',
            'res_model': 'op.student',
            'view_mode': 'list,form',
            'domain': ['|', ('advisor_id', '=', self.id), ('coadvisor_id', '=', self.id), ('capes_status', '=', 'graduated')],
            'context': {'default_advisor_id': self.id},
        }

    def action_view_subjects(self):
        self.ensure_one()
        return {
            'name': f'Disciplinas Ministradas - {self.name}',
            'type': 'ir.actions.act_window',
            'res_model': 'op.subject',
            'view_mode': 'list,form',
            'domain': [('id', 'in', self.faculty_subject_ids.ids)],
        }

    @api.onchange('first_name', 'middle_name', 'last_name')
    def _onchange_name(self):
        fname = self.first_name or ""
        mname = self.middle_name or ""
        lname = self.last_name or ""
        if fname or mname or lname:
            self.name = " ".join(filter(None, [fname, mname, lname]))
        else:
            self.name = "Novo Docente"

    @api.onchange('name')
    def _onchange_full_name(self):
        if self.name and self.name != "Novo Docente":
            fn, mn, ln = _parse_brazilian_name(self.name)
            if fn:
                self.first_name = fn
            self.middle_name = mn
            if ln:
                self.last_name = ln

    @api.constrains('workload')
    def _check_workload(self):
        for record in self:
            if record.workload < 0:
                raise ValidationError("A carga horária semanal do docente não pode ser negativa.")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            name = vals.get('name')
            fname = vals.get('first_name')
            mname = vals.get('middle_name')
            lname = vals.get('last_name')

            if name and (not fname or not mname or not lname):
                parsed_fn, parsed_mn, parsed_ln = _parse_brazilian_name(name)
                if not fname:
                    vals['first_name'] = parsed_fn
                if not mname and parsed_mn:
                    vals['middle_name'] = parsed_mn
                if not lname and parsed_ln:
                    vals['last_name'] = parsed_ln

            fn = vals.get('first_name') or ""
            mn = vals.get('middle_name') or ""
            ln = vals.get('last_name') or ""
            if fn or mn or ln:
                vals['name'] = " ".join(filter(None, [fn, mn, ln]))

        return super(OpFaculty, self).create(vals_list)

    def write(self, vals):
        if 'name' in vals and not ('first_name' in vals and 'middle_name' in vals and 'last_name' in vals):
            fn, mn, ln = _parse_brazilian_name(vals['name'])
            if 'first_name' not in vals and fn:
                vals['first_name'] = fn
            if 'middle_name' not in vals:
                vals['middle_name'] = mn
            if 'last_name' not in vals and ln:
                vals['last_name'] = ln
        elif any(f in vals for f in ('first_name', 'middle_name', 'last_name')):
            for rec in self:
                fn = vals.get('first_name', rec.first_name) or ""
                mn = vals.get('middle_name', rec.middle_name) or ""
                ln = vals.get('last_name', rec.last_name) or ""
                vals['name'] = " ".join(filter(None, [fn, mn, ln]))
        return super(OpFaculty, self).write(vals)
