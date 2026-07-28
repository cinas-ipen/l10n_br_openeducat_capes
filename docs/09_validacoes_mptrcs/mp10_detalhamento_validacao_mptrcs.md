# **Validação Técnica MP10 - Governança do Colegiado e Reuniões da CPG**

## **1. Introdução e Finalidade**

O **Macroprocesso 10** transforma o ERP na ferramenta oficial de orquestração da governança do programa. Ele conecta a instância deliberativa (Comissão de Pós-Graduação - CPG) aos processos administrativos e requerimentos discentes. Garante que nenhuma decisão estratégica seja tomada sem rastro, ata e aprovação colegiada.

## **2. Gestão da Composição da CPG (op.cpg.committee e op.cpg.member)**

Nenhuma reunião pode ser criada sem estar vinculada a uma composição de CPG vigente.

* **Cadastro de Gestão:** A secretaria registra a gestão atual (ex: "Gestão 2024-2027") com data de início e término.  
* **Quadro de Membros:** Especificação clara de cargos (Coordenador, Vice, Titulares, Suplentes e Representação Discente).  
* **Mandatos:** O registro de como o membro assumiu o cargo (Eleito pelos Pares ou Indicado pela Reitoria) é obrigatório, com campo para o número da portaria/ata de nomeação.  
* **Histórico de Gestões:** Gestões encerradas são automaticamente movidas para um arquivo histórico (Read-Only), assegurando a integridade das decisões tomadas em mandatos anteriores.

## **3. Workflow de Pauta e Reunião (op.cpg.meeting)**

A secretaria acadêmica gerencia a esteira de deliberações de forma estruturada, combinando fluxos automatizados com pautas administrativas diretas:

1. **Triagem (Secretaria):** Requerimentos do portal entram na fila waiting_screening. Se a documentação estiver completa, a secretaria a move para ready_for_agenda (Apto para Pauta).  
2. **Inclusão de Itens Administrativos:** Além dos requerimentos do portal, a secretaria pode incluir **Itens Administrativos Diretos** na pauta (ex: credenciamento docente, novos convênios, resoluções internas) que não possuem requerente discente, mas exigem deliberação.  
3. **Pauta:** O sistema compila uma lista única na reunião (op.cpg.meeting), contendo tanto os requerimentos do portal quanto os itens administrativos inclusos pela secretaria.  
4. **Convocação:** O sistema envia e-mails automáticos com a Ordem do Dia e links seguros para o dossiê de cada item da pauta.

## **4. O Motor de Template da Ata (QWeb) e o "Clique Auditável"**

A ata é um documento gerado pelo próprio ERP:

* **Padronização:** O motor QWeb compila o cabeçalho institucional, lista de presentes, pauta (tanto os requerimentos pautados quanto os itens administrativos) e deliberações em um PDF unificado.  
* **Clique Auditável:** Para aprovação da ata, o sistema substitui assinaturas físicas. Cada membro presente clica em "Aprovar Ata". O sistema registra **quem** aprovou, **quando** (timestamp) e de **qual IP**, criando um selo de auditoria imutável vinculado ao documento.

## **5. Gatilhos de Execução Autônoma**

A aprovação da ata é o gatilho final para o sistema:

* **Deferimento:** O requerimento (prorrogação, trancamento) assume o status "Deferido" e o Odoo executa a ação (ex: soma o prazo de prorrogação ao relógio do aluno).  
* **Congelamento:** A reunião e os documentos assinados são movidos para readonly.  
* **Transparência:** O PDF da Ata recebe o status "Publicado" e pode ser disponibilizado automaticamente no portal público do programa.

## **6. Resumo para Stakeholders (Parametrização MPTRCS)**

| Funcionalidade | Mecanismo | Benefício / Regra |
| :---- | :---- | :---- |
| **Composição da CPG** | Entidade fixa (Gestão) | Evita deliberações por membros sem mandato vigente. |
| **Pauta Mista** | Integração Portal + Itens Adm. | Permite que a secretaria inclua pautas que não originam de requerimentos discentes. |
| **Aprovação de Ata** | Clique Auditável (IP/User) | Segurança jurídica, rapidez e eliminação de papel. |
| **Execução de Decisões** | Gatilhos Autônomos | A decisão tomada em ata é refletida no perfil do aluno instantaneamente. |

*O MP10 centraliza a governança, transformando a CPG em um colegiado moderno, 100% digital e preparado para responder a qualquer auditoria dos órgãos de controle com precisão de minutos.*
