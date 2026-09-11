# **Validação Técnica MP7 - Expedição Documental e Diploma Digital**

## **1. Introdução e Finalidade**

O **Macroprocesso 07** operacionaliza o encerramento do vínculo acadêmico. No contexto IPEN/USP, este processo é bifásico:

1. **IPEN (Origem/Validação):** Responsável pela auditoria final, consolidação do dossiê acadêmico e envio dos dados à USP.  
2. **USP (Registradora/Emissora):** Responsável pela emissão final do Diploma Nato-Digital, em conformidade com a Portaria MEC nº 70/2025.

A finalidade deste processo no ERP é compilar o "Pacote de Titulação" com rigor criptográfico e conformidade legal, garantindo que a USP receba dados imutáveis e auditáveis.

## **2. O Pacote de Titulação (Envio IPEN -> USP)**

Uma vez que o discente atinge o status "Titulado" no IPEN (após o upload da versão final do PDF pelo discente e a chancela/validação da Secretaria Acadêmica), o sistema congela a vida acadêmica e prepara o **Dossiê Digital de Expedição**, que deve ser transmitido para o sistema da USP.

Este pacote contém:

* **XML de Registro Acadêmico:** Dados civis do egresso, carga horária total, disciplinas cursadas, notas, frequência e resumo da dissertação.  
* **Evidências de Defesa:** Ata de defesa com a composição da banca (identificando o membro externo) e a validação do quórum regimental.  
* **Evidências de PTT:** Registro do PTT homologado, com seu respectivo estrato Qualis e URL de acesso ao Repositório Institucional (DSpace).  
* **Hash de Integridade:** O ERP IPEN gera um *Hash SHA-256* de todo o pacote de dados enviado, garantindo que o que foi enviado é exatamente o que a USP receberá.

## **3. Fluxo de Expedição (Workflow IPEN-USP)**

`[IPEN: Auditoria de Elegibilidade Final (Créditos, PTT, Defesa, CEP)]`  
               `│`  
               `▼`  
`[IPEN/ERP: Compila Dossiê Digital + Assinatura Digital do Coordenador]`  
               `│`  
               `▼`  
`[IPEN -> USP: Transmissão via API / Canal Seguro]`  
               `│`  
               `▼`  
`[USP: Validação do Dossiê e Assinatura da Autoridade Registradora]`  
               `│`  
               `▼`  
`[USP: Emissão do Diploma Nato-Digital (Portaria MEC 70/2025)]`  
               `│`  
               `▼`  
`[Discente: Download do Diploma na Carteira Digital da USP]`

## **4. Governança e Responsabilidades (Matriz de Stakeholders)**

| Ator | Responsabilidade no Processo |
| :---- | :---- |
| **IPEN (Secretaria/CPG)** | Validação acadêmica, auditoria de documentos e envio do dossiê. |
| **USP (Registradora)** | Conferência final de dados, assinatura digital oficial e expedição. |
| **ERP (OpenEduCat)** | Motor de auditoria, cálculo de créditos e selagem do dossiê (Hash). |

## **5. Roteiro para Reunião de Validação (Secretaria IPEN e TI USP)**

Para validar este fluxo de expedição, sugiro focar nos seguintes pontos de pauta:

1. **Padronização do Pacote de Dados:** Definir a estrutura (schema) do JSON/XML que o IPEN enviará para a USP, garantindo que os metadados acadêmicos da CAPES estejam presentes.  
2. **Homologação da RVDD:** Validar se o template do diploma (PDF) emitido pela USP está recebendo corretamente os dados orquestrados pelo IPEN.  
3. **Protocolo de Retorno:** Definir como a USP sinaliza ao sistema do IPEN que o diploma foi emitido, para que o status do aluno possa ser atualizado de "Titulado" para "Diploma Expedido" automaticamente.  
4. **Infraestrutura de Assinatura:** Confirmar se a USP aceitará a assinatura do Coordenador do IPEN no dossiê de envio como parte da "Declaração de Veracidade da Origem".
