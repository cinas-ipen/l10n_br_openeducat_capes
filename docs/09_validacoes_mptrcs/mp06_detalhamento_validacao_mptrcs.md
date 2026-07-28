# **Validação Técnica MP6 - Ritos de Titulação, Bancas e Defesas**

## **1. Introdução e Finalidade**

O **Macroprocesso 06** é o ápice do percurso acadêmico do discente. Sua função é orquestrar o rito final de defesa (pública e solene), garantindo que todos os pré-requisitos regimentais tenham sido cumpridos e que a comissão julgadora esteja em estrita conformidade com as normas da CPG-MP. Este processo é o guardião da qualidade final do mestrado.

## **2. Travas de Elegibilidade (O Checklist de Defesa)**

O ERP atua como um fiscalizador rigoroso. O sistema bloqueia a abertura do agendamento da defesa até que o checklist eletrônico seja atendido:

* **Integralização:** O aluno deve atingir a meta global de créditos (ex: 100 créditos no MPTRCS) e ter sido aprovado em **todas** as disciplinas obrigatórias.  
* **Marcos Intermediários:** Aprovação no Seminário de Área (para Mestrado Profissional) ou Exame de Qualificação.  
* **Homologação do PTT:** O PTT deve estar homologado via fluxo cpg_checklist (para o MPTRCS) ou com estrato Qualis validado (qualis_prior), dependendo da parametrização do currículo.  
* **Ética (CEP):** Se o plano de trabalho exigir, o sistema verifica se o parecer consubstanciado de aprovação ética foi anexado.

## **3. Composição e Governança da Banca**

A estrutura da banca examinadora não é arbitrária; ela segue as regras parametrizadas para a versão curricular do aluno (op.curriculum.committee.rule), prevenindo nulidades jurídicas no título outorgado.

### **3.1. Regras de Composição**

* **Quórum e Papéis:** O sistema valida automaticamente o número mínimo de membros (ex: 3 titulares Doutores) e o papel de cada integrante.  
* **Voto do Orientador:** Parametrizável (voting_president ou non_voting_president). No MPTRCS, o orientador preside e possui direito a voto ativo.  
* **Endogenia:** O sistema trava o agendamento se não for cumprida a regra de membros externos ao PPG/IPEN (ex: mínimo de 1 examinador externo).  
* **Impedimentos Cíveis:** O motor de integridade cruza os dados do docente com o discente para bloquear parentesco de até 4º grau, conforme as normas de transparência.

### **3.2. Modalidade e Cronometria**

* **Presencial/Híbrida/Remota:** Definida pela política de defesa (defense_location_policy). No MPTRCS, adota-se a modalidade híbrida (presença física do discente e presidente).  
* **Cronometria:** O sistema registra a minutagem de exposição e arguição para conferência em ata (ex: 50 min de exposição).

## **4. Workflow de Agendamento e Execução**

1. **Solicitação:** Orientador protocola a banca no portal, anexando a versão final da dissertação.  
2. **Triagem:** Secretaria Acadêmica verifica a conformidade da banca e a elegibilidade do aluno.  
3. **Homologação da CPG:** A banca é submetida à deliberação do colegiado.  
4. **Sessão:** Realização da defesa e lavratura da ata automática via QWeb.  
5. **Depósito no Repositório (Fonte Ouro):** Após a aprovação, abre-se o prazo legal de 30 dias para depósito no DSpace.

## **5. Resumo para Stakeholders (Parametrização MPTRCS)**

| Funcionalidade | Configuração MPTRCS (IPEN) | Benefício / Regra |
| :---- | :---- | :---- |
| **Quórum Banca** | 3 Doutores | Padrão acadêmico de segurança. |
| **Voto Orientador** | voting_president | Orientador participa ativamente da decisão. |
| **Membros Externos** | Mínimo 1 externo | Evita endogenia e garante visão externa. |
| **Prazo Pós-Defesa** | 30 Dias | Garante a brevidade da titulação. |
| **Ata da Banca** | QWeb + Clique Auditável | Segurança jurídica e automação. |

*O MP6 blinda o IPEN contra futuras auditorias da CAPES/MEC ao exigir, de forma inegociável, que a banca de defesa seja constituída apenas por membros que respeitem o regimento, garantindo que a emissão do diploma digital (MEC 70/2025) tenha lastro legal indiscutível.*
