# Documento 02: Histórico Escolar Consolidado de Pós-Graduação (Transcrição Oficial)

## 1. A Complexidade da Transcrição Stricto Sensu
O histórico escolar de pós-graduação (`report_student_transcript_br_document` em `l10n_br_openeducat_capes_diploma`) é um documento autossuficiente e dotado de fé pública, que consolida a jornada inteira do discente. Ele difere substancialmente de um boletim escolar comum porque documenta não apenas as notas e créditos, mas as regras regimentais sob as quais foram obtidos (Ato Jurídico Perfeito), a filiação ao Programa de Pós-Graduação da CAPES e o rito de defesa pública final com registro no Repositório Institucional.

## 2. Arquitetura de Dados via Odoo QWeb (Wkhtmltopdf)
A engine de relatórios nativa do Odoo (QWeb) consolida dados de múltiplos domínios do banco relacional de forma integrada e performática:

### 2.1. Cabeçalho e Identificação Acadêmica
* **Identificação do Discente:** Nome completo (`o.partner_id.name`) e CPF (`o.partner_id.cpf`).
* **Programa e Código SNPG/CAPES:** Nome oficial do programa (`o.program_id.name`) e código de 12 dígitos no Sistema Nacional de Pós-Graduação (`o.program_id.snpg_code`).
* **Registro Acadêmico Institucional (RA):** Número perene de matrícula na IES (`o.ra_number`), preservado ao longo de toda a vida acadêmica.
* **Datas e Versão Regimental:** Data oficial de admissão regular (`o.admission_date`), Versão Regimental ativa sob a égide do Ato Jurídico Perfeito (`o.curriculum_version_id.name`) e Situação Acadêmica discente (`o.capes_status`).

### 2.2. Integralização Curricular via Livro-Razão Acadêmico (`op.student.credit.ledger`)
O corpo principal itera exclusivamente sobre o livro-razão imutável (*append-only*), ordenado cronologicamente por `date_earned asc, id asc`:
* **Código e Denominação da Atividade:** Código oficial da disciplina (`ledger.subject_id.code`) e denominação da atividade (`ledger.course_name`).
* **Carga Horária e Créditos:** Horas computadas com conversão regimental (`ledger.hours`) e créditos concedidos (`ledger.credits`).
* **Conceito / Nota Obtida:** Conceito regimental oficial (`ledger.grade_concept`, ex: A, B, C, D).
* **Resultado:** Situação de aprovação (`is_approved`: Aprovado em destaque verde ou Reprovado em destaque vermelho).
* **Política de Aluno Especial:** Em conformidade com a regra regimental `omit_on_regular`, disciplinas cursadas em regime especial que não foram formalmente incorporadas via CPG permanecem em quarentena e não figuram no histórico oficial de titulação regular, compondo apenas a Certidão de Estudos Isolados.

### 2.3. Rito Público de Conclusão e Defesa (`capes.thesis`)
Quando o discente atinge a fase de defesa, o relatório extrai automaticamente os dados da banca homologada:
* **Título Final Aprovado em Ata:** Redação exata homologada pela comissão examinadora (`defense.title`).
* **Data da Sessão Pública:** Data e horário da sessão solene de defesa (`defense.defense_date`).
* **Repositório DSpace (Handle/URI):** Identificador permanente gerado pela biblioteca institucional (`defense.repository_url`), conectando a Fonte Prata à Fonte Ouro.
* **Situação do Rito:** Status oficial homologado (`defense.status`). Caso o aluno ainda não tenha defendido, o documento estampa: *"Nenhuma defesa final registrada ou homologada até a presente data"*.

## 3. Segurança Criptográfica, QR Code e Conformidade MEC (Portaria nº 70/2025)
Para assegurar integridade jurídica nato-digital e eliminar a necessidade de carimbos físicos analógicos:
* O rodapé estampa a chancela formal da **Portaria MEC nº 70/2025**.
* Um quadro de **QR Code de Validação Pública** permite a conferência instantânea por órgãos externos, empregadores e agências de fomento, direcionando para o endpoint `/valida-documento` onde a assinatura digital e o hash SHA-256 do histórico escolar podem ser auditados online.
