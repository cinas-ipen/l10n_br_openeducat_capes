# **Validação Técnica MP9 - Gestão do Corpo Docente e Rastreabilidade GoPG**

## **1. Introdução e Finalidade**

O **Macroprocesso 09** é fundamental para a governança docente exigida pela CAPES. A agência não solicita apenas um "retrato" atual, mas o "filme" (*timeline*) de toda a vida acadêmica e credenciamento. Este macroprocesso garante que toda alteração de status, categoria ou regime seja registrada cronologicamente.

## **2. Entidade de Vínculo Docente (op.faculty.program.link)**

A arquitetura adota uma tabela relacional entre o Docente (op.faculty) e o Programa (op.program.capes).

* **Multi-Vínculo:** Permite atuações simultâneas em diferentes PPGs sem conflito de dados.  
* **Histórico de Vínculos:** Mantém o registro histórico para auditoria da CAPES sobre em qual período o docente estava vinculado a qual programa.

## **3. O Livro-Razão de Categorias (Timeline de Credenciamento)**

Para atender à auditoria da CAPES, o sistema implementa a estrutura op.faculty.category.ledger.

* **Categoria:** Permanente, Colaborador, Visitante ou Assistente.  
* **Período de Vigência:** Data de Início e Data de Fim.  
* **Documento Comprobatório:** Obrigatório.  
* **Auditabilidade:** Registro *append-only* (apenas inserção).

### **3.1. Gestão de Exceções e Override de Credenciamento**

Em situações excepcionais (ex: pandemia ou deliberações extraordinárias do Conselho Superior), o programa pode necessitar prorrogar credenciamentos fora dos prazos padrão.

* **Fluxo de Override (op.administrative.override):** O sistema permite uma excepcionalidade administrativa que não viola a imutabilidade do Ledger. A secretaria abre um requerimento de override anexando a Portaria do Conselho Superior/CPG.  
* **Trava de Auditoria:** O sistema só permite a prorrogação se o override_id estiver vinculado a uma Ata da CPG (op.cpg.meeting) que contenha a deliberação de aprovação. O registro original de vencimento permanece, mas é anotado com uma referência de exceção, garantindo total transparência para auditorias externas.

## **4. Painel de Produção e Orientação (Prevenção de Sobrecarga)**

* **Monitoramento Real-Time:** Cruzamento com o Livro-Razão de alunos regulares (op.student.credit.ledger).  
* **Alerta de Sobrecarga:** Bloqueio automático para novos vínculos se o limite (ex: 8 alunos no IPEN) for atingido, salvo exceções aprovadas pelo comitê.

## **5. Resumo para Stakeholders (Parametrização MPTRCS)**

| Funcionalidade | Trava/Regra Sistêmica | Benefício para o Programa |
| :---- | :---- | :---- |
| **Timeline de Credenciamento** | Livro-Razão (category.ledger) | Evita glosas da CAPES por falta de comprovação. |
| **Exceções (Override)** | Vinculação à Ata/Portaria | Segurança jurídica para situações de força maior. |
| **Limite de Orientandos** | Trava automática (teto 8 alunos) | Qualidade da orientação e conformidade. |
| **Ata de Credenciamento** | Anexo PDF obrigatório | Origem legal preservada. |

*Este macroprocesso transforma a gestão docente em um fluxo de auditoria em tempo real.*
