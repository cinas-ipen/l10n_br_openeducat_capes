### docs/06_titulacao_e_conformidade_documental/03_diploma_digital_nato_digital.md

# Governança de Expedição de Diplomas – Integração IPEN (Origem) e USP (Instituição Registradora Emissora)

## 1. O Marco Regulatório e a Realidade Institucional (Portaria MEC nº 70/2025)

A expedição de diplomas de pós-graduação *Stricto Sensu* rege-se pela Portaria MEC nº 70/2025, que proíbe o formato físico em papel como documento oficial, exigindo a entidade "Nato-Digital" sob a forma de arquivo XML criptografado.

No ecossistema do Programa de Pós-Graduação em Tecnologia das Radiações em Ciências da Saúde (MPTRCS), o **Instituto de Pesquisas Energéticas e Nucleares (IPEN-CNEN/SP)** atua como unidade técnico-científica de ensino, mas **não possui autonomia legal direta para o registro autônomo de graus acadêmicos**, competindo esta atribuição institucional à **Universidade de São Paulo (USP)**, à qual o programa está formalmente vinculado e associado para fins de outorga de títulos.

Portanto, o submódulo `l10n_br_openeducat_capes_diploma` opera em duas camadas coordenadas:

1. **IPEN (Fonte Prata e Ouro):** Orquestra a auditoria integral da vida acadêmica, a defesa, a homologação do PTT, a validação da versão final do PDF e a geração do manifesto para o Repositório Institucional (DSpace), gerando e selando o **Pacote de Titulação**.
2. **USP (Autoridade Registradora Emissora):** Recebe o pacote validado, processa a homologação final do registro acadêmico e emite oficialmente o Diploma Nato-Digital.

---

## 2. A Composição do "Pacote de Titulação" (IPEN $\rightarrow$ USP)

Uma vez que o discente atinge o status de "Titulado" no ERP do IPEN (após o upload da versão final em PDF pelo discente e a chancela/validação da Secretaria Acadêmica), o sistema empacota os dados para transmissão segura à USP, contendo:

* **XML de Lastro Acadêmico:** Extraído diretamente das tabelas *append-only* do Livro-Razão (`op.student.credit.ledger`), contendo o histórico escolar consolidado com conversão de créditos em horas-aula e as assinaturas de regimento (Ato Jurídico Perfeito).
* **Ata de Defesa e Dossiê da Banca:** Metadados da comissão julgadora (`capes.thesis.committee`), comprovando o quórum de doutores, a participação de membros externos e a inexistência de endogenia ou impedimentos.
* **Comprovação do PTT:** Identificação do Produto Técnico-Tecnológico validado com seu estrato Qualis e evidências anexadas.

---

## 3. Orquestração Criptográfica e Expedição pela USP

Com base no pacote enviado pelo IPEN, a infraestrutura da USP executa a esteira tecnológica de expedição regulada pela Portaria MEC nº 70/2025:

* **Estruturação dos XMLs Oficiais:** Geração do XML do Diploma Digital (dados civis, grau de Mestre Profissional, reconhecimento CAPES) e do XML da Documentação Acadêmica (histórico).
* **Assinatura Avançada XAdES (ICP-Brasil):** Aplicação de assinaturas digitais com certificados corporativos institucionais A3/HSM da Reitoria da USP e da unidade registradora.
* **Carimbo de Tempo (Timestamp):** Injeção de carimbo de tempo por Autoridade de Certificação homologada para assegurar a perenidade e a imutabilidade da data de outorga do grau.

---

## 4. Representação Visual e Transparência (RVDD)

Para legibilidade do mercado e dos egressos, a USP gera a **Representação Visual do Diploma Digital (RVDD)** em PDF de alta resolução, contendo:

* O brasão institucional e os selos de registro.
* Um **QR Code** de acesso público que aponta diretamente para o validador digital da USP e para os metadados validados na Fonte Prata do IPEN.

---
