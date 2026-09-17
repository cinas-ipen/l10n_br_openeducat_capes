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
    _description = 'Expedição e Registro de Diplomas (Nato-Digital MEC 70/2025 e Físico/Papel)'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'graduation_date desc, id desc'

    name = fields.Char(
        string='Identificador do Diploma',
        compute='_compute_name',
        store=True
    )
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

    @api.depends('diploma_process_number', 'student_id.name')
    def _compute_name(self):
        for record in self:
            proc = record.diploma_process_number or f"DIP-{record.id or 'NOVO'}"
            sname = record.student_id.name or 'Discente'
            record.name = f"{proc} - {sname}"


    degree_type = fields.Selection([
        ('master', 'Mestre em Ciências / Mestre Profissional'),
        ('doctorate', 'Doutor em Ciências')
    ], string='Grau Acadêmico Concedido', required=True, default='master', tracking=True)

    # Modalidade e Governança do Registro
    issuing_ies_type = fields.Selection([
        ('autonomous_university', 'Universidade com Autonomia Registradora Direta'),
        ('external_registering_university', 'Registro via IES Registradora Externa (ex: USP para IPEN)')
    ], string='Governança do Registro', default='external_registering_university', required=True, tracking=True)

    emission_format = fields.Selection([
        ('digital', 'Nato-Digital (Portaria MEC nº 70/2025)'),
        ('paper_hybrid', 'Físico em Papel Registrado (Tradição/Transição MEC)'),
        ('both', 'Ambos (Digital + Físico)')
    ], string='Formato de Emissão', default='paper_hybrid', required=True, tracking=True)

    origin_ies_name = fields.Char(
        string='IES / Instituto de Origem',
        default='Instituto de Pesquisas Energéticas e Nucleares - IPEN-CNEN/SP',
        required=True
    )
    issuing_ies_name = fields.Char(
        string='IES Emissora / Registradora do Grau',
        default='Universidade de São Paulo - USP',
        required=True,
        help='Para institutos de pesquisa como o IPEN, a IES Registradora do diploma é a USP.'
    )

    diploma_process_number = fields.Char(
        string='Número do Processo de Registro de Diploma',
        tracking=True,
        help='Número de protocolo do processo de registro (ex: Processo USP / IPEN)'
    )
    graduation_date = fields.Date(
        string='Data da Outorga do Grau',
        required=True,
        default=fields.Date.context_today,
        tracking=True
    )

    # Campos de Registro Físico / Livro de Registro
    registration_book_number = fields.Char(
        string='Número do Livro de Registro',
        tracking=True,
        help='Livro de Registro de Diplomas da IES Registradora (ex: Livro 42-B na USP)'
    )
    registration_page_number = fields.Char(
        string='Folha / Página do Registro',
        tracking=True,
        help='Número da Folha/Página do Livro de Registro (ex: Fls. 118)'
    )
    registration_date = fields.Date(
        string='Data do Registro na IES Registradora',
        tracking=True,
        help='Data em que a IES Registradora (ex: USP) efetivou o registro do diploma'
    )
    physical_dispatch_date = fields.Date(
        string='Data de Remessa do Protocolo Físico',
        tracking=True,
        help='Data de remessa do processo/diploma em papel para a IES Registradora'
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
        ('signed', 'Assinado Digitalmente / Registrado'),
        ('issued', 'Diploma Expedido & Registrado')
    ], string='Situação', default='draft', tracking=True)

    signature_log_ids = fields.One2many(
        'capes.diploma.signature.log',
        'diploma_id',
        string='Trilha de Auditoria de Assinaturas Criptográficas'
    )

    @api.onchange('issuing_ies_type')
    def _onchange_issuing_ies_type(self):
        for record in self:
            if record.issuing_ies_type == 'external_registering_university':
                record.issuing_ies_name = 'Universidade de São Paulo - USP'
            elif record.issuing_ies_type == 'autonomous_university':
                record.issuing_ies_name = record.origin_ies_name or 'Universidade Autônoma'

    def action_generate_degree_package(self):
        """Gera o Hash SHA-256 e os XMLs estruturados do Dossiê Acadêmico."""
        Ledger = self.env['op.student.credit.ledger']
        for record in self:
            if not record.student_id or not record.thesis_id:
                raise ValidationError("Discente e Defesa/Tese são obrigatórios para gerar o Pacote de Titulação.")

            # 1. Cálculo da Chave Hash SHA-256
            raw_hash_str = f"{record.student_id.id}|{record.student_id.partner_id.cpf}|{record.thesis_id.title}|{record.graduation_date}|{record.origin_ies_name}|{record.issuing_ies_name}|{record.emission_format}"
            hash_object = hashlib.sha256(raw_hash_str.encode('utf-8'))
            record.sha256_hash = hash_object.hexdigest().upper()
            record.validation_qr_code_url = f"/valida-documento?hash={record.sha256_hash}"

            # 2. Geração do XML do Diploma (Portaria MEC 70/2025)
            company = self.env.company
            diploma_xml_str = f"""<?xml version="1.0" encoding="UTF-8"?>
<DiplomaDigital xmlns="http://www.mec.gov.br/diplomadigital">
    <InfDiplomaDigital id="DIP-{record.id}">
        <DadosDiploma>
            <FormatoEmissao>{record.emission_format}</FormatoEmissao>
            <GovernancaRegistro>{record.issuing_ies_type}</GovernancaRegistro>
            <NomeTitulado>{record.student_id.partner_id.name}</NomeTitulado>
            <CPFTitulado>{record.student_id.partner_id.cpf or ''}</CPFTitulado>
            <GrauConcedido>{record.degree_type}</GrauConcedido>
            <DataOutorga>{record.graduation_date}</DataOutorga>
            <IesOrigem>{record.origin_ies_name}</IesOrigem>
            <IesEmissora>{record.issuing_ies_name}</IesEmissora>
            <CodigoEMEC>{company.emec_code or ''}</CodigoEMEC>
            <CodigoCapesPPG>{record.student_id.program_id.snpg_code if record.student_id.program_id else ''}</CodigoCapesPPG>
        </DadosDiploma>
        <DadosRegistroFisico>
            <NumeroLivro>{record.registration_book_number or ''}</NumeroLivro>
            <NumeroFolha>{record.registration_page_number or ''}</NumeroFolha>
            <DataRegistro>{record.registration_date or ''}</DataRegistro>
        </DadosRegistroFisico>
        <DadosTese>
            <TituloTese>{record.thesis_id.title}</TituloTese>
            <HandleDSpace>{record.thesis_id.repository_url or ''}</HandleDSpace>
        </DadosTese>
        <ChaveAutenticacao>{record.sha256_hash}</ChaveAutenticacao>
    </InfDiplomaDigital>
</DiplomaDigital>"""
            record.diploma_xml = diploma_xml_str

            # 3. Geração do XML do Dossiê Acadêmico (Livro-Razão e Banca)
            # Exclui disciplinas em quarentena de aluno especial que não foram formalmente incorporadas
            ledger_records = Ledger.search([
                ('student_id', '=', record.student_id.id),
                ('credit_type', '!=', 'subject_special_quarantine'),
                ('is_approved', '=', True)
            ])
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
        """Orquestra a assinatura criptográfica avançada XAdES ICP-Brasil ou a chancela do protocolo físico."""
        for record in self:
            if record.state not in ('package_ready', 'signed'):
                raise ValidationError("Gere primeiro o Pacote de Titulação antes de assinar digitalmente / registrar.")

            # Simulação Criptográfica de Envelope XAdES-BES (MEC 70/2025)
            timestamp_str = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
            sig_hash = hashlib.sha256(f"{record.diploma_xml}|{timestamp_str}".encode('utf-8')).hexdigest().upper()

            subject_name = "CN=SECRETARIA ACADEMICA ICP-BRASIL, O=INSTITUTO DE PESQUISAS ENERGETICAS E NUCLEARES"
            signer_label = "Secretaria Acadêmica / CPG-IPEN"
            if record.issuing_ies_type == 'external_registering_university':
                subject_name += f", OU={record.issuing_ies_name}"
                signer_label += f" & Pró-Reitoria de Pós-Graduação ({record.issuing_ies_name})"

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
            <ds:X509SubjectName>{subject_name}</ds:X509SubjectName>
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
                'signer_name': signer_label,
                'certificate_serial': 'ICP-BR-A3-2026-IPEN-USP-0091823',
                'signature_timestamp': fields.Datetime.now(),
                'signature_hash': sig_hash,
                'signature_algorithm': 'XAdES-BES SHA-256 com Carimbo de Tempo (ICP-Brasil)'
            })

            record.state = 'signed'

    def action_issue_diploma(self):
        """Conclui a expedição formal e o registro do Diploma."""
        for record in self:
            if not record.signed_xades_xml:
                raise ValidationError("O diploma precisa estar assinado / chancelado no pacote antes de ser expedido.")
            record.state = 'issued'
