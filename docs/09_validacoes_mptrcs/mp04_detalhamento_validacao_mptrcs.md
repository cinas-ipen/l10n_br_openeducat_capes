# **Validação Técnica MP4 - Requerimentos, Vigilância Cronológica e Jubilamento**

## **1. Introdução**

O **Macroprocesso 04** é o "mecanismo de defesa" do PPG. Sua função é garantir o cumprimento rigoroso dos prazos regimentais e a aplicação dos requerimentos discentes, assegurando que o programa mantenha indicadores saudáveis de "Tempo Médio de Titulação" para a CAPES. Ele atua de forma proativa, fiscalizando o relógio acadêmico de cada aluno.

## **2. O Relógio Implacável: Monitoramento de Prazos**

O sistema centraliza o controle cronológico a partir da admission_date (Data de Ingresso) do discente. O parâmetro mestre é o max_months_defense (Prazo Máximo de Titulação) configurado no regimento vigente do aluno (op.curriculum.version).

* **O parâmetro no MPTRCS:** O sistema está configurado com **24 meses** para o Mestrado Profissional, sendo este o gatilho principal para alertas automáticos ao discente e ao orientador.

## **3. Subprocessos de Gestão Cronológica**

### **3.1. Trancamento de Matrícula (Suspensão) – Conforme Art. 22º e 23º**

O sistema operacionaliza o trancamento garantindo a conformidade legal e a integridade da jornada acadêmica, sem restrições de período letivo inicial:

* **Regra de Justificativa (Art. 22º):** O sistema valida solicitações baseadas nos incisos do regulamento:  
  * I. Convocação para serviço militar;
  * II. Problemas de saúde incapacitantes (exige atestado médico);
  * III. Acompanhamento de cônjuge ou parente de primeiro grau para tratamento de saúde (exige atestado médico);  
  * IV. Demais casos previstos em lei ou situações excepcionais (sujeitas à deliberação da CPG-MP, conforme Art. 22º, §4º).  
* **Flexibilidade de Pedido:** Em conformidade com o Art. 22º, §1º, o trancamento pode ser requerido em **qualquer tempo**, não havendo trava sistêmica para o 1º semestre letivo. O parâmetro `block_first_semester_trancamento` (Bool) controla o bloqueio no 1º semestre (Configurado como False no MPTRCS).
* **Retorno do Estudante (Art. 23º):** O retorno está condicionado à continuidade do curso, devendo o aluno seguir a estrutura curricular vigente na data de seu retorno. Para evitar o hibridismo normativo, o aluno cumpre a nova matriz, mas as disciplinas já aprovadas permanecem integradas ao seu patrimônio acadêmico (Ato Jurídico Perfeito).  
* **Limite Contínuo (Art. 22º, §3º):** O sistema aplica uma trava algorítmica **parametrizável**  (`max_trancamento_days`): o período máximo de trancamento contínuo.
* **Exceções Autoritativas (Override):** Para trancamentos que excedem os limites regimentais (ex: pandemia), o sistema exige a vinculação da Portaria do Conselho Superior/CPG e do Parecer favorável. Esse ato fica permanentemente registrado no prontuário do aluno como "Exceção Administrativa Auditável" (`op.administrative.override`), garantindo que, durante uma auditoria, o IPEN possa provar que a quebra de prazo foi um ato legal e fundamentado.

### **3.2. Prorrogações de Prazo**

* **Prorrogação Regular:** Solicitada via portal por aluno e orientador. O sistema valida se o aluno já possui o Plano de Trabalho homologado e a Qualificação aprovada.
* **Limite no MPTRCS:** O teto de prorrogação é de **90 dias**, conforme configurado em `max_extension_days`.
* **Exceções Autoritativas (Override):** Para prorrogações que excedem os limites regimentais (ex: pandemia), o sistema exige a vinculação da Portaria do Conselho Superior/CPG e do Parecer favorável. Esse ato fica permanentemente registrado no prontuário do aluno como "Exceção Administrativa Auditável" (`op.administrative.override`), garantindo que, durante uma auditoria, o IPEN possa provar que a quebra de prazo foi um ato legal e fundamentado.


## **4. Jubilamento Automático (pending_dismissal)**

Este é o processo de autoproteção do programa para evitar a inflação negativa nos indicadores de desempenho junto à CAPES. Diariamente, à meia-noite, uma Ação Agendada (Cron Job) varre os prazos:

1. **Estouro de Prazo:** Estudantes que ultrapassarem o prazo (Ingresso + meses regimentais + trancamentos + prorrogações) sem depósito de dissertação são movidos para pending_dismissal.
2. **Reprovação Dupla:** O sistema monitora reprovações acumuladas. Duas reprovações em disciplinas OU duas reprovações em ritos acadêmicos (Exame de Qualificação/Seminário) disparam o desligamento.
3. **Efeito Imediato:** O status pending_dismissal corta imediatamente a exportação do discente como "Ativo" para os endpoints da CAPES (Fonte Prata), protegendo a nota do programa.

## **5. Portal, Requerimentos e Governança da CPG**

Toda interação é descentralizada e auditável via `op.academic.request`.

1. **Triagem (Secretaria):** O chamado entra no status `waiting_screening`. A secretaria valida documentos (pendências na biblioteca/financeiro). Se correto, vira ready_for_agenda.
2. **Reunião da CPG:** O item é puxado para a pauta da reunião (`op.cpg.meeting`).
3. **Template de Ata (QWeb):** O sistema compila a ata em PDF automaticamente.
4. **Clique Auditável:** Membros da CPG aprovam a ata no sistema (grava-se User ID, Timestamp e IP), garantindo conformidade sem necessidade de assinatura física.
5. **Gatilho de Execução:** Após aprovação, o status muda automaticamente (ex: "Deferido" e o sistema já injeta os dias de prorrogação ou atualiza o regimento/status (trancamento) no perfil do aluno).

## **6. Resumo para Stakeholders (Parametrização MPTRCS)**

| Funcionalidade | Trava/Regra Sistêmica | Benefício para o Programa |
| :---- | :---- | :---- |
| **Limite de Trancamento** | 365 dias corridos (`max_trancamento_days`) | Evita a "perpetuação" do aluno no sistema. |
| **Prorrogação Regular** | 90 dias (`max_extension_days`) | Mantém o aluno dentro do ritmo CAPES. |
| **Jubilamento** | Cron Job (Meia-noite) | Protege os indicadores de produtividade. |
| **Ata da CPG** | Clique Auditável (IP/User) | Segurança jurídica das deliberações. |
| **Triagem** | Secretaria (Pre-flight) | Evita pautas com documentação incompleta. |

Este detalhamento garante que o MPTRCS tenha total controle sobre o fluxo cronológico dos seus discentes, automatizando a gestão burocrática e focando na qualidade acadêmica.
