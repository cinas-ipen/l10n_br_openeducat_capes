### docs/07_padroes_de_interoperabilidade_externa/02_gopg_coleta_e_crosswalk_dspace.md

# Documento 02: DSpace, OAI-PMH e Crosswalk Semântico (Fonte Ouro)

## 1. A Fonte Ouro e a Trava de Metadados
Enquanto o Odoo (Fonte Prata) detém a verdade sobre a "Vida Acadêmica", o Repositório Institucional DSpace (Fonte Ouro) detém a verdade sobre o "Produto Final" (Teses, Dissertações e PTTs). O GoPG estabelece que a biblioteca digital é o fim da linha; a CAPES coleta o XML bibliográfico diretamente do DSpace via protocolo OAI-PMH (Open Archives Initiative Protocol for Metadata Harvesting).

O desafio arquitetural resolvido pelo `l10n_br_openeducat_capes_integration` é garantir que o aluno não deposite lixo no DSpace. O fluxo determina que:
1. O aluno defende a tese no Odoo.
2. A banca aprova no Odoo.
3. O Odoo gera um pacote de metadados selado.
4. O discente submete o PDF ao DSpace utilizando os metadados validados pelo Odoo.
5. Após o bibliotecário aprovar o depósito, o DSpace gera um Handle (URI).
6. Este Handle é averbado de volta no campo `repository_url` da classe `capes.thesis` no Odoo para liberar a geração do Diploma Digital.

## 2. O Contexto e Prefixo Exclusivo `oai_capes`
Para que os robôs da Plataforma Sucupira diferenciem uma dissertação normal de um arquivo de som histórico presente na biblioteca da IES, o repositório DSpace deve ser configurado com um contexto OAI-PMH específico.

A documentação determina a parametrização do container Tomcat/Solr do DSpace para expor o prefixo `oai_capes` (abandonando o uso genérico do `oai_dc` - Dublin Core, que é insuficiente para as ontologias da DAV).

## 3. Matriz de Mapeamento (Crosswalk XSLT)
O núcleo da interoperabilidade da Fonte Ouro é o arquivo de transformação XSLT (`oai_capes.xsl`) a ser injetado nas configurações do repositório institucional. Este arquivo faz a matriz "De / Para" (Crosswalk) traduzindo os metadados internos do DSpace (namespace `dim`) para as chaves XML obrigatórias da CAPES.

A configuração de interoperabilidade garantirá o mapeamento dos seguintes Identificadores Persistentes Essenciais:

| Metadado DSpace (dim) | Tag XML Exposta (`oai_capes`) | Origem da Informação (Odoo) |
| :--- | :--- | :--- |
| `dc.identifier.uri` | `<capes:identifier>` | DOI ou Handle gerado pelo RI. |
| `dc.contributor.author` | `<capes:author>` | `capes.thesis.student_id` |
| `dc.identifier.orcid` | `<capes:author_orcid>`| `res.partner.orcid` |
| `dc.contributor.advisor` | `<capes:advisor>` | `capes.thesis.committee.member_role='advisor'` |
| `dc.subject.cnpq` | `<capes:knowledge_area>`| `op.program.capes.basic_area` |
| `dc.relation.ispartof` | `<capes:program_code>` | `op.program.capes.snpg_code` (Chave Mestra) |
| `local.capes.ptt.axis` | `<capes:ptt_axis>` | `capes.ptt.product.type_id.axis_id` |
| `local.capes.ptt.stratum`| `<capes:ptt_stratum>` | `capes.ptt.evaluation.final_stratum` |

## 4. Orquestração do Crosswalk (Exemplo de Sintaxe)
O administrador do repositório deve implementar o crosswalk para extrair e cruzar os identificadores organizacionais e biográficos injetados originariamente pelo Odoo.

```xml
<xsl:template match="dim:dim">
    <oai_capes:thesis xmlns:oai_capes="http://capes.gov.br/oai/oai_capes/">
        <oai_capes:programCode>
            <xsl:value-of select="dim:field[@mdschema='local'][@element='capes'][@qualifier='snpg']"/>
        </oai_capes:programCode>
        
        <oai_capes:title>
            <xsl:value-of select="dim:field[@mdschema='dc'][@element='title']"/>
        </oai_capes:title>
        
        <oai_capes:author>
            <oai_capes:name>
                <xsl:value-of select="dim:field[@mdschema='dc'][@element='contributor'][@qualifier='author']"/>
            </oai_capes:name>
            <oai_capes:orcid>
                <xsl:value-of select="dim:field[@mdschema='dc'][@element='identifier'][@qualifier='orcid']"/>
            </oai_capes:orcid>
        </oai_capes:author>
        
        <oai_capes:institutionRor>
            <xsl:value-of select="dim:field[@mdschema='local'][@element='ies'][@qualifier='ror']"/>
        </oai_capes:institutionRor>
    </oai_capes:thesis>
</xsl:template>
```

Através desta dupla malha — a Fonte Prata (Odoo) a entregar dados relacionais em JSON ativo, e a Fonte Ouro (DSpace) a entregar a materialidade científica selada em XML passivo —, o ecossistema `l10n_br_openeducat_capes` cumpre integralmente a totalidade dos requisitos para a modernização exigida pela governança do MEC/CAPES em 2026.
