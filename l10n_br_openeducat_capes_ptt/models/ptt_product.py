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


class CapesPttProduct(models.Model):
    _name = 'capes.ptt.product'
    _description = 'Produto Técnico-Tecnológico (PTT)'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    title = fields.Char(
        string='Título do Produto',
        required=True,
        tracking=True,
        help='Denominação oficial do desenvolvimento técnico-tecnológico'
    )
    type_id = fields.Many2one(
        'capes.ptt.type',
        string='Tipologia do Produto (GTPT)',
        required=True,
        tracking=True
    )
    axis_id = fields.Many2one(
        'capes.ptt.axis',
        string='Eixo Estruturante',
        related='type_id.axis_id',
        store=True,
        readonly=True
    )
    student_id = fields.Many2one(
        'op.student',
        string='Discente Autor (Principal)',
        required=True,
        tracking=True
    )
    thesis_id = fields.Many2one(
        'capes.thesis',
        string='Tese / Dissertação Associada',
        help='Trabalho de conclusão do qual este PTT é derivado'
    )

    # Maturidade Tecnológica (Escala TRL 1 a 9)
    trl_level = fields.Selection([
        ('trl_1', 'TRL 1 - Princípios Básicos Observados'),
        ('trl_2', 'TRL 2 - Conceito ou Aplicação Formulada'),
        ('trl_3', 'TRL 3 - Prova de Conceito Analítica / Experimental'),
        ('trl_4', 'TRL 4 - Validação de Componentes em Laboratório'),
        ('trl_5', 'TRL 5 - Validação em Ambiente Relevante'),
        ('trl_6', 'TRL 6 - Modelo Demonstrado em Ambiente Relevante'),
        ('trl_7', 'TRL 7 - Demonstração de Protótipo Operacional'),
        ('trl_8', 'TRL 8 - Sistema Completo e Qualificado'),
        ('trl_9', 'TRL 9 - Sistema Provado em Ambiente Operacional Real')
    ], string='Nível de Maturidade Tecnológica (TRL)', default='trl_5', required=True, tracking=True)

    adherence_justif = fields.Text(
        string='Justificativa de Aderência à Linha de Pesquisa',
        required=True,
        help='Texto discursivo fundamentando a ligação do produto com a Linha de Pesquisa do PPG'
    )
    is_adherent = fields.Boolean(
        string='Validação de Aderência Confirmada',
        default=True,
        tracking=True,
        help='Se False, o produto sofre glosa técnica e não pode receber estratificação positiva'
    )
    target_audience = fields.Text(
        string='Público-Alvo / Beneficiários',
        help='Setor produtivo, órgãos governamentais ou sociedade civil beneficiada'
    )
    financing_agency = fields.Char(
        string='Agência de Financiamento / Fomento',
        help='Órgão parceiro ou financiador da inovação'
    )
    repository_url = fields.Char(
        string='URL do Produto no Repositório (DSpace)',
        help='Link permanente no repositório institucional (DSpace / Fonte Ouro)'
    )

    state = fields.Selection([
        ('draft', 'Rascunho'),
        ('adherence_check', 'Auditoria de Aderência'),
        ('evaluating', 'Em Avaliação Qualis'),
        ('homologated', 'Homologado / Validado'),
        ('rejected', 'Rejeitado / TNC')
    ], string='Situação', default='draft', tracking=True)

    author_ids = fields.One2many(
        'capes.ptt.author',
        'product_id',
        string='Coautores e Equipe de Criação'
    )
    evaluation_ids = fields.One2many(
        'capes.ptt.evaluation',
        'product_id',
        string='Avaliações do Qualis Tecnológico'
    )

    final_stratum = fields.Selection([
        ('T1', 'T1 - Excelente (90-100 pts)'),
        ('T2', 'T2 - Muito Bom (75-89 pts)'),
        ('T3', 'T3 - Bom (60-74 pts)'),
        ('T4', 'T4 - Regular (45-59 pts)'),
        ('T5', 'T5 - Fraco (30-44 pts)'),
        ('TNC', 'TNC - Produto Não Classificado (<30 pts ou Não Aderente)')
    ], string='Estrato Final Qualis Tecnológico', compute='_compute_stratum', store=True, tracking=True)

    @api.depends('evaluation_ids.final_stratum', 'evaluation_ids.total_score', 'is_adherent')
    def _compute_stratum(self):
        for record in self:
            if not record.is_adherent:
                record.final_stratum = 'TNC'
            elif record.evaluation_ids:
                # Obtém a maior nota de avaliação homologada
                highest_eval = max(record.evaluation_ids, key=lambda e: e.total_score)
                record.final_stratum = highest_eval.final_stratum
            else:
                record.final_stratum = 'TNC'

    @api.constrains('adherence_justif')
    def _check_justif(self):
        for record in self:
            if not record.adherence_justif or not record.adherence_justif.strip():
                raise ValidationError("A justificativa de aderência à linha de pesquisa é obrigatória para cadastrar o PTT.")

    def action_submit_for_evaluation(self):
        for record in self:
            record.state = 'evaluating'

    def action_homologate_ptt(self):
        for record in self:
            if not record.is_adherent:
                raise ValidationError("Produtos não aderentes à linha de pesquisa não podem ser homologados.")
            record.state = 'homologated'
