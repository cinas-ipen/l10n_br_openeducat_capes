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


class OpStudent(models.Model):
    _inherit = 'op.student'

    company_id = fields.Many2one(
        'res.company',
        string='Instituição de Ensino (IES)',
        default=lambda self: self.env.company,
        required=True,
        index=True,
        help='IES mantenedora soberana do Registro Acadêmico (RA) do discente'
    )

    program_id = fields.Many2one(
        'op.program.capes',
        string='Programa de Pós-Graduação (PPG)',
        index=True,
        help='Programa de Pós-Graduação (CAPES/SNPG) ao qual o discente está filiado.'
    )


    student_category = fields.Selection([
        ('regular', 'Regular'),
        ('special', 'Aluno Especial (Disciplinas Isoladas)'),
        ('alumni', 'Egresso / Titulado')
    ], string='Categoria Discente', default='regular')

    ra_number = fields.Char(
        string='Registro Acadêmico (RA)',
        related='gr_no',
        store=True,
        readonly=False,
        help='Identificador institucional único e permanente na IES (espelha gr_no)'
    )
    code = fields.Char(
        string='Código / RA',
        related='ra_number',
        store=False,
        readonly=True,
        help='Identificador institucional de compatibilidade com relatórios e views legadas'
    )

    capes_status = fields.Selection([
        ('enrolled', 'Matriculado'),
        ('abandon', 'Abandono'),
        ('dismissed', 'Desligado'),
        ('pending_dismissal', 'Desligamento Em Andamento'),
        ('graduated', 'Titulado'),
        ('deceased', 'Falecido')
    ], string='Situação Discente CAPES', default='enrolled')

    admission_date = fields.Date(
        string='Data de Ingresso Oficial',
        required=True,
        default=fields.Date.context_today,
        help='Data de efetivação da primeira matrícula regular'
    )
    status_date = fields.Date(
        string='Data da Situação',
        default=fields.Date.context_today,
        help='Data da última alteração de status do discente'
    )

    advisor_id = fields.Many2one(
        'op.faculty',
        string='Orientador Principal',
        help='Docente credenciado atuando como orientador principal'
    )
    coadvisor_id = fields.Many2one(
        'op.faculty',
        string='Coorientador',
        help='Docente credenciado atuando como coorientador'
    )

    # Controle de Proficiência Linguística (GoPG / DAV)
    english_proficiency_status = fields.Selection([
        ('pending', 'Pendente'),
        ('approved', 'Aprovado'),
        ('exempt', 'Isento')
    ], string='Proficiência em Inglês', default='pending', required=True)

    portuguese_proficiency_status = fields.Selection([
        ('not_applicable', 'Não Aplicável'),
        ('pending', 'Pendente'),
        ('approved', 'Aprovado')
    ], string='Proficiência em Português (Estrangeiros)', default='not_applicable', required=True)

    # Contadores e Métodos de Acesso 360° (Core)
    course_count = fields.Integer(
        string='Vínculos de Curso',
        compute='_compute_course_count'
    )

    @api.depends('course_detail_ids')
    def _compute_course_count(self):
        for record in self:
            record.course_count = len(record.course_detail_ids)

    def action_view_courses(self):
        self.ensure_one()
        return {
            'name': f'Vínculos de Curso - {self.name}',
            'type': 'ir.actions.act_window',
            'res_model': 'op.student.course',
            'view_mode': 'list,form',
            'domain': [('student_id', '=', self.id)],
            'context': {'default_student_id': self.id},
        }

    @api.onchange('first_name', 'middle_name', 'last_name')
    def _onchange_name(self):
        fname = self.first_name or ""
        mname = self.middle_name or ""
        lname = self.last_name or ""
        if fname or mname or lname:
            self.name = " ".join(filter(None, [fname, mname, lname]))
        else:
            self.name = "Novo Discente"

    @api.onchange('name')
    def _onchange_full_name(self):
        if self.name and self.name != "Novo Discente":
            fn, mn, ln = _parse_brazilian_name(self.name)
            if fn:
                self.first_name = fn
            self.middle_name = mn
            if ln:
                self.last_name = ln

    @api.constrains('advisor_id', 'coadvisor_id')
    def _check_advisor_coadvisor(self):
        for record in self:
            if record.advisor_id and record.coadvisor_id and record.advisor_id == record.coadvisor_id:
                raise ValidationError("O orientador principal e o coorientador não podem ser a mesma pessoa.")

    @api.constrains('partner_id', 'company_id')
    def _check_unique_student_partner_company(self):
        for record in self:
            if record.partner_id and record.company_id:
                duplicate = self.search([
                    ('partner_id', '=', record.partner_id.id),
                    ('company_id', '=', record.company_id.id),
                    ('id', '!=', record.id)
                ], limit=1)
                if duplicate:
                    cpf_str = record.partner_id.cpf or record.partner_id.name
                    raise ValidationError(
                        f"A pessoa física '{record.partner_id.name}' (CPF/Ref: {cpf_str}) já possui um Registro "
                        f"Acadêmico institucional (RA: {duplicate.gr_no}) na IES {record.company_id.name}.\n"
                        "A identidade do discente na IES é soberana e perpétua. Novos percursos formativos "
                        "(como Aluno Regular ou Aluno Especial) devem ser vinculados ao histórico de cursos (Opção B)."
                    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            # Sincronização inteligente de nome
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

            # Se nomes particionados estão presentes, consolida name
            fn = vals.get('first_name') or ""
            mn = vals.get('middle_name') or ""
            ln = vals.get('last_name') or ""
            if fn or mn or ln:
                vals['name'] = " ".join(filter(None, [fn, mn, ln]))

            if not vals.get('gr_no'):
                # Gera o RA sequencial institucional caso não informado
                seq = self.env['ir.sequence'].next_by_code('op.student.ra')
                if not seq:
                    # Fallback com base em contagem caso a sequência não esteja instalada
                    year = fields.Date.context_today(self).year
                    count = self.search_count([]) + 1
                    seq = f"RA{year}{count:04d}"
                vals['gr_no'] = seq
        return super(OpStudent, self).create(vals_list)

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
        return super(OpStudent, self).write(vals)
