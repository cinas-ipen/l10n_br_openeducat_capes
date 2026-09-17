# Documento 01: Visão Geral Sistêmica e Paradigma GoPG

## 1. Contexto Regulatório do Stricto Sensu Nacional
A administração acadêmica da pós-graduação *Stricto Sensu* no Brasil diferencia-se substancialmente dos modelos lineares norte-americanos e europeus, nos quais os sistemas de Enterprise Resource Planning (ERP) educacionais tradicionais são baseados. O ecossistema brasileiro exige o cumprimento de uma teia altamente complexa de resoluções internas combinadas a diretrizes rígidas das agências federais de fomento e regulação. 

A avaliação continuada promovida pela Coordenação de Aperfeiçoamento de Pessoal de Nível Superior (CAPES) impõe consequências severas às Instituições de Ensino Superior (IES) e Institutos de Pesquisa. Erros operacionais, omissões na prestação de contas de produção intelectual ou falhas na consistência temporal de vínculos docentes e discentes resultam no rebaixamento de notas e conceitos dos Programas de Pós-Graduação (PPGs). Esse rebaixamento gera impactos institucionais diretos, tais como a redução ou perda de verbas orçamentárias de fomento, cortes severos de bolsas de estudo para pesquisadores e, em última instância, a cassação da autorização de funcionamento do programa junto ao Ministério da Educação (MEC).

## 2. O Programa de Governança Colaborativa de Informações da Pós-Graduação (GoPG)
O Programa de Governança Colaborativa de Informações da Pós-Graduação (GoPG), instituído de forma oficial pela Portaria CAPES nº 158, de 17 de agosto de 2023, e complementado pela Instrução Normativa nº 1/2026, representa uma mudança de paradigma estrutural na coleta e auditoria de dados científicos e acadêmicos do país. O programa altera o modelo tradicional de alimentação manual periódica e descentralizada da Plataforma Sucupira por um ambiente interoperável em tempo real. 

Os objetivos fundamentais estabelecidos pelo GoPG compreendem:
* **Mitigação de Redundâncias Crônicas:** Eliminar a necessidade de redigitação manual de dados que já existem nos sistemas internos das instituições de ensino.
* **Garantia de Integridade e Rastreabilidade:** Assegurar que os dados informados sejam auditáveis e reflitam com exatidão matemática o histórico acadêmico em nível de banco de dados corporativo.
* **Coleta Ativa e Passiva Automatizada:** Substituir os fluxos analógicos baseados em preenchimento humano por janelas de coleta automatizadas diretamente nas plataformas institucionais integradas.

## 3. Arquitetura de Fontes de Dados (Ouro, Prata e Bronze)
O GoPG classifica a infraestrutura analítica e tecnológica das instituições em três níveis de precedência e confiabilidade regulatória:

### 3.1. Fonte Ouro (Repositórios Institucionais)
* **Definição e Escopo:** Representada pelo Repositório Institucional (RI), tipicamente operado por meio da plataforma de código aberto DSpace, sob a gestão e curadoria da biblioteca central.
* **Responsabilidade:** Custodiar, preservar e expor os arquivos digitais originais das teses, dissertações e os Produtos Técnicos e Tecnológicos (PTTs) gerados pelas defesas.
* **Trava Lógica Regulamentar:** Uma vez coletados pela CAPES via Fonte Ouro, os metadados bibliográficos sofrem um bloqueio relacional rígido na Plataforma Sucupira, impedindo edições gráficas manuais residuais pela secretaria ou coordenação. Qualquer correção ortográfica ou alteração de comissão julgadora exige obrigatoriamente a retificação na origem (DSpace) para reidratação dos dados no próximo ciclo de varredura.

### 3.2. Fonte Prata (Sistemas Acadêmicos de Gestão)
* **Definição e Escopo:** Representada pela plataforma modular `l10n_br_openeducat_capes` construída sobre o ecossistema ERP Odoo/OpenEduCat.
* **Responsabilidade:** Gerenciar e orquestrar de forma transacional o ciclo de vida completo do discente, o histórico de aproveitamento de créditos, os vínculos e recredenciamentos de docentes, e a infraestrutura de projetos de pesquisa vinculados às linhas de fomento.
* **Identidade Soberana e Multi-Vínculo Acadêmico:** Adota o modelo de separação estrita entre a **Identidade Discente Soberana** (registro em `op.student` com Registro Acadêmico — RA perene e unívoco por CPF na IES) e os **Vínculos Acadêmicos** (`op.student.course` / matrículas ativas). Isso assegura que um estudante que inicia sua trajetória institucional como Aluno Especial em disciplinas isoladas e posteriormente ingressa como Aluno Regular em um programa de pós-graduação (como o MPTRCS) mantenha exatamente o mesmo RA e histórico institucional auditável.
* **Trânsito Intra-IES e Governança de Disciplinas:** Permite a livre circulação discente entre programas da mesma IES (`op.program.capes` sob a mesma `res.company`), garantindo que disciplinas intra-IES sejam incorporadas em valor nominal de créditos (100% de peso), ao passo que disciplinas de programas vinculados a outras universidades (extra-IES, como o programa de Tecnologia Nuclear USP/IPEN frente ao MPTRCS) sejam submetidas a requerimento prévio e deliberação da CPG sob o teto de créditos externos.
* **Interoperabilidade:** Expor endpoints RESTful estruturados em JSON leves e protegidos por criptografia para fornecer o censo acadêmico contínuo exigido para as avaliações quadrienais.

