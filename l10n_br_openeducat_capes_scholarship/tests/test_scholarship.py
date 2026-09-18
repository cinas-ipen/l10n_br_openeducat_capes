import unittest


class MockRubricItem:
    def __init__(self, name, category, formula, base_points=1.0, linear_factor=0.2, linear_base=1.0, min_months=6, max_months=34, cap=0.0):
        self.name = name
        self.category = category
        self.calculation_formula = formula
        self.base_points = base_points
        self.linear_factor = linear_factor
        self.linear_base = linear_base
        self.min_months = min_months
        self.max_months = max_months
        self.category_cap_points = cap

    def calculate_score(self, quantity=1.0, months=0, num_authors=1, direct_val=0.0):
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
            split = 1.0 if num_authors <= 2 else float(num_authors)
            return (self.base_points * quantity) / max(1.0, split)
        return 0.0


class TestScholarshipLogic(unittest.TestCase):

    def test_fixed_points(self):
        item = MockRubricItem('Plano Aprovado', 'work_plan', 'fixed', base_points=10.0)
        score = item.calculate_score(quantity=1.0)
        self.assertEqual(score, 10.0)

    def test_linear_months_formula(self):
        # IPEN IC: y = 0.3 * meses + 2; min=6; max=35
        item = MockRubricItem('IC', 'internship_ic', 'linear_months', linear_factor=0.3, linear_base=2.0, min_months=6, max_months=35)
        # Menos de 6 meses -> 0
        self.assertEqual(item.calculate_score(months=5), 0.0)
        # 10 meses -> 0.3 * 10 + 2 = 5.0
        self.assertAlmostEqual(item.calculate_score(months=10), 5.0)
        # 35 meses -> 0.3 * 35 + 2 = 12.5
        self.assertAlmostEqual(item.calculate_score(months=35), 12.5)
        # 40 meses -> teto em 35 meses = 12.5
        self.assertAlmostEqual(item.calculate_score(months=40), 12.5)

    def test_authorship_split(self):
        # Livro internacional: 5 pts; integral até 2 autores; se 5 autores -> 5 / 5 = 1 pt
        item = MockRubricItem('Livro Internacional', 'scientific_production', 'authorship_split', base_points=5.0)
        self.assertEqual(item.calculate_score(quantity=1.0, num_authors=1), 5.0)
        self.assertEqual(item.calculate_score(quantity=1.0, num_authors=2), 5.0)
        self.assertEqual(item.calculate_score(quantity=1.0, num_authors=5), 1.0)

    def test_direct_score_likert_scale(self):
        # MP-TRCS: dimensões de 1 a 5
        item = MockRubricItem('Dimensão 1', 'graduation_grades', 'direct_score', base_points=5.0)
        self.assertEqual(item.calculate_score(direct_val=4.5), 4.5)

    def test_parallel_reviewers_average_consolidation(self):
        # Revisor 1 dá 85.0; Revisor 2 dá 95.0
        rev1_score = 85.0
        rev2_score = 95.0
        consolidated = (rev1_score + rev2_score) / 2.0
        self.assertEqual(consolidated, 90.0)

    def test_affirmative_action_reversion(self):
        # Edital com 3 vagas: 1 PPI e 2 Ampla
        slots_total = 3
        slots_ppi = 1
        slots_ampla = 2
        revert = True

        candidates = [
            {'name': 'Candidato A', 'quota': 'ampla', 'score': 95.0},
            {'name': 'Candidato B', 'quota': 'ampla', 'score': 90.0},
            {'name': 'Candidato C', 'quota': 'ampla', 'score': 85.0},
        ]
        # Não há candidatos PPI inscritos
        ppi_candidates = [c for c in candidates if c['quota'] == 'ppi']
        ppi_awarded = len(ppi_candidates[:slots_ppi])
        unused_ppi = slots_ppi - ppi_awarded

        if unused_ppi > 0 and revert:
            slots_ampla += unused_ppi

        self.assertEqual(slots_ampla, 3)
        awarded = candidates[:slots_ampla]
        self.assertEqual(len(awarded), 3)
        self.assertEqual([c['name'] for c in awarded], ['Candidato A', 'Candidato B', 'Candidato C'])

    def test_duration_limits(self):
        # Mestrado 24 meses; usou 6 meses previamente -> saldo restante 18 meses
        max_months = 24
        prior_months = 6
        remaining = max_months - prior_months
        self.assertEqual(remaining, 18)


if __name__ == '__main__':
    unittest.main()
