### docs/06_titulacao_e_conformidade_documental/03_diploma_digital_nato_digital.md

# Governança de Expedição e Registro de Diplomas – Dualidade de Modelos (IPEN/USP) e Suporte Híbrido (Digital / Físico)

## 1. O Marco Regulatório e as Modalidades de Emissão

A expedição de diplomas de pós-graduação *Stricto Sensu* (Mestrado e Doutorado) no Brasil vivencia uma fase de transição normativa e tecnológica:

- **Portaria MEC nº 70/2025 (Nato-Digital):** Estabelece as especificações do Diploma Digital assinado via ICP-Brasil (XAdES-BES com Carimbo de Tempo e Representação Visual RVDD).
- **Emissão Tradicional / Híbrida em Papel:** Tendo em vista que o Ministério da Educação (MEC) implementou integralmente a obrigatoriedade do diploma digital prioritariamente para os cursos de Graduação, os Programas de Pós-Graduação *Stricto Sensu* mantêm operacionalmente a emissão de diplomas físicos em papel com trâmite de registro formal em Livro de Registro físico/digital.

O submódulo `l10n_br_openeducat_capes_diploma` foi arquitetado para suportar **ambos os formatos** (`emission_format`):
- `digital`: Nato-Digital em XML com envelope XAdES e RVDD (MEC 70/2025).
- `paper_hybrid`: Diploma Físico em Papel com protocolo de remessa, averbação em Livro de Registro e chancela digital do dossiê.
- `both`: Emissão Simultânea (Digital + Físico em Papel).

---

## 2. Modelos de Governança Institucional (`issuing_ies_type`)

O ERP diferencia dois arranjos institucionais de outorga de graus acadêmicos:

### Modelo A: Autonomia Registradora Direta (`autonomous_university`)
Aplicável a Universidades (Federais, Estaduais ou Privadas com autonomia) que possuem prerrogativa legal para registrar autonomamente os diplomas por elas emitidos (`origin_ies_name` == `issuing_ies_name`).

### Modelo B: Registro via IES Registradora Externa (`external_registering_university`)
Aplicável a Institutos de Pesquisa e Faculdades isoladas — como o **Instituto de Pesquisas Energéticas e Nucleares (IPEN-CNEN/SP)** —, os quais ministram o ensino e possuem excelência acadêmica, mas **não possuem autonomia universitária direta para o registro autônomo de diplomas**.

No caso do MP-TRCS e demais cursos do IPEN:
- **IES / Instituto de Origem (`origin_ies_name`):** Instituto de Pesquisas Energéticas e Nucleares (IPEN-CNEN/SP).
- **IES Emissora / Registradora (`issuing_ies_name`):** Universidade de São Paulo (USP), responsável pela escrituração do registro de diploma em seus livros e pela expedição/averbação formal do título.

---

## 3. Estrutura do "Pacote de Titulação" e Tramitação Interinstitucional

Independentemente do formato (Digital ou Físico), o Odoo consolida o **Pacote de Titulação** no IPEN após a aprovação da defesa e validação da versão final:

1. **Selagem do Lastro Acadêmico (IPEN):** Compilação do histórico escolar *append-only* (`op.student.credit.ledger`), ata da comissão julgadora e comprovante do Produto Técnico-Tecnológico (PTT).
2. **Cálculo da Chave Hash SHA-256:** Geração da impressão digital criptográfica única para imutabilidade do processo.
3. **Remessa para a IES Registradora (USP):**
   - *No formato Físico/Papel:* Registro da `physical_dispatch_date` (Data de Remessa do Processo) e posterior averbação do `registration_book_number` (Livro de Registro) e `registration_page_number` (Folha/Página) atribuídos pela Pró-Reitoria de Pós-Graduação da USP.
   - *No formato Digital:* Transmissão via API do manifesto XML para validação e assinatura XAdES pela USP.

---

## 4. Matriz de Campos do Modelo `capes.digital.diploma`

| Campo Odoo | Descrição | Tipo | Uso / Regra de Negócio |
| :--- | :--- | :--- | :--- |
| `issuing_ies_type` | Governança do Registro | `Selection` | `autonomous_university` vs. `external_registering_university` (IPEN $\rightarrow$ USP). |
| `emission_format` | Formato de Emissão | `Selection` | `digital` (MEC 70/2025), `paper_hybrid` (Físico em Papel), `both`. |
| `origin_ies_name` | IES de Origem | `Char` | Ex: Instituto de Pesquisas Energéticas e Nucleares - IPEN-CNEN/SP. |
| `issuing_ies_name` | IES Registradora | `Char` | Ex: Universidade de São Paulo - USP. |
| `registration_book_number` | Livro de Registro | `Char` | Número do Livro de Registro de Diplomas (ex: Livro 42-B). |
| `registration_page_number` | Folha / Página | `Char` | Folha ou Página do registro (ex: Fls. 118). |
| `registration_date` | Data do Registro | `Date` | Data de efetivação do registro na IES Registradora (USP). |
| `physical_dispatch_date` | Data de Remessa | `Date` | Data de envio do protocolo físico para a USP. |
| `sha256_hash` | Hash de Autenticidade | `Char` | Chave SHA-256 gerada para selagem do processo. |
