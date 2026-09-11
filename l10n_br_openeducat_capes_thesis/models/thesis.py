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


class CapesThesis(models.Model):
    _name = 'capes.thesis'
    _description = 'Trabalho de Conclusão e Ritos Acadêmicos (Qualificação / Defesa)'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'defense_date desc, id desc'

    capes_id = fields.Integer(
        string='Identificador CAPES',
        help='ID numérico do registro na CAPES / Sucupira'
    )
    student_id = fields.Many2one(
        'op.student',
        string='Discente Solicitante',
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
    work_plan_id = fields.Many2one(
        'op.student.work_plan',
        string='Plano de Trabalho Homologado',
        required=True,
        tracking=True,
        help='Plano de trabalho discente homologado pela CPG'
    )
    project_id = fields.Many2one(
        'capes.research.project',
        string='Projeto de Pesquisa Vinculado'
    )
    stage = fields.Selection([
        ('seminar_area', 'Seminário de Área'),
        ('qualification', 'Exame de Qualificação Clássico'),
        ('defense', 'Defesa Pública Final')
    ], string='Rito Acadêmico Registrado', required=True, default='defense', tracking=True)

    doc_type = fields.Selection([
        ('dissertation', 'Dissertação de Mestrado'),
        ('thesis', 'Tese de Doutorado'),
        ('tech_product', 'Produto Tecnológico / Relatório Técnico')
    ], string='Tipo de Documento Final', required=True, default='dissertation', tracking=True)

    defense_date = fields.Datetime(
        string='Data e Horário da Sessão',
        required=True,
        tracking=True
    )
    title = fields.Char(
        string='Título Final Aprovado em Ata',
        required=True,
        tracking=True
    )
    title_alt = fields.Char(
        string='Título Traduzido (Inglês)',
        tracking=True
    )
    abstract_main = fields.Text(
        string='Resumo no Idioma Principal'
    )
    abstract_alt = fields.Text(
        string='Resumo em Inglês (Abstract)'
    )
    keywords_main = fields.Char(
        string='Palavras-chave no Idioma Principal',
        help='Vocabulário controlado separado por ponto e vírgula'
    )
    keywords_alt = fields.Char(
        string='Palavras-chave em Inglês'
    )

    presentation_time_minutes = fields.Integer(
        string='Tempo de Exposição do Candidato (min)',
        default=50,
        help='Teto regimental de exposição (ex: 50 min no IPEN)'
    )
    arguing_time_minutes = fields.Integer(
        string='Tempo de Arguição por Examinador (min)',
        default=40,
        help='Teto regimental de arguição por examinador (ex: 40 min)'
    )

    # Versão Final do PDF enviada pelo Aluno e Validação da Secretaria
    final_pdf_file = fields.Binary(
        string='Versão Final da Dissertação/Tese (PDF)',
        attachment=True,
        help='Upload do PDF final corrigido pelo discente (com capa, folha de aprovação e ficha catalográfica)'
    )
    final_pdf_filename = fields.Char(
        string='Nome do Arquivo PDF Final'
    )
    final_pdf_upload_date = fields.Date(
        string='Data de Envio da Versão Final pelo Aluno'
    )

    secretariat_approval = fields.Boolean(
        string='De Acordo / Validação da Secretaria Acadêmica',
        default=False,
        tracking=True,
        help='Aceite formal da secretaria após conferência de formatação e ficha catalográfica'
    )
    secretariat_approval_date = fields.Date(
        string='Data de Validação da Secretaria'
    )

    # Manifesto de Metadados para a Biblioteca Central (Depósito no DSpace)
    library_manifest_payload = fields.Text(
        string='Guia/Manifesto de Metadados para Biblioteca (DSpace)',
        readonly=True,
        help='Documento/Guia com os metadados acadêmicos gerado para a biblioteca realizar o upload no DSpace'
    )

    # Integração Repositório Institucional (Fonte Ouro / DSpace)
    repository_url = fields.Char(
        string='Handle / URI no Repositório (DSpace)',
        tracking=True,
        help='Handle permanente gerado pela biblioteca após o upload no DSpace (ex: http://repositorio.ipen.br/handle/12345/6789)'
    )
    deposit_date = fields.Date(
        string='Data do Depósito no DSpace pela Biblioteca'
    )

    status = fields.Selection([
        ('draft', 'Rascunho'),
        ('scheduled', 'Agendado'),
        ('approved', 'Aprovado na Banca'),
        ('disapproved', 'Reprovado na Banca'),
        ('deposit_pending', 'Pendente Envio Versão Final (Aluno)'),
        ('final_version_submitted', 'Versão Final Enviada (Triagem Secretaria)'),
        ('homologated', 'Homologado / Titulado (Secretaria OK)')
    ], string='Situação do Rito', default='draft', tracking=True)

    committee_ids = fields.One2many(
        'capes.thesis.committee',
        'thesis_id',
        string='Membros da Comissão Examinadora'
    )

    def action_schedule_rite(self):
        """Executa as travas prévias de elegibilidade antes de agendar o rito acadêmico."""
        Ledger = self.env['op.student.credit.ledger']
        for record in self:
            curriculum = record.curriculum_version_id
            if not curriculum:
                raise ValidationError("O discente deve possuir uma Versão Regimental ativa vinculada.")

            # 1. Trava do Plano de Trabalho Homologado
            if record.work_plan_id.state != 'homologated':
                raise ValidationError("O agendamento do rito exige que o Plano de Trabalho do discente esteja com o status 'Homologado CPG'.")

            # 2. Trava Ética CEP/CEUA
            if record.work_plan_id.opinion_category == 'cep_pending' and not record.work_plan_id.cep_approved:
                raise ValidationError("O Plano de Trabalho possui pendência ética de CEP/CEUA não liberada. Faça o upload do parecer consubstanciado de aprovação.")

            # 3. Trava de Proficiência Linguística (se exigida no rito ou na admissão)
            if curriculum.proficiency_stage == 'qualification' and record.stage == 'qualification':
                if record.student_id.english_proficiency_status != 'approved':
                    raise ValidationError("O regimento do curso exige a comprovação de proficiência em inglês aprovada no Exame de Qualificação.")
            elif curriculum.proficiency_stage == 'defense' and record.stage == 'defense':
                if record.student_id.english_proficiency_status != 'approved':
                    raise ValidationError("O regimento do curso exige a comprovação de proficiência em inglês aprovada para a Defesa Final.")

            # 4. Trava de Créditos Cumpridos em Disciplinas e Atividades (Artigo 39º do Regulamento)
            if record.stage == 'defense':
                ledger_records = Ledger.search([
                    ('student_id', '=', record.student_id.id),
                    ('is_approved', '=', True)
                ])
                subject_credits = sum(ledger_records.filtered(lambda l: l.credit_type in ('subject', 'external', 'apo')).mapped('credits'))
                if subject_credits < curriculum.min_subject_credits:
                    raise ValidationError(
                        f"Integralização de disciplinas insuficiente (Art. 39º). O aluno possui {subject_credits:.1f} créditos em disciplinas, "
                        f"mas o regimento exige o mínimo de {curriculum.min_subject_credits} créditos em disciplinas do programa."
                    )

            record.status = 'scheduled'

    def action_approve_in_board(self):
        """Registra a aprovação na banca e encaminha para envio da versão final pelo aluno."""
        for record in self:
            if record.stage == 'defense':
                record.status = 'deposit_pending'
            else:
                record.status = 'approved'

    def action_disapprove_in_board(self):
        """Registra a reprovação na banca."""
        for record in self:
            record.status = 'disapproved'

    def action_submit_final_version(self):
        """Discente envia o arquivo PDF final corrigido no sistema."""
        for record in self:
            if not record.final_pdf_file:
                raise ValidationError("É necessário anexar o arquivo PDF da Versão Final Corrigida antes de submeter.")
            record.final_pdf_upload_date = fields.Date.context_today(self)
            record.status = 'final_version_submitted'

    def action_secretariat_approve_final_version(self):
        """Secretaria Acadêmica valida o PDF final (formatação/ficha catalográfica), titula o discente e gera o manifesto para a Biblioteca."""
        for record in self:
            if not record.final_pdf_file:
                raise ValidationError("Não há arquivo PDF da versão final anexado para validação.")

            record.secretariat_approval = True
            record.secretariat_approval_date = fields.Date.context_today(self)
            record.status = 'homologated'

            # Altera status do discente para TITULADO
            record.student_id.capes_status = 'graduated'
            record.student_id.status_date = fields.Date.context_today(self)

            # Gera Guia/Manifesto de Metadados para a Biblioteca Central (DSpace)
            record._generate_library_manifest()

    def _generate_library_manifest(self):
        """Gera o manifesto XML com todos os metadados para envio à Biblioteca Central efetuar o depósito no DSpace."""
        for record in self:
            advisor_name = record.student_id.main_advisor_id.partner_id.name if record.student_id.main_advisor_id else ''
            advisor_orcid = record.student_id.main_advisor_id.partner_id.orcid if record.student_id.main_advisor_id else ''
            program_code = record.student_id.program_id.snpg_code if record.student_id.program_id else ''

            manifest = f"""<?xml version="1.0" encoding="UTF-8"?>
<GuiaDepositoDSpace xmlns="http://capes.gov.br/dspace/manifest">
    <Identificadores>
        <ProgramaCodigo>{program_code}</ProgramaCodigo>
        <TeseID>{record.id}</TeseID>
    </Identificadores>
    <Discente>
        <Nome>{record.student_id.partner_id.name}</Nome>
        <CPF>{record.student_id.partner_id.cpf or ''}</CPF>
        <ORCID>{record.student_id.partner_id.orcid or ''}</ORCID>
    </Discente>
    <Orientador>
        <Nome>{advisor_name}</Nome>
        <ORCID>{advisor_orcid}</ORCID>
    </Orientador>
    <Trabalho>
        <TituloMain>{record.title}</TituloMain>
        <TituloAlt>{record.title_alt or ''}</TituloAlt>
        <TipoDocumento>{record.doc_type}</TipoDocumento>
        <DataDefesa>{record.defense_date}</DataDefesa>
        <ResumoMain>{record.abstract_main or ''}</ResumoMain>
        <ResumoAlt>{record.abstract_alt or ''}</ResumoAlt>
        <PalavrasChaveMain>{record.keywords_main or ''}</PalavrasChaveMain>
        <PalavrasChaveAlt>{record.keywords_alt or ''}</PalavrasChaveAlt>
        <ArquivoPDFNome>{record.final_pdf_filename or 'dissertacao_final.pdf'}</ArquivoPDFNome>
    </Trabalho>
</GuiaDepositoDSpace>"""
            record.library_manifest_payload = manifest

    def action_record_dspace_handle(self):
        """Biblioteca informa o Handle/URI permanente gerado após o upload oficial no DSpace."""
        for record in self:
            if not record.repository_url or not record.repository_url.strip():
                raise ValidationError("É obrigatório informar o Handle/URI permanente gerado pelo DSpace.")
            record.deposit_date = fields.Date.context_today(self)
