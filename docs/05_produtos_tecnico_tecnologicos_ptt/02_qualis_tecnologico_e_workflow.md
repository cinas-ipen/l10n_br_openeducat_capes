# Documento 02: O Motor de Aderência e os Workflows de Validação do PTT

## 1. O Paradigma da Aderência e Flexibilidade por Programa

Nos Mestrados e Doutorados Profissionais, a entrega do Produto Técnico-Tecnológico (PTT) é condição estrutural para a titulação. O ERP OpenEduCat suporta múltiplos modos de validação de PTT via parâmetro `ptt_validation_mode`, garantindo que cada IES ou programa aplique as suas regras regimentais sem engessamento de código.

## 2. Workflow V1: Modelo Checklist + Dupla Anuência + Homologação CPG (MPTRCS)

Para a primeira versão do sistema (aplicada ao MPTRCS/IPEN e customizável para outros PPGs), adota-se o modo `cpg_checklist`. O PTT não exige uma câmara prévia de avaliação complexa antes do pedido de defesa; sua validação é integrada ao fluxo de agendamento da dissertação:

```text
[Aluno: Preenche Requerimento de Defesa no Portal]
  │   └── Seleciona PTT do Checklist CAPES + Anexa Evidências
  ▼
[Orientador Principal: Emite Aceite / "De acordo"]
  │
  ▼
[Coorientador (se houver): Emite Aceite / "De acordo"]
  │
  ▼
[Secretaria Acadêmica: Triagem Técnico-Documental]
  │   └── Valida conformidade do anexo e marca: ready_for_agenda
  ▼
[Pauta da Reunião da CPG (op.cpg.meeting)]
  │   └── Colegiado avalia o PTT e delibera aprovação
  ▼
[Aprovação da Ata CPG] ──► [Workflow de Defesa Liberado]
```

1. **Indicação e Checklist no Portal:** No ato da submissão do requerimento de defesa da dissertação, o discente seleciona a tipologia do PTT gerado dentre as opções oficiais cadastradas da CAPES (21 tipos GTPT / 10 subcategorias Medicina II) e realiza o upload dos comprovantes.
2. **Dupla Anuência Eletrônica (Orientador e Coorientador):** O chamado é roteado para os painéis dos docentes. O Orientador e o Coorientador (quando houver) devem registrar o aceite eletrônico ("De acordo"), atestando que o PTT reflete os resultados do trabalho.
3. **Triagem da Secretaria:** A secretaria verifica se a documentação anexada corresponde à tipologia indicada e marca o chamado como `ready_for_agenda` (Apto para Pauta).
4. **Pauta e Deliberação da CPG:** O requerimento é incluído na pauta da reunião seguinte da CPG (`op.cpg.meeting`). A CPG avalia se o PTT cumpre o regulamento do programa e delibera a aprovação formal, liberando o agendamento da defesa.

## 3. Workflow V2: Avaliação e Estratificação Prévia no Qualis Tecnológico (`qualis_prior`)

Para programas que exigem que o PTT possua estrato atribuído (T1 a T5) antes da defesa, o sistema ativa o modo `qualis_prior` com a seguinte máquina de estados (`state` em `capes.ptt.product`):

1. **`draft` (Rascunho):** O discente preenche os metadados e a justificativa de aderência.
2. **`adherence_check` (Auditoria de Aderência):** Decisão binária do orientador/comissão. Rejeição envia para `rejected` (TNC - Produto Não Classificado).
3. **`evaluating` (Em Avaliação Qualis):** Atribuição de notas nas 4 dimensões (Impacto, Inovação, Aplicabilidade TRL 1-9 e Complexidade).
4. **`homologated` (Homologado):** Consolidação do Estrato (T1 a T5), injeção no Livro-Razão e liberação do agendamento da defesa.

## 4. O Registo Transacional: O Produto (`capes.ptt.product`)
A entidade central submetida pelo discente ou docente. É o objeto que será depositado na "Fonte Ouro" (DSpace).

| Campo Odoo | Metadado / Conceito CAPES | Tipo de Dado Odoo | Domínio / Regras de Validação |
| :--- | :--- | :--- | :--- |
| `type_id` | Tipo do Produto | `Many2one` | FK para `capes.ptt.type`. |
| `student_id` | Discente Autor (Principal) | `Many2one` | FK para `op.student`. |
| `thesis_id` | Tese / Dissertação Associada| `Many2one` | FK para `capes.thesis`. Produto que serve como TCC. |
| `title` | Título do Produto | `Char` | Nome exato do desenvolvimento. |
| `trl_level` | Nível de Maturidade (TRL) | `Selection` | Níveis de 1 (Princípios básicos observados) a 9 (Sistema provado em ambiente real). |
| `adherence_justif`| Justificação de Aderência | `Text` | OBRIGATÓRIO: Texto discursivo onde o autor defende a ligação do produto com a Linha de Pesquisa do PPG. |
| `is_adherent` | Validação de Aderência | `Boolean` | Campo de controlo da comissão. Se validado como `False`, o produto sofre glosa imediata e não segue para avaliação. |
| `target_audience` | Público-Alvo / Beneficiários | `Text` | Identificação do setor produtivo, governo ou sociedade civil impactada. |
| `financing_agency`| Agência de Financiamento | `Many2one` | FK para entidade parceira ou de fomento (se aplicável). |
| `repository_url` | URL do Produto (DSpace) | `Char` | Ligação OAI-PMH para a Fonte Ouro. |

## 5. Estrutura de Autoria e Taxonomia (`capes.ptt.author`)
Como os PTTs são frequentemente colaborativos (ex: desenvolvimento de um software clínico), os coautores precisam de rastreabilidade.

| Campo Odoo | Metadado / Conceito CAPES | Tipo de Dado Odoo | Domínio / Regras de Validação |
| :--- | :--- | :--- | :--- |
| `product_id` | Produto Vinculado | `Many2one` | FK para `capes.ptt.product`. |
| `partner_id` | Coautor | `Many2one` | FK para `res.partner`. |
| `author_role` | Papel na Criação | `Selection` | Desenvolvedor Principal, Orientador, Validador Técnico, Financiador. |
| `ip_share` | Quota de Patente (%) | `Float` | Percentagem de titularidade em caso de geração de Propriedade Intelectual. |
