# **Validação Técnica MP7 - Expedição Documental, Registro Interinstitucional (USP) e Diplomas (Físico / Digital)**

## **1. Introdução e Finalidade**

O **Macroprocesso 07** operacionaliza o encerramento do vínculo acadêmico no contexto do **IPEN-CNEN/SP**:

1. **IPEN (Origem / Validação Acadêmica):** Responsável pela auditoria final, consolidação do dossiê acadêmico e conferência de elegibilidade de titulação.
2. **USP (Universidade Registradora Externa):** Tendo em vista que o IPEN é um instituto de pesquisa (sem autonomia universitária direta para escrituração autônoma de diplomas), a **Universidade de São Paulo (USP)** atua como IES Registradora encarregada do registro formal do diploma.
3. **Dualidade de Formatos (Físico em Papel e Nato-Digital MEC 70/2025):** Tendo em vista que o MEC priorizou a implementação obrigatória do diploma digital na graduação, a pós-graduação *Stricto Sensu* do MP-TRCS utiliza a emissão em papel com protocolo de remessa para registro na USP (Livro de Registro e Folha), estando o Odoo preparado para a transição nato-digital simultânea (`emission_format` = `paper_hybrid` / `digital` / `both`).

A finalidade deste processo no ERP é compilar o "Pacote de Titulação" com rigor criptográfico e auditabilidade, atendendo tanto ao trâmite impresso em papel quanto ao modelo nato-digital.

---

## **2. O Pacote de Titulação (IPEN $\rightarrow$ USP)**

Uma vez que o discente atinge o status "Titulado" no IPEN (após o upload da versão final do PDF pelo discente e a chancela/validação da Secretaria Acadêmica), o sistema congela a vida acadêmica e prepara o **Dossiê Digital de Expedição** a ser transmitido/encaminhado para a USP.

Este pacote contém:

* **Histórico Escolar Consolidado:** Carga horária total em horas (100 créditos = 1.500h), disciplinas cursadas, conceitos e nota final.
* **Evidências de Defesa:** Ata de defesa com a composição da banca (identificando os membros externos) e a validação do quórum regimental.  
* **Evidências de PTT:** Registro do PTT homologado, com seu respectivo estrato Qualis e Handle URI do Repositório Institucional (DSpace).  
* **Hash SHA-256 de Integridade:** O ERP IPEN gera uma chave criptográfica SHA-256 para selagem do processo.

---

## **3. Fluxo de Expedição (Workflow IPEN-USP)**

`[IPEN: Auditoria de Elegibilidade Final (Créditos, PTT, Defesa, CEP)]`  
               `│`  
               `▼`  
`[IPEN/ERP: Compila Dossiê Digital + Selagem com Hash SHA-256]`  
               `│`  
               `▼`  
`[IPEN -> USP: Remessa do Processo Físico / Transmissão via API]`  
               `│`  
               `▼`  
`[USP: Escrituração no Livro de Registro de Diplomas (Livro / Folha)]`  
               `│`  
               `▼`  
`[IPEN/Odoo: Averbação do Livro/Folha e Conclusão do Processo]`

---

## **4. Governança e Responsabilidades (Matriz de Stakeholders)**

| Ator | Responsabilidade no Processo |
| :---- | :---- |
| **IPEN (Secretaria/CPG)** | Auditoria acadêmica, consolidação do dossiê, remessa do diploma/processo e averbação. |
| **USP (Pró-Reitoria de Pós-Graduação)** | Registro oficial do grau acadêmico, escrituração no Livro de Registro e emissão/autenticação. |
| **ERP (OpenEduCat)** | Motor de auditoria, cálculo de créditos, gestão de livros de registro e selagem criptográfica (Hash SHA-256). |

---

## **5. Roteiro para Reunião de Validação (Secretaria IPEN e Pró-Reitoria USP)**

Para validar este fluxo de expedição, sugiro focar nos seguintes pontos de pauta:

1. **Protocolo de Remessa do Processo:** Definir a fluxo de envio físico do diploma impressos em papel e do histórico escolar para a USP.
2. **Escrituração de Livro e Folha:** Confirmar o preenchimento dos campos `registration_book_number` e `registration_page_number` no Odoo após o retorno do protocolo da USP.
3. **Chancela Digital e QR Code:** Testar o QR Code de acesso público e a chave Hash SHA-256 gravados no rodapé dos documentos emitidos pelo IPEN.