### 3.3. Fonte Bronze (Inserção Manual Residual)
* **Definição e Escopo:** Consiste no preenchimento manual de formulários diretamente na interface Web da Plataforma Sucupira.
* **Diretriz de Descontinuidade:** O GoPG visa erradicar progressivamente a dependência deste método arcaico. A persistência de erros ou incompletudes que forcem o uso da Fonte Bronze gera retrabalho burocrático e eleva o risco de não conformidade nos fechamentos estatísticos.

## 4. Macrodinâmica da Rede RICA|PG e Fluxos de Coleta
A coordenação das conexões em rede e o reuso de dados ocorrem através da Rede de Integração da Comunidade Acadêmica da Pós-Graduação (RICA|PG). A arquitetura estabelece que os dados devem nascer unicamente na sua fonte originária mais confiável. 

O OpenEduCat atua como a espinha dorsal de validação semântica: ele unifica as regras acadêmicas e os Identificadores Persistentes (PIDs), garantindo que no momento do depósito legal no DSpace, o discente insira informações pré-auditadas pelo ERP acadêmico. O robô coletor governamental aciona os endpoints da Fonte Prata para cruzar os dados de matrícula com o endpoint OAI-PMH (sob o prefixo customizado `oai_capes`) exposto pela Fonte Ouro, consolidando o pacote de informações sem intervenção humana.

```text
       +-------------------------------------------------------+
       |                     CAPES / RICA|PG                   |
       +----------------------------+--------------------------+
                                    |
            +-----------------------+-----------------------+
            | Coleta Passiva (JSON) | Coleta OAI-PMH (XML)  |
            v                                               v
+-----------------------+                       +-----------------------+
|      FONTE PRATA      |  Validação Semântica  |       FONTE OURO      |
|  OpenEduCat ERP Odoo  |======================>|     DSpace Server     |
|   (Dados Acadêmicos)  |    e Injeção de PIDs  | (Teses, Dissert. PTT) |
+-----------------------+                       +-----------------------+
```

## 5. Fases de Implementação e Homologação Técnica (T1 a T5)
A adequação institucional do ecossistema segue rigorosamente as cinco etapas procedimentais e progressivas estipuladas pelo Guia Orientador oficial da CAPES, condicionando o avanço à aprovação de validadores governamentais:

* **T1: Treinamento e Usabilidade:** Capacitação intensiva das equipes multidisciplinares corporativas (Tecnologia da Informação, bibliotecários curadores e coordenações de PPGs) acerca dos dicionários de metadados, ontologias da DAV e ferramentas de monitoramento de integridade.
* **T2: Implantação de Ferramentas:** Instalação e provisionamento da suite de módulos do monorepo `l10n_br_openeducat_capes` no Odoo, configuração do container Apache Tomcat e indexadores Solr no servidor do repositório, e testes preliminares de infraestrutura de rede e segurança de endpoints.
* **T3: Configuração de Dados:** Mapeamento semântico exaustivo dos campos locais. Desenvolvimento de planilhas matriciais "de / para" e codificação de crosswalks baseados em transformações XSLT no DSpace, em paralelo à estruturação de views SQL e payloads JSON no barramento de integração do OpenEduCat.
* **T4: Homologação e Testes:** Solicitação de credenciais de escopo temporário junto à agência de fomento. Envio controlado de lotes de dados reais em ambiente de *sandbox* da CAPES para validação de integridade relacional, correção iterativa de falhas de serialização e tratamento de rejeições apontadas pelos validadores automáticos.
* **T5: Ambiente de Produção:** Ativação definitiva de chaves e Bearer Tokens de produção. Abertura segura e ininterrupta das rotas de API para varredura passiva agendada pela ferramenta federal de extração de dados acadêmicos, operando sob o cumprimento estrito das diretrizes de segurança digital da LGPD.
