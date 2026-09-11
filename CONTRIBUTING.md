# Guia de Contribuição (`CONTRIBUTING.md`)

Agradecemos o seu interesse em contribuir para o **`l10n_br_openeducat_capes`**! Este projeto tem como missão disponibilizar uma localização brasileira aberta, robusta e regimentalmente aderente ao Odoo 19.0 e OpenEduCat 19.0 para Programas de Pós-Graduação *Stricto Sensu* (Mestrado Acadêmico/Profissional e Doutorado) de todas as IES e Institutos de Pesquisa do Brasil.

---

## 🏛️ Regras de Ouro da Arquitetura

Antes de submeter qualquer código, certifique-se de que a sua contribuição respeita os 4 pilares arquiteturais do projeto:

1. **Proibição Absoluta de Hardcode Regimental:** Nenhuma regra de prazo, quórum de banca, fatores de conversão de créditos ou proficiências pode ser fixa (*hardcoded*) em Python. Todas as validações devem consultar a entidade de versionamento regimental (`op.curriculum.version`).
2. **Imutabilidade do Livro-Razão (Append-Only):** As tabelas financeiras/acadêmicas de livro-razão (`op.student.credit.ledger` e `op.faculty.category.ledger`) funcionam em modo estritamente aditivo (*append-only*). Nunca crie métodos que permitam exclusão (`unlink`) ou recálculo destrutivo em lançamentos já homologados.
3. **Respeito ao Ato Jurídico Perfeito (CF/88):** Alterações em regimentos ou versões curriculares futuras nunca devem afetar retroativamente o histórico de alunos sob regimentos anteriores.
4. **Segurança Obrigatória:** Todo novo modelo Python criado deve ter obrigatoriamente a sua entrada de permissão no arquivo `security/ir.model.access.csv` do seu respectivo submódulo.

---

## 🔄 Workflow de Contribuição (Git / GitLab / GitHub)

1. **Faça um Fork** do repositório para o seu perfil ou organização.
2. **Crie uma Branch** temática a partir da `main`:
   ```bash
   git checkout -b feature/minha-nova-funcionalidade
   # ou
   git checkout -b fix/correcao-bug-creditos
   ```
3. **Desenvolva e Teste** localmente no ambiente Docker:
   ```bash
   docker compose up -d --build
   ```
4. **Faça Commits Claros e Semânticos:**
   ```bash
   git commit -m "feat(academic): adiciona campo de trava de prorrogação na versão regimental"
   ```
5. **Submita um Pull Request / Merge Request** com uma descrição detalhada da alteração, motivando a necessidade técnica ou funcional e citando portarias ou regulamentos aplicáveis, se houver.

---

## 🐍 Padrões de Código e Convenções (Odoo 19)

### Python (PEP 8)
- Indentação de **4 espaços** (sem tabulações).
- Nome de modelos em ponto: `op.curriculum.version`.
- Nome de campos em *snake_case*: `max_extension_months`.
- Utilização estrita de `@api.depends` especificando apenas os campos diretamente auditados.
- Métodos computados devem ser idempotentes e seguros contra valores nulos (`None` / `False`).

### XML (Views e Data)
- Identação de **4 espaços**.
- IDs de registros formatados por convenção:
  - Form Views: `view_[modelo_simplificado]_form`
  - Tree/List Views: `view_[modelo_simplificado]_tree`
  - Search Views: `view_[modelo_simplificado]_search`
  - Actions: `action_[modelo_simplificado]`
  - Menus: `menu_[modelo_simplificado]`

---

## 🐛 Relatando Bugs ou Sugerindo Melhorias

Ao abrir uma *Issue*:
- Descreva o comportamento esperado vs. o comportamento observado.
- Inclua o passo a passo para reproduzir o problema.
- Anexe tracebacks ou logs relevantes extraídos do comando `docker compose logs odoo`.
- Se a sugestão envolver normativas da CAPES ou MEC, cite a Portaria ou Instrução Normativa correspondente.

Muito obrigado por ajudar a fortalecer a pós-graduação pública e aberta no Brasil! 🇧🇷
