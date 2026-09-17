### docs/06_titulacao_e_conformidade_documental/02_historico_escolar_consolidado.md

# Documento 02: Histórico Escolar Consolidado (Transcrição)

## 1. A Complexidade da Transcrição Stricto Sensu
O histórico escolar de pós-graduação (`op.student.transcript.br`) é um documento autossuficiente e dotado de fé pública, que consolida a jornada inteira do estudante. Ele difere de um boletim comum porque precisa documentar não apenas as notas, mas as regras sob as quais essas notas foram obtidas e o veredito final da pesquisa.

## 2. Arquitetura de Dados via Odoo QWeb
A engine de relatórios nativa do Odoo (QWeb) é utilizada para fazer um *JOIN* complexo entre quatro domínios isolados do banco de dados:

1. **A Base Regimental (`op.curriculum.version`):** O cabeçalho do documento imprime a portaria MEC de reconhecimento do curso e as exigências totais do regimento escolhido pelo aluno (Ato Jurídico Perfeito).
2. **O Livro-Razão (`op.student.credit.ledger`) e Filtro de Aluno Especial:** O corpo principal itera exclusivamente sobre o livro-razão imutável, consolidando as disciplinas oficiais do percurso regular:
   * *Disciplinas Computadas:* Inclui disciplinas próprias (`subject_internal`), de outros PPGs da IES (`subject_intra_ies`), disciplinas externas convalidadas (`subject_extra_ies`) e disciplinas de regime especial formalmente deferidas pela CPG (`subject_special_incorporated`).
   * *Expurgo de Reprovações e Quarentena de Aluno Especial:* Em estrita observância à parametrização regimental (`special_transcript_fail_policy = 'omit_on_regular'`, padrão MPTRCS), o Histórico Oficial de Titulação omite automaticamente quaisquer reprovações ("R" ou "F") ou disciplinas avulsas não aproveitadas obtidas no regime de aluno especial. Essas atividades figuram exclusivamente na *Certidão de Estudos Isolados*, preservando a idoneidade e o foco exclusivo do percurso de titulação regular.
3. **O Produto Intelectual (`capes.thesis`):** Extração do Título Exato da tese homologada, data da defesa e identificador persistente do Repositório Institucional (URI/Handle).
4. **O Veredito Final (`capes.thesis.committee`):** Listagem nominal de todos os membros da banca examinadora com as respectivas titulações e IES de origem, corroborando a aprovação pública.

## 3. Segurança e Auto-Autenticação
Para eliminar fraudes documentais e a necessidade de carimbos físicos, o relatório QWeb gera automaticamente uma chave de hash SHA-256 baseada nos dados do registo. 

Esta chave é transformada num QR Code e impressa no rodapé do documento. Qualquer auditor ou empregador pode scannear o código, que o redirecionará para um endpoint público do OpenEduCat (`/valida-documento`), confirmando a autenticidade dos dados ali impressos diretamente da "Fonte Prata".
