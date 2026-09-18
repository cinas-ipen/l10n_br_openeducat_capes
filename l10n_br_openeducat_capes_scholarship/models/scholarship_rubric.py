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
###############################################################################

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class CapesScholarshipRubric(models.Model):
    """Barema Parametrizável de Avaliação para Concessão de Bolsas.
    Permite modelar tanto baremas analíticos por pontos e tetos (IPEN Acadêmico)
    quanto matrizes quali-quantitativas em escala 1 a 5 (Mestrado Profissional MP-TRCS).
    """
    _name = 'capes.scholarship.rubric'
    _description = 'Barema de Avaliação de Bolsas'
    _order = 'name'

    name = fields.Char(string='Título do Barema', required=True)
    level = fields.Selection([
        ('master_acad', 'Mestrado Acadêmico'),
        ('master_prof', 'Mestrado Profissional'),
        ('phd', 'Doutorado'),
        ('direct_phd', 'Doutorado Direto'),
    ], string='Nível de Formação', required=True, default='master_acad')
    
    scoring_model = fields.Selection([
        ('analytical_points', 'Pontuação Analítica com Tetos (Padrão IPEN)'),
        ('likert_scale', 'Matriz em Escala de 1 a 5 (Padrão MP-TRCS)'),
    ], string='Modelo de Pontuação', required=True, default='analytical_points')

    total_max_points = fields.Float(
        string='Pontuação Máxima Global',
        help='Teto máximo global da ficha (ex.: 125 no ME, 190 no DO).'
    )
    description = fields.Text(string='Orientações aos Avaliadores')
    active = fields.Boolean(string='Ativo', default=True)

    item_ids = fields.One2many(
        'capes.scholarship.rubric.item',
        'rubric_id',
        string='Itens Avaliativos'
    )


class CapesScholarshipRubricItem(models.Model):
    """Linha do Barema de Avaliação de Bolsas."""
    _name = 'capes.scholarship.rubric.item'
    _description = 'Item do Barema de Bolsas'
    _order = 'sequence, id'

    rubric_id = fields.Many2one(
        'capes.scholarship.rubric',
        string='Barema',
        required=True,
        ondelete='cascade'
    )
    sequence = fields.Integer(string='Sequência', default=10)
    name = fields.Char(string='Critério / Descrição', required=True)
    category = fields.Selection([
        ('work_plan', 'Plano de Trabalho'),
        ('enade', 'Avaliação ENADE da Graduação'),
        ('graduation_time', 'Tempo de Conclusão da Graduação'),
        ('graduation_grades', 'Média de Notas/Conceitos da Graduação'),
        ('postgrad_previous', 'Mestrado Prévio (Conceito, Depósito, Notas)'),
        ('internship_ic', 'Iniciação Científica e Estágios'),
        ('scientific_production', 'Produção Científica (Periódicos, Congressos, Livros, Patentes)'),
        ('research_projects', 'Projetos de Pesquisa com Recursos'),
        ('dedication', 'Grau de Dedicação à Pós-Graduação'),
        ('professional_experience', 'Experiência Profissional e Cursos de Extensão (Perfil Profissional)'),
        ('other', 'Outros Critérios'),
    ], string='Categoria do Barema', required=True, default='other')

    calculation_formula = fields.Selection([
        ('fixed', 'Pontuação Fixa'),
        ('linear_months', 'Fórmula Linear por Meses (y = ax + b)'),
        ('authorship_split', 'Rateio por Coautoria (Integral <= 2; Dividido se > 2)'),
        ('direct_score', 'Atribuição Direta pelo Revisor (1 a 5 ou Nota)'),
    ], string='Fórmula de Cálculo', required=True, default='fixed')

    base_points = fields.Float(
        string='Pontos Base / Multiplicador',
        default=1.0,
        help='Valor do ponto por unidade ou multiplicador base.'
    )
    linear_factor = fields.Float(
        string='Coeficiente Angular (a)',
        default=0.2,
        help='Valor de "a" na fórmula y = a * meses + b'
    )
    linear_base = fields.Float(
        string='Termo Independente (b)',
        default=1.0,
        help='Valor de "b" na fórmula y = a * meses + b'
    )
    min_months = fields.Integer(string='Meses Mínimos para Pontuar', default=6)
    max_months = fields.Integer(string='Meses Máximos (Teto Linear)', default=34)

    category_cap_points = fields.Float(
        string='Teto da Categoria / Subbloco',
        help='Teto máximo para a soma dos itens desta categoria (ex.: máx. 30 pts em periódicos).'
    )

    def calculate_score(self, quantity=1.0, months=0, num_authors=1, direct_val=0.0):
        """Calcula a nota com base na parametrização sem hardcode."""
        self.ensure_one()
        if self.calculation_formula == 'fixed':
            return self.base_points * quantity
        elif self.calculation_formula == 'direct_score':
            return direct_val
        elif self.calculation_formula == 'linear_months':
            if months < self.min_months:
                return 0.0
            calc_months = min(months, self.max_months) if self.max_months > 0 else months
            score = (self.linear_factor * calc_months) + self.linear_base
            return max(0.0, score)
        elif self.calculation_formula == 'authorship_split':
            # Regra IPEN: integral até 2 autores; se > 2 autores, dividido pelo número total
            split = 1.0 if num_authors <= 2 else float(num_authors)
            return (self.base_points * quantity) / max(1.0, split)
        return 0.0
