### docs/06_titulacao_e_conformidade_documental/02_historico_escolar_consolidado.md

# Documento 02: Histórico Escolar Consolidado (Transcrição)

## 1. A Complexidade da Transcrição Stricto Sensu
O histórico escolar de pós-graduação (`op.student.transcript.br`) é um documento autossuficiente e dotado de fé pública, que consolida a jornada inteira do estudante. Ele difere de um boletim comum porque precisa documentar não apenas as notas, mas as regras sob as quais essas notas foram obtidas e o veredito final da pesquisa.

## 2. Arquitetura de Dados via Odoo QWeb
A engine de relatórios nativa do Odoo (QWeb) é utilizada para fazer um *JOIN* complexo entre quatro domínios isolados do banco de dados:

1. **A Base Regimental (`op.curriculum.version`):** O cabeçalho do documento imprime a portaria MEC de reconhecimento do curso e as exigências totais do regimento escolhido pelo aluno (Ato Jurídico Perfeito).
2. **O Livro-Razão (`op.student.credit.ledger`):** O corpo principal itera exclusivamente sobre o livro-razão imutável, listando disciplinas cursadas, conceitos (A, B, C, R), frequência e totalização de horas-aula vs. créditos integralizados.
3. **O Produto Intelectual (`capes.thesis`):** Extração do Título Exato da tese homologada, data da defesa e identificador persistente do Repositório Institucional (URI/Handle).
4. **O Veredito Final (`capes.thesis.committee`):** Listagem nominal de todos os membros da banca examinadora com as respectivas titulações e IES de origem, corroborando a aprovação pública.

## 3. Segurança e Auto-Autenticação
Para eliminar fraudes documentais e a necessidade de carimbos físicos, o relatório QWeb gera automaticamente uma chave de hash SHA-256 baseada nos dados do registo. 

Esta chave é transformada num QR Code e impressa no rodapé do documento. Qualquer auditor ou empregador pode scannear o código, que o redirecionará para um endpoint público do OpenEduCat (`/valida-documento`), confirmando a autenticidade dos dados ali impressos diretamente da "Fonte Prata".
