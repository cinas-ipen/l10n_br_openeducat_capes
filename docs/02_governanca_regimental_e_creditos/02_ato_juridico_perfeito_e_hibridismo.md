# Documento 02: Ato Jurídico Perfeito, Hibridismo e Regras de Transição

## 1. Natureza do Vínculo Acadêmico e a Inexistência de Direito Adquirido
Um dos maiores focos de erro administrativo nas secretarias de pós-graduação durante transições normativas é a presunção do "direito adquirido". A modelagem do OpenEduCat fundamenta-se na pacífica jurisprudência nacional de que **não existe direito adquirido a regime acadêmico**. As universidades exercem autonomia didático-científica e o regulamento atua como atos-regra mutáveis.

Isso implica sistemicamente que normas supervenientes, como a redução do prazo de titulação ou o endurecimento dos critérios de exame de qualificação, aplicam-se de forma imediata aos alunos já matriculados. O ERP, portanto, não pode congelar indefinidamente as expectativas de direito do ano de ingresso do aluno se o programa deliberar pela atualização.

## 2. A Tutela Sistêmica do Ato Jurídico Perfeito
Embora o direito adquirido global não exista, a arquitetura do banco de dados deve prover proteção inabalável ao **Ato Jurídico Perfeito**. Isso significa que atividades integralmente concluídas, avaliadas e registradas no histórico escolar sob a égide de um regimento anterior não podem ser retroativamente invalidadas pelo sistema.

Se um estudante obteve aprovação em uma disciplina de 4 créditos sob um regimento antigo, e a nova versão do currículo altera essa mesma disciplina para 6 créditos ou a extingue da grade, o algoritmo do OpenEduCat é programado para **não recalcular** retroativamente o histórico escolar do estudante. A nota e os créditos originalmente conquistados incorporam-se imutavelmente ao seu patrimônio acadêmico. O mesmo princípio de proteção absoluta aplica-se aos exames de proficiência e qualificações já superados.

## 3. A Vedação Algorítmica ao Hibridismo Normativo
O sistema implementa uma trava de arquitetura rigorosa contra o "hibridismo normativo". A doutrina da incindibilidade determina que é terminantemente proibida a combinação utilitarista de normativas.

O algoritmo Python vinculado ao `op.curriculum.version` bloqueia tentativas de um estudante exigir o cumprimento da carga menor de disciplinas de um regimento recente e, simultaneamente, tentar invocar os prazos de prorrogação mais permissivos de um regimento obsoleto. A opção por um regimento submete o aluno incondicionalmente à totalidade daquela versão.

## 4. O Fluxo de Migração e Direito de Opção via Portal
As atualizações de currículo não devem ser aplicadas pela secretaria de forma silenciosa ou arbitrária sem documentação formal. A transição exige a ativação do "Direito de Opção".

Foi projetado no módulo `l10n_br_openeducat_capes_academic` o requerimento `op.academic.request.regime_migration` acessível pelo Portal do Aluno. A lógica operacional dita que:
1. O aluno inicia o requerimento e o sistema renderiza um quadro comparativo (ex: matriz de redução de créditos vs. novos exames exigidos).
2. O discente submete o pleito mediante a assinatura digital de um termo de aceitação irrevogável.
3. Após aprovação eletrônica do colegiado, o código Odoo executa a migração sistêmica: ele encerra a leitura do livro-razão de créditos associada à versão antiga e abre a contabilidade na nova versão atrelada ao aluno (`curriculum_version_id`), acionando os novos gatilhos cronológicos.

## 5. O Ato Jurídico Perfeito no Aproveitamento de Disciplinas de Aluno Especial

O aproveitamento de disciplinas cursadas no regime de Aluno Especial em momento anterior ao ingresso regular segue com rigor a preservação do Ato Jurídico Perfeito:

* **Inviolabilidade da Nota e Carga:** A disciplina cursada sob regime especial permanece intacta no Livro-Razão primitivo com seu conceito e frequência originais. O sistema não permite reclassificação nem recálculo de notas.
* **Mecanismo Append-Only de Incorporação:** Ao ser deferido o requerimento de aproveitamento (`op.special.credit.incorporation.request`), o sistema insere um novo evento contábil no livro-razão com tipologia `subject_special_incorporated`, vinculando o ato deliberativo da CPG e preservando o registro histórico da quarentena original.
* **Preclusão Temporal (Decadência):** Transcorrido o prazo decadencial regimental (padrão de 36 meses entre a conclusão da disciplina e o ingresso regular), a prerrogativa de aproveitamento é extinta por imperativo legal, impedindo a revalidação anacrônica de conteúdos programáticos defasados.
