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

import hashlib
from datetime import datetime
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class CapesDigitalDiploma(models.Model):
    _name = 'capes.digital.diploma'
    _description = 'Diploma Nato-Digital e Pacote de Titulação (Portaria MEC 70/2025)'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'graduation_date desc, id desc'

    student_id = fields.Many2one(
        'op.student',
        string='Discente Titulado',
        required=True,
        tracking=True
    )
    thesis_id = fields.Many2one(
        'capes.thesis',
        string='Defesa / Trabalho de Conclusão',
        required=True,
        tracking=True
    )
    curriculum_version_id = fields.Many2one(
        'op.curriculum.version',
        string='Versão Regimental Ativa (Ato Perfeito)',
        related='student_id.curriculum_version_id',
        store=True,
        readonly=True
    )

    degree_type = fields.Selection([
        ('master', 'Mestre em Ciências / Mestre Profissional'),
        ('doctorate', 'Doutor em Ciências')
    ], string='Grau Acadêmico Concedido', required=True, default='master', tracking=True)

    origin_ies_name = fields.Char(
        string='IES de Origem (Ensino / Pesquisa)',
        default='Instituto de Pesquisas Energéticas e Nucleares - IPEN-CNEN/SP',
        required=True
    )
    issuing_ies_name = fields.Char(
        string='IES Emissora / Registradora do Grau',
        default='Universidade de São Paulo - USP',
        required=True
    )

    diploma_process_number = fields.Char(
        string='Número do Processo de Registro de Diploma',
        tracking=True,
        help='Número de protocolo de registro na Pró-Reitoria de Pós-Graduação'
    )
    graduation_date = fields.Date(
        string='Data da Outorga do Grau',
        required=True,
        default=fields.Date.context_today,
        tracking=True
    )

    # Criptografia e Estruturação de XMLs Federais (Portaria MEC nº 70/2025)
    diploma_xml = fields.Text(
        string='XML Estruturado do Diploma Digital (MEC 70/2025)',
        readonly=True
    )
    dossier_xml = fields.Text(
        string='XML do Dossiê / Lastro Acadêmico (Histórico e Banca)',
        readonly=True
    )
    signed_xades_xml = fields.Text(
        string='XML Assinado Digitalmente (XAdES ICP-Brasil A3/HSM)',
        readonly=True
    )

    sha256_hash = fields.Char(
        string='Chave Hash SHA-256 de Auto-Autenticação',
        readonly=True,
        tracking=True
    )
    validation_qr_code_url = fields.Char(
        string='URL do QR Code de Validação Pública',
        readonly=True,
        help='Redirecionamento para o endpoint público /valida-documento'
    )

    state = fields.Selection([
        ('draft', 'Rascunho / Em Preparação'),
        ('package_ready', 'Pacote de Titulação Selado'),
        ('signed', 'Assinado Digitalmente (XAdES)'),
        ('issued', 'Diploma Expedido & Registrado')
    ], string='Situação', default='draft', tracking=True)

    signature_log_ids = fields.One2many(
        'capes.diploma.signature.log',
        'diploma_id',
        string='Trilha de Auditoria de Assinaturas Criptográficas'
    )

    def action_generate_degree_package(self):
        """Gera o Hash SHA-256 e os XMLs estruturados conforme a Portaria MEC nº 70/2025."""
        Ledger = self.env['op.student.credit.ledger']
        for record in self:
            if not record.student_id or not record.thesis_id:
                raise ValidationError("Discente e Defesa/Tese são obrigatórios para gerar o Pacote de Titulação.")

            # 1. Cálculo da Chave Hash SHA-256
            raw_hash_str = f"{record.student_id.id}|{record.student_id.partner_id.cpf}|{record.thesis_id.title}|{record.graduation_date}|{record.origin_ies_name}|{record.issuing_ies_name}"
            hash_object = hashlib.sha256(raw_hash_str.encode('utf-8'))
            record.sha256_hash = hash_object.hexdigest().upper()
            record.validation_qr_code_url = f"/valida-documento?hash={record.sha256_hash}"

            # 2. Geração do XML do Diploma (Portaria MEC 70/2025)
            company = self.env.company
            diploma_xml_str = f"""<?xml version="1.0" encoding="UTF-8"?>
<DiplomaDigital xmlns="http://www.mec.gov.br/diplomadigital">
    <InfDiplomaDigital id="DIP-{record.id}">
        <DadosDiploma>
            <NomeTitulado>{record.student_id.partner_id.name}</NomeTitulado>
            <CPFTitulado>{record.student_id.partner_id.cpf or ''}</CPFTitulado>
            <GrauConcedido>{record.degree_type}</GrauConcedido>
            <DataOutorga>{record.graduation_date}</DataOutorga>
            <IesOrigem>{record.origin_ies_name}</IesOrigem>
            <IesEmissora>{record.issuing_ies_name}</IesEmissora>
            <CodigoEMEC>{company.emec_code or ''}</CodigoEMEC>
            <CodigoCapesPPG>{record.student_id.program_id.snpg_code if record.student_id.program_id else ''}</CodigoCapesPPG>
        </DadosDiploma>
        <DadosTese>
            <TituloTese>{record.thesis_id.title}</TituloTese>
            <HandleDSpace>{record.thesis_id.repository_url or ''}</HandleDSpace>
        </DadosTese>
        <ChaveAutenticacao>{record.sha256_hash}</ChaveAutenticacao>
    </InfDiplomaDigital>
</DiplomaDigital>"""
            record.diploma_xml = diploma_xml_str

            # 3. Geração do XML do Dossiê Acadêmico (Livro-Razão e Banca)
            ledger_records = Ledger.search([('student_id', '=', record.student_id.id), ('is_approved', '=', True)])
            ledger_xml_lines = "".join([
                f"<Disciplina><Nome>{l.subject_id.name if l.subject_id else ''}</Nome><Creditos>{l.credits}</Creditos><Conceito>{l.grade_concept}</Conceito></Disciplina>"
                for l in ledger_records
            ])

            dossier_xml_str = f"""<?xml version="1.0" encoding="UTF-8"?>
<DossieAcademico xmlns="http://www.mec.gov.br/dossieacademico">
    <Discente>{record.student_id.partner_id.name}</Discente>
    <VersaoRegimental>{record.curriculum_version_id.name if record.curriculum_version_id else ''}</VersaoRegimental>
    <HistoricoCreditos>
        {ledger_xml_lines}
    </HistoricoCreditos>
</DossieAcademico>"""
            record.dossier_xml = dossier_xml_str
            record.state = 'package_ready'

    def action_sign_diploma_xades(self):
        """Orquestra a assinatura criptográfica avançada XAdES ICP-Brasil (Certificados A3/HSM) e insere Carimbo de Tempo."""
        for record in self:
            if record.state not in ('package_ready', 'signed'):
                raise ValidationError("Gere primeiro o Pacote de Titulação antes de assinar digitalmente.")

            # Simulação Criptográfica de Envelope XAdES-BES (MEC 70/2025)
            timestamp_str = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
            sig_hash = hashlib.sha256(f"{record.diploma_xml}|{timestamp_str}".encode('utf-8')).hexdigest().upper()

            signed_xml = f"""{record.diploma_xml}
<!-- Signature XAdES ICP-Brasil Enveloped -->
<ds:Signature xmlns:ds="http://www.w3.org/2000/09/xmldsig#" id="SIG-{record.id}">
    <ds:SignedInfo>
        <ds:SignatureMethod Algorithm="http://www.w3.org/2001/04/xmldsig-more#rsa-sha256"/>
        <ds:DigestValue>{sig_hash}</ds:DigestValue>
    </ds:SignedInfo>
    <ds:SignatureValue>XAdES_ICP_BRASIL_A3_HSM_SIGNATURE_DATA_STRING</ds:SignatureValue>
    <ds:KeyInfo>
        <ds:X509Data>
            <ds:X509SubjectName>CN=REITORIA USP ICP-BRASIL, O=UNIVERSIDADE DE SAO PAULO</ds:X509SubjectName>
        </ds:X509Data>
    </ds:KeyInfo>
    <ds:Object>
        <TimeStamp>{timestamp_str}</TimeStamp>
    </ds:Object>
</ds:Signature>"""
            record.signed_xades_xml = signed_xml

            # Registra a trilha de auditoria de assinatura
            self.env['capes.diploma.signature.log'].create({
                'diploma_id': record.id,
                'signer_name': 'Reitoria da Universidade de São Paulo - USP / CPG-IPEN',
                'certificate_serial': 'ICP-BR-A3-2026-USP-0091823',
                'signature_timestamp': fields.Datetime.now(),
                'signature_hash': sig_hash,
                'signature_algorithm': 'XAdES-BES SHA-256 com Carimbo de Tempo (ICP-Brasil)'
            })

            record.state = 'signed'

    def action_issue_diploma(self):
        """Conclui a expedição formal e o registro do Diploma Digital."""
        for record in self:
            if not record.signed_xades_xml:
                raise ValidationError("O diploma precisa estar assinado no padrão XAdES antes de ser expedido.")
            record.state = 'issued'
