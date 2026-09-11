# **Validação Técnica MP8 - Interoperabilidade e Envio de Dados (GoPG/CAPES)**

## **1. Introdução e Finalidade**

O **Macroprocesso 08** é o elo de conexão do ecossistema do IPEN com o ecossistema federal de fomento. Sua função é garantir que todos os dados de vida acadêmica, titulação e produção científica (PTTs) sejam transmitidos à CAPES e ao MEC com integridade, segurança e automação total, eliminando a "Fonte Bronze" (digitação manual na Plataforma Sucupira).

O sistema opera sob o paradigma do **GoPG (Governança Colaborativa de Informações da Pós-Graduação)**, que estabelece o fluxo unificado de dados a partir das fontes primárias.

## **2. A Arquitetura das Fontes de Dados (Ouro e Prata)**

Para que o MPTRCS tenha nota máxima na avaliação, a interoperabilidade deve ser precisa:

* **Fonte Ouro (DSpace/Repositório):** É a fonte da verdade da produção acadêmica e científica. A Biblioteca Central realiza o upload oficial e a curadoria do PDF final da dissertação e PTT no DSpace, exposto via OAI-PMH (`oai_capes`), gerando o **Handle (URI persistente)** averbado no Odoo (`repository_url`).  
* **Fonte Prata (OpenEduCat/Odoo):** É a fonte da verdade da vida acadêmica (alunos, docentes, disciplinas, créditos, bancas). O Odoo expõe endpoints RESTful que são consumidos pelos robôs coletores da CAPES.

## **3. Workflow de Interoperabilidade (O Motor de Integração)**

O processo segue uma lógica de dupla malha de dados:

1. **Camada Passiva (REST API):** O Odoo expõe rotas seguras para que a RICA|PG (Rede de Integração da Comunidade Acadêmica da Pós-Graduação) realize a varredura automática.  
2. **Camada de Metadados (OAI-PMH):** O DSpace expõe o protocolo OAI-PMH com o prefixo oai_capes. O Odoo garante que os metadados que chegam ao DSpace já contenham os PIDs (Identificadores Persistentes) corretos, como o ORCiD e o DOI, injetados durante o fluxo do MP05 e MP06.

## **4. Endpoints da API (Fonte Prata)**

O submódulo l10n_br_openeducat_capes_integration centraliza a inteligência de conectividade. Os principais *endpoints* expostos são:

| Endpoint | Objetivo | Dados Transmitidos |
| :---- | :---- | :---- |
| /api/capes/v1/students | Censo Acadêmico | Vínculos, PIDs (CPF/ORCiD), status, regimento. |
| /api/capes/v1/faculty | Credenciamento Docente | Timeline de credenciamento (Ledger), Lattes, carga horária. |
| /api/capes/v1/curriculums | Estrutura Curricular | Disciplinas, ementas, cargas, regras de versionamento. |
| /api/capes/v1/projects_and_ptts | Produção Acadêmica | Projetos, dissertações defendidas e PTTs com estratos Qualis. |

## **5. Segurança Criptográfica (LGPD e Compliance)**

A transmissão de dados sensíveis segue diretrizes rigorosas:

* **Autenticação:** O acesso é protegido via *OAuth 2.0* com *Mutual TLS* (mTLS), garantindo que apenas o servidor homologado pela RICA|PG consiga requisitar os dados.  
* **Privacy by Design:** O serializador JSON do Odoo foi configurado para **excluir** dados de natureza estritamente privada (como contatos telefônicos pessoais, prontuários de saúde ou informações financeiras), enviando apenas o necessário para a avaliação da CAPES.

## **6. Sincronização com o DSpace (Fonte Ouro)**

Para que a CAPES valide a "Fonte Ouro", o MPTRCS deve garantir a consistência através do mapeamento semântico (Crosswalk):

1. **Averbação de Identificadores & Manifesto:** O Odoo, ao titular o discente e emitir o manifesto de metadados (`library_manifest_payload`), encaminha os dados e PIDs (DOI, ORCiD, SNPG) para a Biblioteca Central realizar o upload no DSpace e averbar o Handle de volta no Odoo.  
2. **Transformação XSLT:** O DSpace utiliza o arquivo oai_capes.xsl para transformar os metadados internos (padrão Dublin Core dim) para o XML exigido pela CAPES, garantindo que o snpg_code e o orcid do autor estejam presentes.

## **7. Resumo de Validação para Stakeholders (IPEN)**

| Requisito | Trava/Regra Sistêmica | Benefício para o Programa |
| :---- | :---- | :---- |
| **PIDs (ORCiD/DOI)** | Obrigatório em op.student/capes.thesis | Evita glosas na avaliação por dados duplicados ou nulos. |
| **Barramento REST** | OAuth 2.0 / mTLS | Segurança total contra vazamento de dados. |
| **Integração DSpace** | Averbação do Handle | Garante a "Fonte Ouro" como verídica. |
| **Sincronia Semântica** | Prefixo oai_capes | Permite que o robô da CAPES diferencie PTTs de bibliografia comum. |

*Este macroprocesso transforma o MPTRCS em um programa "nativamente interoperável", eliminando a dependência do preenchimento manual da Plataforma Sucupira e garantindo que o IPEN responda aos indicadores da CAPES de forma automática, precisa e auditável.*
