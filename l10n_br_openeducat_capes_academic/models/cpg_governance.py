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


class OpCpgCommittee(models.Model):
    _name = 'op.cpg.committee'
    _description = 'Comissão de Pós-Graduação (CPG) - Gestão e Mandato'
    _order = 'start_date desc, name'

    name = fields.Char(
        string='Identificação da Gestão',
        required=True,
        help='Ex: Gestão CPG 2024-2027, Conselho CPG IPEN 2026'
    )
    program_id = fields.Many2one(
        'op.program.capes',
        string='Programa de Pós-Graduação',
        required=True
    )
    start_date = fields.Date(
        string='Início do Mandato',
        required=True,
        default=fields.Date.context_today
    )
    end_date = fields.Date(
        string='Término do Mandato',
        help='Data de encerramento do mandato (ex: 3 anos de gestão)'
    )
    status = fields.Selection([
        ('active', 'Ativa'),
        ('closed', 'Encerrada')
    ], string='Situação da Gestão', default='active', required=True)

    member_ids = fields.One2many(
        'op.cpg.member',
        'committee_id',
        string='Membros do Conselho CPG'
    )

    @api.constrains('start_date', 'end_date')
    def _check_mandate_dates(self):
        for record in self:
            if record.start_date and record.end_date and record.end_date < record.start_date:
                raise ValidationError("A data de término do mandato da CPG deve ser posterior à data de início.")


class OpCpgMember(models.Model):
    _name = 'op.cpg.member'
    _description = 'Membro de Comissão de Pós-Graduação (CPG)'

    committee_id = fields.Many2one(
        'op.cpg.committee',
        string='Gestão CPG',
        required=True,
        ondelete='cascade'
    )
    partner_id = fields.Many2one(
        'res.partner',
        string='Membro da CPG',
        required=True
    )
    role = fields.Selection([
        ('coordinator', 'Coordenador(a) / Presidente'),
        ('vice_coordinator', 'Vice-Coordenador(a)'),
        ('titular', 'Membro Titular'),
        ('suplente', 'Membro Suplente'),
        ('student_rep', 'Representante Discente')
    ], string='Cargo no Conselho', default='titular', required=True)

    mandate_origin = fields.Selection([
        ('peer_election', 'Eleito pelos Pares Docentes'),
        ('rector_appointment', 'Indicado pela Reitoria / Conselho'),
        ('student_election', 'Eleição de Representação Discente')
    ], string='Origem do Mandato', default='peer_election')

    document_ref = fields.Char(
        string='Portaria / Ata de Indicação',
        help='Número da Portaria ou documento formal de designação'
    )


class OpCpgMeeting(models.Model):
    _name = 'op.cpg.meeting'
    _description = 'Reunião e Deliberação da Comissão de Pós-Graduação (CPG)'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'meeting_date desc, id desc'

    name = fields.Char(
        string='Número / Identificador da Reunião',
        required=True,
        help='Ex: 3ª Reunião Ordinária CPG/2026'
    )
    committee_id = fields.Many2one(
        'op.cpg.committee',
        string='Composição CPG Responsável',
        required=True,
        tracking=True
    )
    meeting_date = fields.Datetime(
        string='Data e Hora da Reunião',
        required=True,
        default=fields.Datetime.now,
        tracking=True
    )
    meeting_type = fields.Selection([
        ('ordinary', 'Ordinária'),
        ('extraordinary', 'Extraordinária')
    ], string='Tipo de Reunião', default='ordinary', required=True)

    state = fields.Selection([
        ('draft', 'Rascunho / Pauta'),
        ('agenda_open', 'Pauta Aberta / Em Preparação'),
        ('in_approval', 'Em Aprovação'),
        ('published', 'Publicada / Homologada'),
        ('cancelled', 'Cancelada')
    ], string='Situação', default='draft', tracking=True)

    agenda_request_ids = fields.One2many(
        'op.academic.request',
        'cpg_meeting_id',
        string='Requerimentos Pautados'
    )
    minutes_pdf = fields.Binary(
        string='Ata Final da Reunião (QWeb PDF)',
        readonly=True,
        attachment=True,
        help='Documento formal de Ata gerado pelo sistema'
    )
    approval_log_ids = fields.One2many(
        'op.cpg.approval.log',
        'meeting_id',
        string='Registro de Cliques Auditáveis de Aprovação'
    )

    def action_publish_minutes(self):
        """Dispara a homologação da reunião e registro de ata."""
        for record in self:
            if record.state == 'cancelled':
                raise ValidationError("Reuniões canceladas não podem ser homologadas.")
            record.state = 'published'


class OpCpgApprovalLog(models.Model):
    _name = 'op.cpg.approval.log'
    _description = 'Registro Auditável de Aprovação Eletrônica da CPG'
    _order = 'timestamp desc'

    meeting_id = fields.Many2one(
        'op.cpg.meeting',
        string='Reunião CPG',
        required=True,
        ondelete='cascade'
    )
    user_id = fields.Many2one(
        'res.users',
        string='Usuário Votante / Homologador',
        required=True,
        default=lambda self: self.env.user
    )
    timestamp = fields.Datetime(
        string='Carimbo de Tempo Digital',
        required=True,
        default=fields.Datetime.now
    )
    ip_address = fields.Char(
        string='Endereço IP',
        help='IP do terminal no momento da votação/aprovação'
    )
    vote = fields.Selection([
        ('approve', 'Aprovar / Deferir'),
        ('reject', 'Rejeitar / Indeferir'),
        ('abstain', 'Abstenção')
    ], string='Voto / Deliberação', default='approve', required=True)

    notes = fields.Text(
        string='Observações / Ressalvas'
    )
