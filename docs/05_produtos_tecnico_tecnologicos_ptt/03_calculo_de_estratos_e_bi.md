### docs/05_produtos_tecnico_tecnologicos_ptt/03_calculo_de_estratos_e_bi.md

# Documento 03: Motor de Estratificação e Inteligência Analítica (BI)

## 1. O Cálculo Estruturado do Qualis Tecnológico
A subjetividade da banca é limitada pelo algoritmo do Odoo, que transpõe o baremo oficial da CAPES (Área de Ensino e Interdisciplinar) para a classe `capes.ptt.evaluation`.

A nota final não é uma atribuição direta, mas sim a soma de quatro dimensões ponderadas e isoladas que, combinadas, geram uma pontuação máxima de 100 pontos:

1. **Impacto e Demanda (30 pts):** Avalia se a demanda foi induzida pela IES ou trazida pela sociedade, e qual o raio de impacto (local, regional, nacional).
2. **Inovação e Originalidade (25 pts):** Cruza a novidade com o nível de maturidade (TRL declarado).
3. **Aplicabilidade e Replicabilidade (25 pts):** Mede a facilidade de adoção do produto por terceiros sem a intervenção contínua dos criadores.
4. **Complexidade (20 pts):** Valida a exigência da infraestrutura de pesquisa e as interações multidisciplinares exigidas para criar o produto.

## 2. O Motor de Avaliação: Qualis Tecnológico (`capes.ptt.evaluation`)
O painel de pontuação utilizado pela comissão avaliadora do PPG para estratificar o produto. A lógica obedece a um algoritmo Python com o decorador `@api.depends`.

| Campo Odoo | Metadado / Conceito CAPES | Tipo de Dado Odoo | Domínio / Regras de Validação |
| :--- | :--- | :--- | :--- |
| `product_id` | Produto Avaliado | `Many2one` | FK para `capes.ptt.product`. |
| `evaluator_id` | Avaliador (Docente/Externo)| `Many2one` | FK para `res.partner` (Membro da comissão). |
| `dim_impact` | Demanda e Impacto | `Float` | Escala de 0 a 30 pontos. |
| `dim_innovation`| Inovação / Originalidade | `Float` | Escala de 0 a 25 pontos. |
| `dim_applicability`| Aplicabilidade / Replicab. | `Float` | Escala de 0 a 25 pontos. |
| `dim_complexity`| Complexidade | `Float` | Escala de 0 a 20 pontos. |
| `total_score` | Pontuação Total | `Float` | Campo computado (Read-Only): Soma das 4 dimensões. Máx: 100 pontos. |
| `final_stratum` | Estrato Final Calculado | `Selection` | T1 (90-100), T2 (75-89), T3 (60-74), T4 (45-59), T5 (30-44), TNC (<30 ou Não Aderente). Calculado automaticamente pelo Odoo. |


## 3. Algoritmo em Python e Determinação do Estrato (T1 a T5)
O núcleo da avaliação é gerido por um método protegido com o decorador `@api.depends`, garantindo que qualquer edição na nota das dimensões recalcula em tempo real o Estrato Final.

```python
class CapesPttEvaluation(models.Model):
    _name = 'capes.ptt.evaluation'
    
    # ... declaração de campos de dimensão ...

    @api.depends('dim_impact', 'dim_innovation', 'dim_applicability', 'dim_complexity', 'product_id.is_adherent')
    def _compute_final_stratum(self):
        for eval in self:
            # Trava Lógica de Aderência: O requisito primário
            if not eval.product_id.is_adherent:
                eval.total_score = 0
                eval.final_stratum = 'TNC' # Produto Não Classificado
                continue
                
            # Somatório das Dimensões
            score = sum([eval.dim_impact, eval.dim_innovation, 
                         eval.dim_applicability, eval.dim_complexity])
            eval.total_score = score
            
            # Classificação por Corte Paramétrico
            if score >= 90:
                eval.final_stratum = 'T1'
            elif score >= 75:
                eval.final_stratum = 'T2'
            elif score >= 60:
                eval.final_stratum = 'T3'
            elif score >= 45:
                eval.final_stratum = 'T4'
            elif score >= 30:
                eval.final_stratum = 'T5'
            else:
                eval.final_stratum = 'TNC'
```

## 4. Inteligência Analítica e Odoo BI Views
Para o coordenador do Mestrado Profissional, o sucesso da avaliação quadrienal depende da monitorização da "Densidade de Impacto" do seu programa. A arquitetura de interface de utilizador (UI) desenvolve as seguintes ferramentas de Business Intelligence nativas:

* **Matriz Pivot (TRL x Inovação):** Uma `pivot view` nativa do Odoo que cruza as 21 Tipologias de PTT no eixo Y com a Escala TRL no eixo X. O coordenador pode visualizar de relance se o programa está a produzir muito "Software TRL 3" (baixa maturidade) ou "Patentes TRL 8" (alta maturidade).
* **Dashboard Gráfico de Estratos:** Uma `graph view` (formato *doughnut*) que totaliza a massa de produção validada. Se a maioria do gráfico apontar para `T4` e `T5`, o coordenador recebe um alerta visual e acionável de que as bancas estão a considerar as entregas de baixa relevância/complexidade.
* **Controle Kanban de Homologação:** Interface visual baseada em cartões que permite ao colegiado arrastar PTTs do estado `evaluating` para `homologated`, selando o fecho da avaliação de cada discente.
