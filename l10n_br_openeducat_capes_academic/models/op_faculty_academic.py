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


class OpFaculty(models.Model):
    _inherit = 'op.faculty'

    program_link_ids = fields.One2many(
        'op.faculty.program.link',
        'faculty_id',
        string='Credenciamentos CPG nos Programas'
    )
    accreditation_count = fields.Integer(
        string='Credenciamentos CPG',
        compute='_compute_accreditation_count'
    )
    program_ids = fields.Many2many(
        'op.program.capes',
        string='Programas PPG Locais',
        compute='_compute_programs',
        store=True,
        help='Programas de Pós-Graduação da instituição aos quais o docente está credenciado.'
    )
    programs_summary = fields.Char(
        string='Programas PPG (Filiações)',
        compute='_compute_programs',
        store=True,
        help='Resumo de todos os programas PPG (locais e externos) aos quais o docente está filiado.'
    )
    permanent_programs_count = fields.Integer(
        string='Vínculos como Permanente (Teto: 3 CAPES)',
        compute='_compute_programs',
        store=True,
        help='Total de programas stricto sensu onde o docente atua como Permanente (máximo 3 pela Portaria CAPES nº 81/2016).'
    )
    capes_program_compliance = fields.Selection([
        ('compliant', 'Regular (≤ 3 Vínculos)'),
        ('warning', 'Teto Atingido (3 Vínculos)'),
        ('exceeded', 'Irregular (> 3 Vínculos)')
    ], string='Conformidade Portaria CAPES 81/2016', compute='_compute_programs', store=True)

    @api.depends('program_link_ids')
    def _compute_accreditation_count(self):
        for record in self:
            record.accreditation_count = len(record.program_link_ids)

    @api.depends(
        'program_link_ids',
        'program_link_ids.link_type',
        'program_link_ids.program_id',
        'program_link_ids.external_program_name',
        'program_link_ids.external_ies_name',
        'program_link_ids.faculty_category'
    )
    def _compute_programs(self):
        cat_labels = {
            'permanent': 'Permanente',
            'collaborator': 'Colaborador',
            'visiting': 'Visitante',
            'assistant': 'Assistente',
        }
        for faculty in self:
            links = faculty.sudo().program_link_ids
            local_progs = links.filtered(lambda l: l.link_type == 'internal' and l.program_id).mapped('program_id')
            faculty.program_ids = [(6, 0, local_progs.ids)]

            summaries = []
            perm_count = 0
            for link in links:
                cat = cat_labels.get(link.faculty_category, link.faculty_category or 'Permanente')
                if link.faculty_category == 'permanent':
                    perm_count += 1
                if link.link_type == 'internal' and link.program_id:
                    prog_label = link.program_id.short_name or link.program_id.name
                    summaries.append(f"{prog_label} ({cat})")
                elif link.link_type == 'external' and link.external_program_name:
                    ies_prefix = f"{link.external_ies_name}/" if link.external_ies_name else ""
                    summaries.append(f"{ies_prefix}{link.external_program_name} (Ext. {cat})")

            faculty.programs_summary = " | ".join(summaries) if summaries else "Sem vínculo registrado"
            faculty.permanent_programs_count = perm_count
            if perm_count > 3:
                faculty.capes_program_compliance = 'exceeded'
            elif perm_count == 3:
                faculty.capes_program_compliance = 'warning'
            else:
                faculty.capes_program_compliance = 'compliant'

    @api.constrains('program_link_ids')
    def _check_capes_permanent_limit(self):
        for faculty in self:
            links = faculty.sudo().program_link_ids
            perm_links = links.filtered(lambda l: l.faculty_category == 'permanent')
            if len(perm_links) > 3:
                raise ValidationError(
                    f"Bloqueio de Conformidade Regulatória (Portaria CAPES nº 81/2016, Art. 4º, § 2º):\n"
                    f"O docente '{faculty.name}' está associado como Permanente a {len(perm_links)} programas.\n"
                    f"A legislação federal estipula o teto máximo de 3 (três) programas de pós-graduação stricto sensu "
                    f"como Docente Permanente em todo o território nacional."
                )

    def action_view_accreditations(self):
        self.ensure_one()
        return {
            'name': f'Credenciamentos CPG - {self.name}',
            'type': 'ir.actions.act_window',
            'res_model': 'op.faculty.program.link',
            'view_mode': 'list,form',
            'domain': [('faculty_id', '=', self.id)],
            'context': {'default_faculty_id': self.id},
        }
