# Documento 01: Taxonomia GTPT - Eixos Estruturantes e Tipologias Medicina II / CAPES

## 1. O Desafio da Padronização da Produção Técnica

Nos Mestrados e Doutorados Profissionais, a produção do egresso afasta-se da bibliometria clássica (artigos e livros) e foca-se na intervenção real na sociedade ou no mercado. Para viabilizar a avaliação destas entregas na Plataforma Sucupira, o Grupo de Trabalho de Produção Técnica (GTPT) e o Comitê da Área de Medicina II / Ensino da CAPES estabeleceram uma ontologia rígida e fechada.

A arquitetura do `l10n_br_openeducat_capes_ptt` proíbe a inserção manual de categorias de produtos pelos utilizadores. Toda a árvore de taxonomia é pré-populada no banco de dados via arquivos XML de dados (`data/ptt_taxonomy_data.xml`) durante a instalação do módulo.

## 2. Os 4 Eixos Estruturantes (`capes.ptt.axis`)

A classe representa as grandes dimensões de impacto aprovadas pela CAPES. O registro de qualquer produto exige a vinculação obrigatória a um eixo primário:

* **Eixo 1 - Produtos e Processos:** Inovação tangível, patentes, softwares, hardwares, metodologias de intervenção clínica/radiológica e tecnologias sociais.
* **Eixo 2 - Formação:** Impacto na capacitação humana, como elaboração de cursos de qualificação, materiais didáticos complexos, manuais operacionais e propostas de currículos.
* **Eixo 3 - Divulgação e Difusão:** Democratização do conhecimento técnico, incluindo organização de eventos tecnológicos, exposições, curadoria de dados públicos e relatórios técnicos.
* **Eixo 4 - Serviços Técnicos:** Prestação de assessoria ao Estado ou à indústria, laudos radiológicos/nucleares complexos, normas técnicas e marcos regulatórios.

### 2.1. Tabela de campos dos Eixos Estruturantes (`capes.ptt.axis`)
Os quatro grandes pilares de classificação da produção técnica.

| Campo Odoo | Metadado / Conceito CAPES | Tipo de Dado Odoo | Domínio / Regras de Validação |
| :--- | :--- | :--- | :--- |
| `code` | Código do Eixo | `Char` | Ex: E1, E2, E3, E4. |
| `name` | Nome do Eixo | `Char` | Produtos e Processos, Formação, Divulgação, Serviços Técnicos. |
| `description` | Descrição Normativa | `Text` | Texto explicativo da diretriz da CAPES. |


## 3. As 10 Subcategorias do Comitê Medicina II e as 21 Tipologias GTPT (`capes.ptt.type`)

O módulo realiza o mapeamento biunívoco entre os 21 Tipos oficiais do GTPT (T01 a T21) e as **10 Subcategorias de Entrega** exigidas nos relatórios de avaliação do programa MPTRCS/IPEN (Medicina II):

1. **Ativos de Propriedade Intelectual:** Patente depositada/concedida (T13), Registro de Software / Aplicativo (T19). *Exige comprovante INPI.*
2. **Artigo Científico em Periódico Indexado:** Publicação aceita/publicada em revista indexada na base *Web of Science* / Scopus.
3. **Empresa ou Organização Social Inovadora:** *Spin-off* acadêmica ou *startup* de tecnologia em saúde (T11).
4. **Curso de Formação Profissional:** Capacitação presencial/EAD elaborada para o SUS ou setor produtivo (T08).
5. **Norma ou Marco Regulatório:** Proposta de norma técnica ou diretriz aprovada por agência reguladora (CNEN, ANVISA).
6. **Relatório Técnico Conclusivo:** Laudo de auditoria de qualidade ou parecer técnico para medicina nuclear/PET-CT.
7. **Manual / Protocolo Clínico:** Guia de procedimentos operacionais padrão (POP) ou radioproteção.
8. **Base de Dados Técnico-Científica:** Data lake ou repositório estruturado de imagens médicas/dosimetria.
9. **Produto de Editoração:** Livro técnico, capítulo ou material instrucional.
10. **Processos e Materiais Não Patenteáveis:** Metodologia de calibragem de equipamentos ou tecnologia social de atendimento.

O campo booleano `req_ip_registration` torna obrigatório o anexo do comprovante de depósito no INPI ou publicação oficial quando a tipologia selecionada assim o exigir.

### 3.1. Tabela de campos Tipo de Produto (`capes.ptt.type`)

As 21 tipologias oficiais homologadas pelo CTC-ES.

| Campo Odoo | Metadado / Conceito CAPES | Tipo de Dado Odoo | Domínio / Regras de Validação |
| :--- | :--- | :--- | :--- |
| `axis_id` | Eixo Vinculado | `Many2one` | FK para `capes.ptt.axis`. |
| `code` | Código da Tipologia | `Char` | Valores de T01 a T21 (Ex: T19, T13). |
| `name` | Nome do Tipo de Produto | `Char` | Ex: Software, Patente, Tecnologia Social, Curso de Formação. |
| `req_ip` | Exige Propriedade Intelectual | `Boolean` | Se `True`, o produto final exigirá o anexo do registo (ex: INPI) no formulário. |



