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


class CapesThesisCommittee(models.Model):
    _name = 'capes.thesis.committee'
    _description = 'Membro da Comissão Examinadora e Banca Julgadora'
    _order = 'is_titular desc, member_role, id'

    thesis_id = fields.Many2one(
        'capes.thesis',
        string='Rito / Trabalho de Conclusão',
        required=True,
        ondelete='cascade'
    )
    member_id = fields.Many2one(
        'res.partner',
        string='Examinador (Pessoa)',
        required=True
    )
    member_role = fields.Selection([
        ('advisor', 'Orientador / Presidente'),
        ('coadvisor', 'Coorientador'),
        ('internal_evaluator', 'Avaliador Interno'),
        ('external_evaluator', 'Avaliador Externo'),
        ('substitute_internal', 'Suplente Interno'),
        ('substitute_external', 'Suplente Externo')
    ], string='Papel na Comissão Julgadora', default='internal_evaluator', required=True)

    is_titular = fields.Boolean(
        string='Membro Titular',
        default=True,
        help='True para membros efetivos da pauta votante; False para suplentes'
    )
    can_vote = fields.Boolean(
        string='Direito a Voto Ativo',
        compute='_compute_can_vote',
        store=True,
        help='Calculado dinamicamente com base nas regras do regimento do aluno'
    )
    is_internal = fields.Boolean(
        string='Pertence ao Quadro da IES',
        related='member_id.is_internal',
        store=True,
        readonly=True
    )
    ies_origin = fields.Char(
        string='IES de Origem do Examinador',
        help='Instituição de origem para membros externos'
    )
    has_phd = fields.Boolean(
        string='Possui Título de Doutor',
        default=True,
        help='Indica se o examinador possui a titulação máxima de Doutorado'
    )
    civil_relationship_flag = fields.Boolean(
        string='Impedimento por Parentesco / Conflito Ético',
        default=False,
        help='Trava de impedimento por parentesco em linha reta ou colateral até 4º grau'
    )
    non_phd_approval_doc = fields.Char(
        string='Ata / Aprovação CPG para Não-Doutor',
        help='Número da ata CPG que autorizou o especialista de mercado sem doutorado'
    )

    @api.depends('is_titular', 'member_role', 'thesis_id.curriculum_version_id')
    def _compute_can_vote(self):
        CommitteeRule = self.env['op.curriculum.committee.rule']
        for record in self:
            if not record.is_titular or record.member_role in ('substitute_internal', 'substitute_external'):
                record.can_vote = False
                continue

            curriculum = record.thesis_id.curriculum_version_id
            if not curriculum:
                record.can_vote = True
                continue

            # Pesquisa regra do regimento correspondente ao rito
            rule = CommitteeRule.search([
                ('curriculum_version_id', '=', curriculum.id),
                ('stage', '=', record.thesis_id.stage)
            ], limit=1)

            if record.member_role == 'advisor':
                if rule and rule.advisor_vote_role == 'non_voting_president':
                    record.can_vote = False
                else:
                    record.can_vote = True
            elif record.member_role == 'coadvisor':
                if rule and rule.coadvisor_participation in ('non_voting_additional', 'forbidden_with_advisor'):
                    record.can_vote = False
                else:
                    record.can_vote = True
            else:
                record.can_vote = True

    @api.constrains('civil_relationship_flag', 'has_phd', 'non_phd_approval_doc')
    def _check_committee_integrity(self):
        for record in self:
            # Trava de Impedimento Cível (parentesco até 4º grau)
            if record.civil_relationship_flag:
                raise ValidationError(f"O examinador {record.member_id.name} possui flag de impedimento cível/ético (parentesco até 4º grau ou conflito de interesse) e não pode integrar a comissão examinadora.")

            # Trava de Notório Saber para Não-Doutor
            if not record.has_phd:
                curriculum = record.thesis_id.curriculum_version_id
                rule = self.env['op.curriculum.committee.rule'].search([
                    ('curriculum_version_id', '=', curriculum.id),
                    ('stage', '=', record.thesis_id.stage)
                ], limit=1) if curriculum else False

                if rule and not rule.allow_non_phd_member:
                    raise ValidationError(f"O regimento do curso não permite examinadores sem o título de Doutor para o rito de {record.thesis_id.stage}.")
                elif not record.non_phd_approval_doc:
                    raise ValidationError(f"É necessário informar a Ata ou ato de homologação da CPG autorizando a participação do especialista não-doutor {record.member_id.name}.")
